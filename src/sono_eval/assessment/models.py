"""Data models for the assessment system."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class MotiveType(str, Enum):
    """Types of micro-motives in the Dark Horse model."""
    EXPLORATION = "exploration"
    MASTERY = "mastery"
    COLLABORATION = "collaboration"
    INNOVATION = "innovation"
    EFFICIENCY = "efficiency"
    QUALITY = "quality"


class PathType(str, Enum):
    """Different assessment paths."""
    TECHNICAL = "technical"
    DESIGN = "design"
    COLLABORATION = "collaboration"
    PROBLEM_SOLVING = "problem_solving"
    COMMUNICATION = "communication"


class EvidenceType(str, Enum):
    """Types of evidence for scoring."""
    CODE_QUALITY = "code_quality"
    DOCUMENTATION = "documentation"
    TESTING = "testing"
    ARCHITECTURE = "architecture"
    COLLABORATION = "collaboration"
    COMMUNICATION = "communication"


class Evidence(BaseModel):
    """Evidence supporting a score."""
    type: EvidenceType
    description: str
    source: str  # File path, line number, or reference
    weight: float = Field(ge=0.0, le=1.0)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class MicroMotive(BaseModel):
    """Micro-motive tracking for Dark Horse model."""
    motive_type: MotiveType
    strength: float = Field(ge=0.0, le=1.0)
    indicators: List[str] = Field(default_factory=list)
    evidence: List[Evidence] = Field(default_factory=list)
    path_alignment: PathType


class ScoringMetric(BaseModel):
    """Individual scoring metric with explainability."""
    name: str
    category: str
    score: float = Field(ge=0.0, le=100.0)
    weight: float = Field(ge=0.0, le=1.0)
    evidence: List[Evidence] = Field(default_factory=list)
    explanation: str
    confidence: float = Field(ge=0.0, le=1.0, default=0.8)


class PathScore(BaseModel):
    """Score for a specific assessment path."""
    path: PathType
    overall_score: float = Field(ge=0.0, le=100.0)
    metrics: List[ScoringMetric] = Field(default_factory=list)
    motives: List[MicroMotive] = Field(default_factory=list)
    strengths: List[str] = Field(default_factory=list)
    areas_for_improvement: List[str] = Field(default_factory=list)


class AssessmentResult(BaseModel):
    """Complete assessment result with explainability."""
    candidate_id: str
    assessment_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    # Overall scores
    overall_score: float = Field(ge=0.0, le=100.0)
    confidence: float = Field(ge=0.0, le=1.0)
    
    # Multi-path scores
    path_scores: List[PathScore] = Field(default_factory=list)
    
    # Dark Horse tracking
    micro_motives: List[MicroMotive] = Field(default_factory=list)
    dominant_path: Optional[PathType] = None
    
    # Explainability
    summary: str
    key_findings: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    
    # Metadata
    engine_version: str = "1.0"
    processing_time_ms: Optional[float] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AssessmentInput(BaseModel):
    """Input for assessment."""
    candidate_id: str
    submission_type: str  # e.g., "code", "project", "interview"
    content: Dict[str, Any]  # Flexible content structure
    paths_to_evaluate: List[PathType] = Field(
        default_factory=lambda: list(PathType)
    )
    options: Dict[str, Any] = Field(default_factory=dict)
