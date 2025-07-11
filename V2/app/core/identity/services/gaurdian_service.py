from uuid import UUID
from sqlalchemy.orm import Session
from V2.app.core.identity.models.guardian import Guardian
from V2.app.core.shared.services.audit_export_service.export import ExportService


class GuardianService:
    def __init__(self, session: Session, current_user = None):
        self.session = session
        self.current_user = current_user
        self.export_service = ExportService(session)


    def export_guardian(self, guardian_id: UUID, export_format: str) -> str:
        """Export guardian object and its associated data
        Args:
            guardian_id: Guardian UUID
            export_format: Preferred export format
        """
        return self.export_service.export_entity(
            Guardian, guardian_id, export_format
        )