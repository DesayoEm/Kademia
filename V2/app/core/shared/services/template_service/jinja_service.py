from typing import Dict
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import io
import re


class JinjaService:
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader("templates"))



    @staticmethod
    def slugify_filename(name: str) -> str:
        return re.sub(r'[^\w\-_.]', '_', name)


    def render_pdf(self, data: Dict, template_name: str, filename: str):
        template = self.env.get_template(f"{template_name}.html")

        html_out = template.render(**data)
        pdf_io = io.BytesIO()
        HTML(string=html_out).write_pdf(pdf_io)

        filename = self.slugify_filename(f"{filename}.pdf")
        pdf_io.seek(0)
        return pdf_io.read(), filename