from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib import colors
from typing import Dict, List
import io
from app.core.shared.services.pdf_service.reportlab_base import ReportLabService


class ResultPDF(ReportLabService):
    def __init__(self):
        super().__init__()

    @staticmethod
    def create_result_table(result_list: List[Dict]) -> Table:
        """Create the results table showing course scores and grades"""
        data = [['Course Code', 'Course Title', 'Total Score', 'Grade']]

        for result in result_list:
            data.append([
                result.get('course_code', ''),
                result.get('course_title', ''),
                result.get('total_score', ''),
                result.get('grading', '')
            ])

        table = Table(data, colWidths=[1.5 * inch, 3 * inch, 1.25 * inch, 1 * inch])

        table.setStyle(TableStyle([
            # Header styling
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),

            # Body styling
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),

            # Borders and grid
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

            # Padding
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))

        return table

    def render_pdf(self, data: Dict, filename: str) -> tuple:
        """
        Generate PDF for student results

        Args:
            data: Dictionary containing student results
            filename: Base filename for the PDF

        Returns:
            tuple: (pdf_bytes, sanitized_filename)
        """
        pdf_buffer = io.BytesIO()

        doc = SimpleDocTemplate(
            pdf_buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )

        story = []

        title = Paragraph("Student Result Report", self.styles['CustomTitle'])
        story.append(title)

        subtitle_text = f"{data.get('student_name', 'Unknown Student')} - {data.get('academic_session', '')} ({data.get('term', '')})"
        subtitle = Paragraph(subtitle_text, self.styles['CustomSubtitle'])
        story.append(subtitle)

        if data.get('result_list'):
            result_table = self.create_result_table(data['result_list'])
            story.append(result_table)
        else:
            no_results = Paragraph("No results available for this term.", self.styles['Normal'])
            story.append(no_results)

        footer_text = f"<b>Date Generated:</b> {data.get('date_generated', '')}"
        footer = Paragraph(footer_text, self.styles['Footer'])
        story.append(footer)

        doc.build(story)

        pdf_buffer.seek(0)
        pdf_bytes = pdf_buffer.read()
        clean_filename = self.slugify_filename(f"{filename}.pdf")

        return pdf_bytes, clean_filename
