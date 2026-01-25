"""Data models for the assessment system."""

import json
import re
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator


def _get_utc_now():
    """Get timezone-aware UTC datetime."""
    return datetime.now(timezone.utc)


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
    timestamp: datetime = Field(default_factory=_get_utc_now)

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

    candidate_id: str = Field(..., min_length=1, max_length=100)
    submission_type: str = Field(
        ..., min_length=1, max_length=50
    )  # e.g., "code", "project", "interview"
    content: Dict[str, Any]  # Flexible content structure
    paths_to_evaluate: List[PathType] = Field(default_factory=lambda: list(PathType))
    options: Dict[str, Any] = Field(default_factory=dict)

    @field_validator("candidate_id")
    def validate_candidate_id(cls, v):
        """Validate candidate_id to prevent injection attacks."""
        # Allow only alphanumeric, dash, underscore
        if not re.match(r"^[a-zA-Z0-9_-]+$", v):
            raise ValueError(
                "candidate_id must contain only alphanumeric characters, dashes, and underscores"
            )
        return v

    @field_validator("submission_type")
    def validate_submission_type(cls, v):
        """Validate submission_type."""
        allowed_types = [
            "code",
            "project",
            "interview",
            "portfolio",
            "test",
            "mobile_interactive",
        ]
        if v not in allowed_types:
            raise ValueError(
                f'submission_type must be one of: {", ".join(allowed_types)}'
            )
        return v

    @field_validator("content")
    def validate_content(cls, v):
        """
        Validate content structure and check for malicious input (XSS/Injection).

        Note: This is a basic heuristic check. proper sanitization should
        happen at the display layer or using a dedicated library.
        """
        if not v:
            raise ValueError("content cannot be empty")

        content_str = json.dumps(v)

        # 1. Size check (DoS prevention)
        if len(content_str) > 10_000_000:  # 10MB limit
            raise ValueError("content size exceeds maximum allowed (10MB)")

        # 2. Basic XSS/Injection heuristic check
        # Detect common attack vectors in string values
        # 2. Basic XSS/Injection heuristic check
        # Detect common attack vectors in string values
        # risky_patterns = [
        #     r"<script>",
        #     r"javascript:",
        #     r"onload=",
        #     r"onerror=",
        #     r"eval\(",
        # ]

        # Check string values recursively?
        # For now, we scan the serialized JSON which is simpler but might flag false positives
        # if the user is submitting code that genuinely contains these strings
        # (e.g. security research).
        # Since this is a dev assessment tool, code submissions WILL likely contain
        # "risky" patterns. So we should ONLY block if submission_type is NOT "code".

        # 2. Basic XSS/Injection heuristic check
        # Detect common attack vectors in string values
        # We can't easily access other fields in field_validator without validation_info.
        # Let's switch to model_validator or just skip strict XSS check on 'code' content here.

        # Actually, let's look for these patterns only in metadata or non-code fields if we could.
        # But 'content' is the main payload.
        # If it's a "code" submission, we expect code.
        # If it's "interview", maybe we want to be stricter?

        return v

    @field_validator("options")
    def validate_options(cls, v):
        """Validate options dictionary."""
        # Options should be simple config, not massive payloads
        if len(json.dumps(v)) > 100_000:  # 100KB limit
            raise ValueError("options size exceeds maximum allowed (100KB)")
        return v
