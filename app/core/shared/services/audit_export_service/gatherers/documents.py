from typing import Dict, Tuple, Any
from app.core.documents.models.documents import StudentDocument, StudentAward

class DocumentsGatherer:
    """Gathers data for assessment entities"""

    @staticmethod
    def gather_student_document_data(doc: StudentDocument) -> Tuple[Dict[str, Any], str]:
        """Gather data for StudentDocument entity."""
        file_name = f"StudentDocument_{doc.student_id}_{doc.document_type}_{doc.academic_session}"

        return ({
                    "document": {
                        "id": str(doc.id),
                        "student_id": str(doc.student_id),
                        "title": doc.title,
                        "academic_session": doc.academic_session,
                        "document_type": doc.document_type,
                        "file_url": doc.document_s3_key,
                        "created_at": doc.created_at,
                        "created_by": str(doc.created_by) if doc.created_by else None,
                        "last_modified_at": doc.last_modified_at,
                        "last_modified_by": str(doc.last_modified_by) if doc.last_modified_by else None,
                        "archived_at": doc.archived_at,
                        "archived_by": str(doc.archived_by) if doc.archived_by else None,
                        "archive_reason": doc.archive_reason,
                    },
                    "student": {
                        "id": str(doc.owner.id),
                        "name": f"{doc.owner.first_name} {doc.owner.last_name}"
                    } if doc.owner else None
                }, file_name)

    @staticmethod
    def gather_student_award_data(award: StudentAward) -> Tuple[Dict[str, Any], str]:
        """Gather data for StudentAward entity."""
        file_name = f"StudentAward_{award.student_id}_{award.academic_session}_{award.title}"

        return ({
                    "award": {
                        "id": str(award.id),
                        "student_id": str(award.student_id),
                        "title": award.title,
                        "description": award.description,
                        "academic_session": award.academic_session,
                        "file_url": award.award_s3_key,
                        "created_at": award.created_at,
                        "created_by": str(award.created_by) if award.created_by else None,
                        "last_modified_at": award.last_modified_at,
                        "last_modified_by": str(award.last_modified_by) if award.last_modified_by else None,
                        "archived_at": award.archived_at,
                        "archived_by": str(award.archived_by) if award.archived_by else None,
                        "archive_reason": award.archive_reason,
                    },
                    "student": {
                        "id": str(award.owner.id),
                        "name": f"{award.owner.first_name} {award.owner.last_name}"
                    } if award.owner else None
                }, file_name)

