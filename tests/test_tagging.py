"""Tests for the tagging system."""

from sono_eval.tagging.generator import SemanticTag, TagGenerator


def test_tag_generator_initialization():
    """Test that tag generator initializes correctly."""
    generator = TagGenerator()
    assert generator is not None
    assert generator.model_name is not None


def test_generate_tags_basic():
    """Test basic tag generation."""
    generator = TagGenerator()

    code = """
    def calculate_sum(numbers):
        return sum(numbers)
    """

    tags = generator.generate_tags(code, max_tags=5)

    assert isinstance(tags, list)
    assert len(tags) <= 5
    assert all(isinstance(tag, SemanticTag) for tag in tags)


def test_generate_tags_python_code():
    """Test tag generation for Python code."""
    generator = TagGenerator()

    code = """
    class Calculator:
        def add(self, a, b):
            return a + b
    """

    tags = generator.generate_tags(code)

    assert len(tags) > 0
    # Should detect Python-related tags
    tag_names = [t.tag.lower() for t in tags]
    assert any("python" in name or "class" in name for name in tag_names)


def test_generate_tags_with_confidence():
    """Test that tags have confidence scores."""
    generator = TagGenerator()

    code = "async function fetchData() { await api.call(); }"

    tags = generator.generate_tags(code)

    for tag in tags:
        assert tag.confidence >= 0.0
        assert tag.confidence <= 1.0


def test_generate_tags_with_categories():
    """Test that tags have categories."""
    generator = TagGenerator()

    code = "def test_function(): pass"

    tags = generator.generate_tags(code)

    for tag in tags:
        assert tag.category is not None
        assert len(tag.category) > 0


def test_batch_generate_tags():
    """Test batch tag generation."""
    generator = TagGenerator()

    texts = [
        "def hello(): pass",
        "class MyClass: pass",
        "import numpy as np",
    ]

    results = generator.batch_generate_tags(texts)

    assert len(results) == len(texts)
    assert all(isinstance(tags, list) for tags in results)


def test_fallback_tagging():
    """Test fallback tagging when model is not available."""
    generator = TagGenerator()

    # This should use fallback even if model loads
    code = "function test() { console.log('test'); }"

    tags = generator._fallback_tagging(code, max_tags=3)

    assert len(tags) <= 3
    assert all(isinstance(tag, SemanticTag) for tag in tags)


def test_tag_confidence_threshold():
    """Test filtering by confidence threshold."""
    generator = TagGenerator()

    code = "print('hello world')"

    tags = generator.generate_tags(code, min_confidence=0.7)

    # All tags should meet threshold
    assert all(tag.confidence >= 0.7 for tag in tags)


def test_infer_category():
    """Test category inference."""
    generator = TagGenerator()

    assert generator._infer_category("python") == "language"
    assert generator._infer_category("testing") == "quality"
    assert generator._infer_category("api") == "architecture"
    assert generator._infer_category("design-pattern") == "pattern"
    assert generator._infer_category("optimization") == "performance"
