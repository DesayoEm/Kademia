from typing import Dict
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import os


class JinjaService:
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader("templates"))

    def render_pdf(self, data: Dict, template_name: str, output_path: str):
        template = self.env.get_template(f"{template_name}.html")

        html_out = template.render(**data)

        HTML(string=html_out).write_pdf(output_path)

        return output_path