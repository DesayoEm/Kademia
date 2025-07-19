from uuid import UUID
from sqlalchemy.orm import Session
from app.core.shared.models.enums import AccessLevel
from app.core.shared.services.audit_export_service.export import ExportService


class AccessLevelService:
    def __init__(self, session: Session, current_user):
        self.session = session
        self.current_user = current_user
        self.export_service = ExportService(session)

    def export_access_level_change(self, level_change_id: UUID, export_format: str) -> str:
        """Export level change object and its associated data
        Args:
            level_change_id: level change UUID
            export_format: Preferred export format
        """
        return self.export_service.export_entity(
            AccessLevel, level_change_id, export_format
        )