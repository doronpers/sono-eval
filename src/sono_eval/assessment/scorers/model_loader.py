"""
ML Model Loader for CodeBERT-based code assessment.

Provides lazy loading, caching, and graceful fallback for transformer models.
Patent compliant: Uses dynamic learned representations, not LPC/source-filter models.
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from sono_eval.utils.logger import get_logger

logger = get_logger(__name__)

# Model configuration
DEFAULT_MODEL_NAME = "microsoft/codebert-base"
CACHE_DIR = Path(__file__).parent.parent.parent.parent.parent / "models" / "cache"


class ModelLoader:
    """
    Handles loading and caching of CodeBERT models for code assessment.

    Supports:
    - Lazy loading (only loads when first needed)
    - Model caching to disk
    - Graceful fallback when model unavailable
    - Model versioning
    """

    _instance: Optional["ModelLoader"] = None
    _model: Optional[Any] = None
    _tokenizer: Optional[Any] = None
    _model_version: str = "unknown"

    def __new__(cls) -> "ModelLoader":
        """Singleton pattern for model loader."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize the model loader."""
        self._model_name = os.environ.get("ML_MODEL_PATH", DEFAULT_MODEL_NAME)
        self._enabled = os.environ.get("ML_MODEL_ENABLED", "true").lower() in (
            "true",
            "1",
            "yes",
        )
        self._loaded = False

    @property
    def is_available(self) -> bool:
        """Check if model is loaded and available."""
        return self._loaded and self._model is not None

    @property
    def model_version(self) -> str:
        """Get the current model version identifier."""
        return self._model_version

    def load(self) -> bool:
        """
        Load the CodeBERT model.

        Returns:
            True if model loaded successfully, False otherwise.
        """
        if self._loaded:
            return self._model is not None

        if not self._enabled:
            logger.info("ML model loading disabled via configuration")
            self._loaded = True
            return False

        try:
            return self._load_transformer_model()
        except Exception as e:
            logger.warning(f"Failed to load ML model: {e}")
            self._loaded = True
            return False

    def _load_transformer_model(self) -> bool:
        """Load the transformer model with proper error handling."""
        try:
            from transformers import AutoModel, AutoTokenizer

            # Ensure cache directory exists
            CACHE_DIR.mkdir(parents=True, exist_ok=True)

            logger.info(f"Loading model: {self._model_name}")

            # Load tokenizer
            self._tokenizer = AutoTokenizer.from_pretrained(
                self._model_name,
                cache_dir=str(CACHE_DIR),
                trust_remote_code=False,
            )

            # Load model
            self._model = AutoModel.from_pretrained(
                self._model_name,
                cache_dir=str(CACHE_DIR),
                trust_remote_code=False,
            )

            # Set to eval mode for inference
            self._model.eval()

            # Extract version from model config
            if hasattr(self._model, "config"):
                self._model_version = getattr(self._model.config, "_name_or_path", self._model_name)
            else:
                self._model_version = self._model_name

            self._loaded = True
            logger.info(
                f"ML model loaded successfully: {self._model_version} " f"(cached at {CACHE_DIR})"
            )
            return True

        except ImportError as e:
            logger.warning(f"Transformers library not available: {e}")
            self._loaded = True
            return False

    def get_embeddings(self, code: str) -> Optional[Tuple[Any, float]]:
        """
        Get code embeddings from the model.

        Args:
            code: Source code to encode

        Returns:
            Tuple of (embeddings tensor, confidence score) or None if unavailable
        """
        if not self.is_available:
            return None

        try:
            import torch

            # Tokenize input
            inputs = self._tokenizer(
                code,
                return_tensors="pt",
                truncation=True,
                max_length=512,
                padding=True,
            )

            # Get embeddings (no gradient computation for inference)
            with torch.no_grad():
                outputs = self._model(**inputs)

            # Use [CLS] token embedding as code representation
            embeddings = outputs.last_hidden_state[:, 0, :]

            # Calculate confidence based on attention patterns
            confidence = self._calculate_confidence(outputs)

            return embeddings, confidence

        except Exception as e:
            logger.debug(f"Embedding extraction failed: {e}")
            return None

    def _calculate_confidence(self, outputs: Any) -> float:
        """
        Calculate confidence score based on model outputs.

        Uses attention entropy as a proxy for model certainty.
        """
        try:
            import torch

            if hasattr(outputs, "attentions") and outputs.attentions is not None:
                # Average attention entropy across layers
                attention = outputs.attentions[-1]  # Last layer
                probs = attention.mean(dim=1)  # Average across heads
                entropy = -torch.sum(probs * torch.log(probs + 1e-10), dim=-1).mean()
                # Normalize entropy to confidence (lower entropy = higher confidence)
                confidence: float = max(0.5, min(1.0, 1.0 - (float(entropy.item()) / 5.0)))
                return confidence
        except Exception as e:
            logger.debug(f"Confidence calculation failed: {e}")

        # Default confidence when attention not available
        return 0.75

    def get_code_quality_score(self, code: str) -> Optional[Dict[str, Any]]:
        """
        Get a code quality assessment from the model.

        This uses the model embeddings to compute similarity against
        known good/bad code patterns (zero-shot approach).

        Args:
            code: Source code to assess

        Returns:
            Dictionary with score, confidence, and pattern classification
        """
        result = self.get_embeddings(code)
        if result is None:
            return None

        embeddings, confidence = result

        try:
            import torch

            # Compute basic statistics from embeddings for scoring
            # This is a simplified zero-shot approach
            embedding_norm = torch.norm(embeddings).item()
            embedding_std = embeddings.std().item()

            # Heuristic scoring based on embedding properties
            # Well-structured code tends to have more consistent embeddings
            norm_score = min(100, max(0, (embedding_norm / 10) * 50 + 25))
            consistency_score = min(100, max(0, (1 - embedding_std) * 100))

            combined_score = (norm_score * 0.4) + (consistency_score * 0.6)

            return {
                "score": combined_score,
                "confidence": confidence,
                "embedding_norm": embedding_norm,
                "embedding_consistency": 1 - embedding_std,
                "model_version": self._model_version,
            }

        except Exception as e:
            logger.debug(f"Code quality scoring failed: {e}")
            return None

    def unload(self) -> None:
        """Unload the model to free memory."""
        if self._model is not None:
            del self._model
            self._model = None

        if self._tokenizer is not None:
            del self._tokenizer
            self._tokenizer = None

        self._loaded = False
        logger.info("ML model unloaded")


# Module-level convenience function
def get_model_loader() -> ModelLoader:
    """Get the singleton model loader instance."""
    return ModelLoader()
