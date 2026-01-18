#!/usr/bin/env python3
"""
Export sono-eval assessment data to a database for Superset visualization.

This script reads assessment data from MemUStorage JSON files and exports them
to a SQL database (SQLite or PostgreSQL) where they can be queried by Apache Superset.

Usage:
    # Export to SQLite (default)
    python export_to_db.py --format sqlite

    # Export to PostgreSQL
    python export_to_db.py --format postgresql --db-uri "postgresql://user:pass@localhost/db"

    # Export from specific storage path
    python export_to_db.py --storage-path ./data/memory --format sqlite
"""

import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))

from sono_eval.assessment.models import AssessmentResult, MicroMotive, PathScore, PathType
from sono_eval.memory.memu import CandidateMemory, MemUStorage
from sono_eval.utils.config import get_config

# Add database directory to path for imports
database_dir = Path(__file__).parent.parent / "database"
sys.path.insert(0, str(database_dir))

from models import Assessment, Candidate
from models import MicroMotive as DBMicroMotive
from models import PathScore as DBPathScore
from models import ScoringMetric

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


class AssessmentExporter:
    """Export assessment data to SQL database."""

    def __init__(self, db_uri: str):
        """Initialize exporter with database URI.

        Args:
            db_uri: SQLAlchemy database URI
        """
        self.db_uri = db_uri
        self.engine = create_engine(db_uri, echo=False)
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self):
        """Create all tables if they don't exist."""
        logger.info("Creating database tables...")
        from models import Base

        Base.metadata.create_all(self.engine)
        logger.info("✓ Tables created successfully")

    def load_assessments_from_memory(
        self, storage_path: Optional[Path] = None
    ) -> List[Dict[str, Any]]:
        """Load assessments from MemUStorage.

        Args:
            storage_path: Optional path to memory storage directory

        Returns:
            List of assessment data dictionaries
        """
        logger.info(f"Loading assessments from memory storage...")
        assessments = []

        # Initialize storage
        if storage_path:
            storage = MemUStorage(storage_path=storage_path)
        else:
            storage = MemUStorage()

        # Get all candidate memory files
        storage_dir = storage.storage_path
        if not storage_dir.exists():
            logger.warning(f"Storage directory {storage_dir} does not exist")
            return assessments

        # Find all JSON files (candidate memory files)
        for json_file in storage_dir.glob("*.json"):
            try:
                candidate_id = json_file.stem
                memory = storage.get_candidate_memory(candidate_id)

                if not memory:
                    continue

                # Search for assessment nodes
                for node in memory.nodes.values():
                    if node.metadata.get("type") == "assessment":
                        assessment_result = node.data.get("assessment_result")
                        if assessment_result:
                            assessment_result["candidate_id"] = candidate_id
                            assessments.append(assessment_result)

            except Exception as e:
                logger.warning(f"Error loading {json_file}: {e}")
                continue

        logger.info(f"Loaded {len(assessments)} assessments from memory")
        return assessments

    def export_assessment(self, assessment_data: Dict[str, Any], session) -> bool:
        """Export a single assessment to database.

        Args:
            assessment_data: Assessment data dictionary
            session: SQLAlchemy session

        Returns:
            True if successful
        """
        try:
            # Parse assessment result
            result = AssessmentResult.model_validate(assessment_data)

            # Create or update candidate
            candidate = session.query(Candidate).filter_by(candidate_id=result.candidate_id).first()
            if not candidate:
                candidate = Candidate(
                    candidate_id=result.candidate_id,
                    created_at=result.timestamp,
                    total_assessments=0,
                    average_score=0.0,
                    highest_score=0.0,
                    lowest_score=100.0,
                )
                session.add(candidate)

            # Update candidate statistics
            candidate.total_assessments += 1
            candidate.last_assessment_at = result.timestamp

            # Update average score
            if candidate.total_assessments == 1:
                candidate.average_score = result.overall_score
                candidate.highest_score = result.overall_score
                candidate.lowest_score = result.overall_score
            else:
                # Recalculate average (simplified - in production, use proper aggregation)
                total_score = (
                    candidate.average_score * (candidate.total_assessments - 1)
                    + result.overall_score
                )
                candidate.average_score = total_score / candidate.total_assessments
                candidate.highest_score = max(candidate.highest_score, result.overall_score)
                candidate.lowest_score = min(candidate.lowest_score, result.overall_score)

            # Create assessment record
            assessment = Assessment(
                assessment_id=result.assessment_id,
                candidate_id=result.candidate_id,
                timestamp=result.timestamp,
                overall_score=result.overall_score,
                confidence=result.confidence,
                dominant_path=(result.dominant_path.value if result.dominant_path else None),
                summary=result.summary,
                key_findings=result.key_findings,
                recommendations=result.recommendations,
                engine_version=result.engine_version,
                processing_time_ms=result.processing_time_ms,
                metadata=result.metadata,
            )
            session.add(assessment)

            # Export path scores
            for path_score in result.path_scores:
                db_path_score = DBPathScore(
                    assessment_id=result.assessment_id,
                    candidate_id=result.candidate_id,
                    path_type=path_score.path_type.value,
                    score=path_score.score,
                    confidence=path_score.confidence,
                    metrics_count=len(path_score.metrics),
                    strengths_count=len(path_score.strengths),
                    weaknesses_count=len(path_score.weaknesses),
                    timestamp=result.timestamp,
                )
                session.add(db_path_score)

                # Export metrics
                for metric in path_score.metrics:
                    db_metric = ScoringMetric(
                        assessment_id=result.assessment_id,
                        path_type=path_score.path_type.value,
                        metric_name=metric.name,
                        score=metric.score,
                        weight=metric.weight,
                        evidence_count=len(metric.evidence),
                        timestamp=result.timestamp,
                    )
                    session.add(db_metric)

            # Export micro-motives
            for motive in result.micro_motives:
                db_motive = DBMicroMotive(
                    assessment_id=result.assessment_id,
                    candidate_id=result.candidate_id,
                    motive_type=motive.motive_type.value,
                    strength=motive.strength,
                    evidence_count=len(motive.evidence),
                    timestamp=result.timestamp,
                )
                session.add(db_motive)

            return True

        except Exception as e:
            logger.error(
                f"Error exporting assessment {assessment_data.get('assessment_id', 'unknown')}: {e}"
            )
            return False

    def export_all(self, storage_path: Optional[Path] = None) -> int:
        """Export all assessments to database.

        Args:
            storage_path: Optional path to memory storage directory

        Returns:
            Number of assessments exported
        """
        assessments = self.load_assessments_from_memory(storage_path)
        if not assessments:
            logger.warning("No assessments found to export")
            return 0

        session = self.Session()
        exported = 0

        try:
            for assessment_data in assessments:
                if self.export_assessment(assessment_data, session):
                    exported += 1

            session.commit()
            logger.info(f"✓ Exported {exported}/{len(assessments)} assessments successfully")

        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            session.close()

        return exported


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Export sono-eval assessments to database")
    parser.add_argument(
        "--format",
        choices=["sqlite", "postgresql"],
        default="sqlite",
        help="Database format (default: sqlite)",
    )
    parser.add_argument(
        "--db-uri",
        help="Database URI (e.g., postgresql://user:pass@localhost/db)",
    )
    parser.add_argument(
        "--storage-path",
        type=Path,
        help="Path to memory storage directory",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("./sono_eval_assessments.db"),
        help="Output SQLite database path (default: ./sono_eval_assessments.db)",
    )

    args = parser.parse_args()

    # Determine database URI
    if args.db_uri:
        db_uri = args.db_uri
    elif args.format == "sqlite":
        db_uri = f"sqlite:///{args.output.absolute()}"
    else:
        logger.error("--db-uri required for PostgreSQL")
        return 1

    # Create exporter
    exporter = AssessmentExporter(db_uri)
    exporter.create_tables()

    # Export assessments
    exported = exporter.export_all(args.storage_path)

    if exported > 0:
        logger.info(f"✓ Successfully exported {exported} assessments to {db_uri}")
        logger.info("You can now connect Superset to this database")
    else:
        logger.warning("No assessments were exported")

    return 0


if __name__ == "__main__":
    sys.exit(main())
