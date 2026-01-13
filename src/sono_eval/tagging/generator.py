"""
T5 + PEFT (LoRA) Tag Generator for semantic code tagging.

Uses T5 model with LoRA fine-tuning for generating semantic tags.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from sono_eval.utils.config import get_config
from sono_eval.utils.logger import get_logger

logger = get_logger(__name__)


class SemanticTag(BaseModel):
    """Semantic tag for code or assessment artifact."""

    tag: str
    category: str
    confidence: float = Field(ge=0.0, le=1.0)
    context: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class TagGenerator:
    """
    T5-based semantic tag generator with LoRA fine-tuning support.

    Features:
    - T5 model for tag generation
    - PEFT LoRA for efficient fine-tuning
    - Semantic understanding of code
    - Configurable generation parameters
    """

    def __init__(self, model_name: Optional[str] = None):
        """Initialize the tag generator."""
        self.config = get_config()
        self.model_name = model_name or self.config.t5_model_name
        self.cache_dir = self.config.get_cache_dir()
        self.lora_config = {
            "r": self.config.t5_lora_rank,
            "lora_alpha": self.config.t5_lora_alpha,
            "lora_dropout": self.config.t5_lora_dropout,
        }

        self.model = None
        self.tokenizer = None
        self._initialized = False

        logger.info(f"Initializing TagGenerator with model: {self.model_name}")

    def initialize(self) -> None:
        """
        Lazy initialization of the model.

        This allows the class to be instantiated without loading the model
        until it's actually needed.
        """
        if self._initialized:
            return

        try:
            from transformers import T5ForConditionalGeneration, T5Tokenizer
            from peft import LoraConfig, get_peft_model

            logger.info(f"Loading T5 model: {self.model_name}")

            # Load tokenizer
            self.tokenizer = T5Tokenizer.from_pretrained(
                self.model_name,
                cache_dir=str(self.cache_dir),
            )

            # Load base model
            base_model = T5ForConditionalGeneration.from_pretrained(
                self.model_name,
                cache_dir=str(self.cache_dir),
            )

            # Apply LoRA
            lora_config = LoraConfig(
                r=self.lora_config["r"],
                lora_alpha=self.lora_config["lora_alpha"],
                lora_dropout=self.lora_config["lora_dropout"],
                target_modules=["q", "v"],
                task_type="SEQ_2_SEQ_LM",
            )

            self.model = get_peft_model(base_model, lora_config)
            self.model.eval()

            self._initialized = True
            logger.info("Model initialization complete")

        except ImportError as e:
            logger.warning(
                f"Model dependencies not available: {e}. " "Tag generator will use fallback mode."
            )
            self._initialized = False
        except Exception as e:
            logger.error(f"Error initializing model: {e}")
            self._initialized = False

    def generate_tags(
        self,
        text: str,
        max_tags: int = 5,
        min_confidence: float = 0.5,
    ) -> List[SemanticTag]:
        """
        Generate semantic tags for text.

        Args:
            text: Input text (code or content)
            max_tags: Maximum number of tags to generate
            min_confidence: Minimum confidence threshold

        Returns:
            List of semantic tags
        """
        if not self._initialized:
            # Use fallback heuristic tagging
            return self._fallback_tagging(text, max_tags)

        try:
            # Prepare input
            prompt = f"generate tags: {text[:500]}"  # Limit input length
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                max_length=512,
                truncation=True,
            )

            # Generate
            outputs = self.model.generate(
                **inputs,
                max_length=50,
                num_return_sequences=max_tags,
                num_beams=max_tags,
                early_stopping=True,
            )

            # Decode
            tags = []
            for output in outputs:
                tag_text = self.tokenizer.decode(output, skip_special_tokens=True)
                if tag_text:
                    tags.append(
                        SemanticTag(
                            tag=tag_text,
                            category=self._infer_category(tag_text),
                            confidence=0.8,  # Could be improved with model confidence
                            context=text[:100],
                        )
                    )

            # Filter by confidence
            tags = [t for t in tags if t.confidence >= min_confidence]
            return tags[:max_tags]

        except Exception as e:
            logger.error(f"Error generating tags: {e}")
            return self._fallback_tagging(text, max_tags)

    def _fallback_tagging(self, text: str, max_tags: int) -> List[SemanticTag]:
        """
        Fallback heuristic tagging when model is not available.

        Args:
            text: Input text
            max_tags: Maximum tags to generate

        Returns:
            List of heuristically generated tags
        """
        tags = []
        text_lower = text.lower()

        # Simple keyword-based tagging
        keyword_map = {
            "python": ("python", "language"),
            "javascript": ("javascript", "language"),
            "java": ("java", "language"),
            "class": ("object-oriented", "pattern"),
            "function": ("functional", "pattern"),
            "async": ("asynchronous", "pattern"),
            "test": ("testing", "quality"),
            "api": ("api", "architecture"),
            "database": ("database", "architecture"),
            "import": ("dependencies", "structure"),
            "error": ("error-handling", "quality"),
            "optimize": ("optimization", "performance"),
        }

        for keyword, (tag, category) in keyword_map.items():
            if keyword in text_lower and len(tags) < max_tags:
                tags.append(
                    SemanticTag(
                        tag=tag,
                        category=category,
                        confidence=0.6,
                        context=text[:100],
                    )
                )

        # Add generic tag if nothing found
        if not tags:
            tags.append(
                SemanticTag(
                    tag="code",
                    category="general",
                    confidence=0.5,
                )
            )

        return tags[:max_tags]

    def _infer_category(self, tag: str) -> str:
        """Infer category from tag text."""
        category_keywords = {
            "language": ["python", "java", "javascript", "c++", "go"],
            "pattern": ["design", "architecture", "oop", "functional"],
            "quality": ["testing", "clean", "maintainable"],
            "architecture": ["api", "database", "microservice"],
            "performance": ["optimization", "efficient", "fast"],
        }

        tag_lower = tag.lower()
        for category, keywords in category_keywords.items():
            if any(kw in tag_lower for kw in keywords):
                return category

        return "general"

    def batch_generate_tags(
        self,
        texts: List[str],
        max_tags: int = 5,
        min_confidence: float = 0.5,
    ) -> List[List[SemanticTag]]:
        """
        Generate tags for multiple texts.

        Args:
            texts: List of input texts
            max_tags: Maximum tags per text
            min_confidence: Minimum confidence threshold

        Returns:
            List of tag lists
        """
        results = []
        for text in texts:
            tags = self.generate_tags(text, max_tags, min_confidence)
            results.append(tags)
        return results

    def fine_tune(
        self,
        training_data: List[Dict[str, Any]],
        epochs: int = 3,
        batch_size: int = 8,
    ) -> None:
        """
        Fine-tune the model on custom data.

        Args:
            training_data: Training examples
            epochs: Number of training epochs
            batch_size: Training batch size
        """
        if not self._initialized:
            self.initialize()

        if not self._initialized:
            logger.error("Cannot fine-tune: model not initialized")
            return

        logger.info(f"Starting fine-tuning with {len(training_data)} examples")

        # This is a placeholder for fine-tuning logic
        # In production, would implement full training loop
        logger.warning("Fine-tuning not fully implemented in this version")
