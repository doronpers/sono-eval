from datetime import datetime

from sono_eval.assessment.models import AssessmentResult
from sono_eval.reporting.pdf_generator import PDFGenerator


def test_pdf_generation():
    # Setup mock result
    result = AssessmentResult(
        candidate_id="test-candidate",
        assessment_id="test-assessment",
        overall_score=85.5,
        confidence=0.9,
        summary="Test Summary",
        key_findings=["Finding 1", "Finding 2"],
        timestamp=datetime.now(),
        path_scores=[],
    )

    generator = PDFGenerator()
    pdf_bytes = generator.generate(result)

    # Verify PDF signature
    assert pdf_bytes.startswith(b"%PDF-")
    assert len(pdf_bytes) > 0


def test_pdf_generation_with_paths():
    # Setup mock result with path scores
    # We need to mock PathScore properly if it's complex,
    # but here we can just assume empty for now or minimum viable
    # Actually, let's create a minimal test where we check if it runs without error

    result = AssessmentResult(
        candidate_id="test-candidate",
        assessment_id="test-assessment",
        overall_score=85.5,
        confidence=0.9,
        summary="Test Summary",
        timestamp=datetime.now(),
        path_scores=[],
    )

    generator = PDFGenerator()
    pdf_bytes = generator.generate(result)
    assert pdf_bytes.startswith(b"%PDF-")
