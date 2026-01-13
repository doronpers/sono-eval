"""
SQLAlchemy models for sono-eval assessment database.

These models define the database schema for storing assessment data
that can be visualized in Apache Superset dashboards.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import JSON, Boolean, Column, DateTime, Float, Index, Integer, String, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Assessment(Base):
    """Model for assessment results."""

    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    assessment_id = Column(String(255), nullable=False, unique=True, index=True)
    candidate_id = Column(String(255), nullable=False, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    # Overall scores
    overall_score = Column(Float, nullable=False, index=True)
    confidence = Column(Float, nullable=False, index=True)

    # Dark Horse tracking
    dominant_path = Column(String(50), index=True)

    # Explainability
    summary = Column(Text)
    key_findings = Column(JSON)  # List of strings
    recommendations = Column(JSON)  # List of strings

    # Metadata
    engine_version = Column(String(50))
    processing_time_ms = Column(Float)
    metadata = Column(JSON)

    # Indexes for common queries
    __table_args__ = (
        Index("idx_assessment_candidate_timestamp", "candidate_id", "timestamp"),
        Index("idx_assessment_score", "overall_score"),
        Index("idx_assessment_confidence", "confidence"),
        Index("idx_assessment_dominant_path", "dominant_path"),
    )

    def __repr__(self):
        return f"<Assessment(id={self.assessment_id}, candidate={self.candidate_id}, score={self.overall_score})>"


class PathScore(Base):
    """Model for individual path scores within an assessment."""

    __tablename__ = "path_scores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    assessment_id = Column(String(255), nullable=False, index=True)
    candidate_id = Column(String(255), nullable=False, index=True)
    path_type = Column(String(50), nullable=False, index=True)  # TECHNICAL, DESIGN, etc.
    score = Column(Float, nullable=False, index=True)
    confidence = Column(Float, nullable=False)

    # Metrics summary
    metrics_count = Column(Integer)
    strengths_count = Column(Integer)
    weaknesses_count = Column(Integer)

    # Metadata
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    __table_args__ = (
        Index("idx_path_assessment", "assessment_id", "path_type"),
        Index("idx_path_candidate", "candidate_id", "path_type"),
        Index("idx_path_score", "path_type", "score"),
    )

    def __repr__(self):
        return f"<PathScore(path={self.path_type}, score={self.score})>"


class ScoringMetric(Base):
    """Model for individual metrics within a path."""

    __tablename__ = "scoring_metrics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    assessment_id = Column(String(255), nullable=False, index=True)
    path_type = Column(String(50), nullable=False, index=True)
    metric_name = Column(String(255), nullable=False, index=True)
    score = Column(Float, nullable=False)
    weight = Column(Float, default=1.0)

    # Evidence
    evidence_count = Column(Integer, default=0)

    # Metadata
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    __table_args__ = (
        Index("idx_metric_assessment_path", "assessment_id", "path_type", "metric_name"),
        Index("idx_metric_name_score", "metric_name", "score"),
    )

    def __repr__(self):
        return f"<ScoringMetric(metric={self.metric_name}, score={self.score})>"


class MicroMotive(Base):
    """Model for Dark Horse micro-motive tracking."""

    __tablename__ = "micro_motives"

    id = Column(Integer, primary_key=True, autoincrement=True)
    assessment_id = Column(String(255), nullable=False, index=True)
    candidate_id = Column(String(255), nullable=False, index=True)
    motive_type = Column(String(50), nullable=False, index=True)  # MASTERY, EFFICIENCY, etc.
    strength = Column(Float, nullable=False, index=True)  # 0.0 to 1.0
    evidence_count = Column(Integer, default=0)

    # Metadata
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    __table_args__ = (
        Index("idx_motive_assessment", "assessment_id", "motive_type"),
        Index("idx_motive_candidate", "candidate_id", "motive_type"),
        Index("idx_motive_strength", "motive_type", "strength"),
    )

    def __repr__(self):
        return f"<MicroMotive(type={self.motive_type}, strength={self.strength})>"


class Candidate(Base):
    """Model for candidate information."""

    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    candidate_id = Column(String(255), nullable=False, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    last_assessment_at = Column(DateTime, index=True)

    # Statistics
    total_assessments = Column(Integer, default=0)
    average_score = Column(Float)
    highest_score = Column(Float)
    lowest_score = Column(Float)

    # Metadata
    metadata = Column(JSON)

    __table_args__ = (Index("idx_candidate_created", "created_at"),)

    def __repr__(self):
        return f"<Candidate(id={self.candidate_id}, assessments={self.total_assessments})>"
