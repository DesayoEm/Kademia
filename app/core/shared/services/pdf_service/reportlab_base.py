from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import re


class ReportLabService:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()

    def setup_custom_styles(self):
        """Create custom styles for our document"""
        # Title style
        self.styles.add(
            ParagraphStyle(
                name="CustomTitle",
                parent=self.styles["Title"],
                fontSize=18,
                spaceAfter=12,
                alignment=TA_CENTER,
                textColor=colors.black,
            )
        )

        # Subtitle style
        self.styles.add(
            ParagraphStyle(
                name="CustomSubtitle",
                parent=self.styles["Normal"],
                fontSize=14,
                spaceAfter=20,
                alignment=TA_CENTER,
                textColor=colors.black,
            )
        )

        # Footer style
        self.styles.add(
            ParagraphStyle(
                name="Footer",
                parent=self.styles["Normal"],
                fontSize=10,
                spaceBefore=30,
                alignment=TA_CENTER,
                textColor=colors.grey,
            )
        )

    @staticmethod
    def slugify_filename(name: str) -> str:
        """Clean up filename for safe file saving"""
        return re.sub(r"[^\w\-_.]", "_", name)
