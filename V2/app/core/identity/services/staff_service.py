from uuid import UUID
from sqlalchemy.orm import Session

from V2.app.core.identity.models.staff import Staff
from V2.app.core.shared.services.export_service.export import ExportService


class StaffService:
    def __init__(self, session: Session, current_user = None):
        self.session = session
        self.current_user = current_user
        self.export_service = ExportService(session)


    def export_staff(self, staff_id: UUID, export_format: str) -> str:
        """Export staff object and its associated data
        Args:
            staff_id: Staff UUID
            export_format: Preferred export format
        """
        return self.export_service.export_entity(
            Staff, staff_id, export_format
        )