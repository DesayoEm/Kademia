from sqlalchemy.orm import Session
from uuid import UUID
from V2.app.core.shared.services.export_service.export import ExportService
from V2.app.core.documents.models.documents import StudentAward, StudentDocument


class DocumentService:
    def __init__(self, session: Session, current_user=None):
        self.export_service = ExportService(session)
        self.current_user = current_user


    def export_award_audit(self, award_id: UUID, export_format: str) -> str:
        """Export award and its associated data
        Args:
            award_id: award UUID
            export_format: Preferred export format
        """
        return self.export_service.export_entity(
            StudentAward, award_id, export_format
        )


    def export_document_audit(self, document_id: UUID, export_format: str) -> str:
        """Export award and its associated data
        Args:
            document_id: document UUID
            export_format: Preferred export format
        """
        return self.export_service.export_entity(
            StudentDocument, document_id, export_format
        )
