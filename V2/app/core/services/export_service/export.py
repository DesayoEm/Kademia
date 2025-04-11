from fpdf import FPDF
import os
from uuid import uuid4

EXPORT_DIR = "exports"
from uuid import UUID

from ....database.models import *
from .gather_data import GatherData
from ...errors.database_errors import EntityNotFoundError
from ...errors.staff_organisation_errors import RoleNotFoundError


class ExportService:
    def __init__(self, session):
        self.session = session
        self.gatherer = GatherData()

    def export_entity(
            self,
            entity_model,
            entity_id: UUID,
            export_format: str
    ) -> str:
        """
        Export an entity and its related data.

        Args:
            entity_model: Base SQLAlchemy model of the entity.
            entity_id (UUID): ID of the entity.
            export_format (str): Export format ("pdf", "csv", "excel").

        Returns:
            str: Path to the exported file.
        """
        error_map = {
            StaffRole: (RoleNotFoundError, "Role")
        }

        entity = self.session.get(entity_model, entity_id)

        if not entity:
            error_info = error_map.get(entity_model)

            if error_info:
                error_class, display_name = error_info
                raise error_class(identifier=entity_id, detail=f"{display_name} not found.")
            else:
                raise EntityNotFoundError(
                    entity_type=entity_model.__name__,
                    identifier=str(entity_id),
                    error="Object not found."
                )

        data = self.gatherer.gather(entity)

        if export_format == "pdf":
            return self.export_to_pdf(data)
        elif export_format == "csv":
            return self.export_to_csv(data)
        elif export_format == "excel":
            return self.export_to_excel(data)
        else:
            raise ValueError(f"Unsupported export export_format: {export_format}")



    def export_to_pdf(self, data: dict) -> str:
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)


        self.write_dict_to_pdf(pdf, data)


        os.makedirs(EXPORT_DIR, exist_ok=True)

        filename = f"{EXPORT_DIR}/export_{uuid4()}.pdf"
        pdf.output(filename)

        return filename


    def write_dict_to_pdf(self, pdf, data: dict, indent=0):
        """Recursively write a dictionary into the PDF."""
        for key, value in data.items():
            if isinstance(value, dict):
                pdf.cell(0, 10, f"{' ' * indent}{key}:", ln=True)
                self.write_dict_to_pdf(pdf, value, indent + 2)
            elif isinstance(value, list):
                pdf.cell(0, 10, f"{' ' * indent}{key}:", ln=True)
                for item in value:
                    if isinstance(item, dict):
                        self.write_dict_to_pdf(pdf, item, indent + 4)
                    else:
                        pdf.cell(0, 10, f"{' ' * (indent + 4)}- {item}", ln=True)
            else:
                pdf.cell(0, 10, f"{' ' * indent}{key}: {value}", ln=True)


    def export_to_csv(self, data) -> str:
        pass

    def export_to_excel(self, entity) -> str:
        pass