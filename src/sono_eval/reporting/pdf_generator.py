"""PDF Report Generator for Assessment Results."""

from datetime import datetime
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from sono_eval.assessment.models import AssessmentResult


class PDFGenerator:
    """Generates PDF reports for assessment results."""

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_styles()

    def _setup_styles(self):
        """Define custom styles."""
        self.styles.add(
            ParagraphStyle(
                name="Header1",
                parent=self.styles["Heading1"],
                fontSize=24,
                spaceAfter=20,
                textColor=colors.HexColor("#1a365d"),
            )
        )
        self.styles.add(
            ParagraphStyle(
                name="SectionHeader",
                parent=self.styles["Heading2"],
                fontSize=18,
                spaceBefore=15,
                spaceAfter=10,
                textColor=colors.HexColor("#2d3748"),
            )
        )
        self.styles.add(
            ParagraphStyle(
                name="ScoreText",
                parent=self.styles["Normal"],
                fontSize=36,
                alignment=1,  # Center
                textColor=colors.HexColor("#2b6cb0"),
            )
        )

    def generate(self, result: AssessmentResult) -> bytes:
        """
        Generate PDF report from assessment result.

        Args:
            result: AssessmentResult object

        Returns:
            bytes: PDF file content
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72,
        )

        elements = []

        # Header
        # Header
        elements.append(
            Paragraph(
                f"Assessment Report: {result.candidate_id}", self.styles["Header1"]
            )
        )
        elements.append(
            Paragraph(
                f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                self.styles["Normal"],
            )
        )
        elements.append(Spacer(1, 0.5 * inch))

        # Overall Score
        elements.append(Paragraph("Overall Score", self.styles["SectionHeader"]))
        elements.append(
            Paragraph(f"{result.overall_score:.1f}/100", self.styles["ScoreText"])
        )
        elements.append(Spacer(1, 0.2 * inch))

        # Executive Summary
        elements.append(Paragraph("Executive Summary", self.styles["SectionHeader"]))
        elements.append(Paragraph(result.summary, self.styles["Normal"]))
        elements.append(Spacer(1, 0.2 * inch))

        # Key Findings
        if result.key_findings:
            elements.append(Paragraph("Key Findings", self.styles["SectionHeader"]))
            for finding in result.key_findings:
                elements.append(Paragraph(f"• {finding}", self.styles["Normal"]))
                elements.append(Spacer(1, 0.05 * inch))

        # Path Scores Table
        if result.path_scores:
            elements.append(
                Paragraph("Detailed Path Analysis", self.styles["SectionHeader"])
            )
            data = [["Path", "Score", "Status"]]
            for path_score in result.path_scores:
                status = (
                    "Excellent"
                    if path_score.overall_score >= 90
                    else (
                        "Good"
                        if path_score.overall_score >= 70
                        else (
                            "Fair"
                            if path_score.overall_score >= 50
                            else "Needs Improvement"
                        )
                    )
                )
                data.append(
                    [path_score.path.title(), f"{path_score.overall_score:.1f}", status]
                )

            table = Table(data, colWidths=[3 * inch, 1.5 * inch, 2 * inch])
            table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#2d3748")),
                        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, 0), 12),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                        ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                        ("TEXTCOLOR", (0, 1), (-1, -1), colors.black),
                        ("GRID", (0, 0), (-1, -1), 1, colors.HexColor("#e2e8f0")),
                    ]
                )
            )
            elements.append(table)

        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        return buffer.getvalue()
