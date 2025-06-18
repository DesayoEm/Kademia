from sqlalchemy.orm import Session
from uuid import UUID
from V2.app.core.curriculum.models.curriculum import Subject
from V2.app.core.shared.services.export_service.export import ExportService


class CurriculumService:
    def __init__(self, session: Session, current_user):
        self.session = session
        self.current_user = current_user
        self.export_service = ExportService(self.session)


    def export_subject_audit(self, subject_id: UUID, export_format: str) -> str:
        """Export subject and its associated data
        Args:
            subject_id: subject UUID
            export_format: Preferred export format
        """
        return self.export_service.export_entity(
            Subject, subject_id, export_format
        )


    def export_level_subject_audit(self, level_subject_id: UUID, export_format: str) -> str:
        """Export level subject and its associated data
        Args:
            level_subject_id: subject UUID
            export_format: Preferred export format
        """
        return self.export_service.export_entity(
            Subject, level_subject_id, export_format
        )


