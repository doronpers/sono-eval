"""
Sono-Eval: Explainable Multi-Path Developer Assessment System

A comprehensive system for evaluating developer skills with:
- Explainable, evidence-based scoring
- Multi-path micro-motive tracking
- Semantic tagging with T5 + PEFT
- Persistent hierarchical memory
- Analytics and visualization
"""

__version__ = "0.1.0"
__author__ = "Sono-Eval Team"

from sono_eval.assessment.engine import AssessmentEngine
from sono_eval.memory.memu import MemUStorage
from sono_eval.tagging.generator import TagGenerator

__all__ = [
    "AssessmentEngine",
    "MemUStorage",
    "TagGenerator",
]
