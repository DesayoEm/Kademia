
from uuid import UUID, uuid4
import magic
from sqlalchemy.orm import Session

from V2.app.core.identity.models.student import Student
from V2.app.core.shared.services.file_storage.s3_upload import S3Upload
from V2.app.infra.log_service.logger import logger
from V2.app.infra.settings import config

from V2.app.core.shared.services.audit_export_service.export import ExportService
from V2.app.core.documents.models.documents import StudentAward, StudentDocument


class DocumentService:
    def __init__(self, session: Session, current_user):
        self.session = session
        self.current_user = current_user
        self.upload = S3Upload(session, self.current_user)
        self.export_service = ExportService(session)

        self.SUPPORTED_DOCUMENT_TYPES = {
            'image/png': 'png',
            'image/jpeg': 'jpg',
            'image/jpg': 'jpg',
            'image/webp': 'webp',
            'application/pdf': 'pdf',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx',
            'application/msword': 'doc'
        }

        self.MIN_FILE_SIZE = 1 * self.upload.KB
        self.MAX_FILE_SIZE = 10 * self.upload.MB

    @staticmethod
    def generate_doc_key(
            student: Student, doc_type: str,  s3_folder: str, file_extension: str
    ) -> str:
        """
        Generate a unique filename for the uploaded file.
        Args:
            student: Student object
            s3_folder: S3 folder path (e.g., "student-documents/")
            doc_type: Type of document being stored
            file_extension: File extension
        Returns:
            str: Unique filename
        """

        unique_id = str(uuid4())[:8]

        first_name = student.first_name
        last_name = student.last_name


        return f"{s3_folder}{doc_type}_{first_name}_{last_name}_{unique_id}.{file_extension}"


    def upload_award_file(self, file, student: Student, award: StudentAward):
        """
        Upload and validate a document for a student.
        Args:
            file: The uploaded file
            student: Student object
            award: StudentAward object
        Returns:
            dict: Upload result with success status and file info
        """
        try:
            contents = self.upload.validate_file_upload(
                file, self.MIN_FILE_SIZE, self.MAX_FILE_SIZE, self.SUPPORTED_DOCUMENT_TYPES
            )

            detected_type = magic.from_buffer(contents, mime = True)
            file_extension = self.SUPPORTED_DOCUMENT_TYPES[detected_type]

            s3_folder = config.STUDENT_AWARDS_FOLDER
            doc_type = "AWARD"

            s3_key = self.generate_doc_key(student, doc_type, s3_folder, file_extension)
            award_key_column = "award_s3_key"

            self.upload.s3_upload(contents=contents, key=s3_key)

            logger.info(f"Award uploaded successfully for award {award.id}: {s3_key}")

            self.upload.save_key_in_db(award, s3_key, award_key_column)

            return {
                "filename": s3_key.split('/')[-1],
                "size": len(contents),
                "file_type": detected_type
            }

        except Exception as e:
            logger.error(f"Award upload failed for award {award.id}: {str(e)}")
            raise


    def remove_award_file(self, award: StudentAward) -> None:
        """
        Delete award file from S3 and database.
        Args:
            award: Award object
        """
        try:
            s3_key = award.award_s3_key
            self.upload.s3_client.delete_object(Bucket=self.upload.AWS_BUCKET_NAME, Key=s3_key)

            award.award_s3_key = None
            award.last_modified_by = self.current_user.id
            self.session.commit()

            logger.info(f"Award file deleted for award {award.id}")


        except Exception as e:
            self.session.rollback()
            logger.error(f"Failed to file for award {award.id}: {str(e)}")
            raise


    def export_award_audit(self, award_id: UUID, export_format: str) -> str:
        """Export award and its associated data
        Args:
            award_id: award UUID
            export_format: Preferred export format
        """
        return self.export_service.export_entity(
            StudentAward, award_id, export_format
        )


    def upload_document_file(self, file, student, document: StudentDocument):
        """
        Upload and validate a document for a student.
        Args:
            file: The uploaded file
            student: Student object
            document: StudentDocument object
        Returns:
            dict: Upload result with success status and file info
        """
        try:
            contents = self.upload.validate_file_upload(
                file, self.MIN_FILE_SIZE, self.MAX_FILE_SIZE, self.SUPPORTED_DOCUMENT_TYPES
            )

            detected_type = magic.from_buffer(contents, mime=True)
            file_extension = self.SUPPORTED_DOCUMENT_TYPES[detected_type]
            doc_type = document.document_type.value

            s3_folder = config.STUDENT_DOCUMENTS_FOLDER
            s3_key = self.generate_doc_key(student, doc_type, s3_folder, file_extension)
            document_key_column = "document_s3_key"

            self.upload.s3_upload(contents=contents, key=s3_key)

            logger.info(f"Document uploaded successfully for document {document.id}: {s3_key}")

            self.upload.save_key_in_db(document, s3_key, document_key_column)

            return {
                "filename": s3_key.split('/')[-1],
                "size": len(contents),
                "file_type": detected_type
            }

        except Exception as e:
            logger.error(f"Document upload failed for document {document.id}: {str(e)}")
            raise


    def remove_document_file(self, document: StudentDocument) -> None:
        """
        Delete document file from S3 and database.
        Args:
            document: Document object
        """
        try:
            s3_key = document.document_s3_key
            self.upload.s3_client.delete_object(Bucket=self.upload.AWS_BUCKET_NAME, Key=s3_key)

            document.document_s3_key = None
            document.last_modified_by = self.current_user.id
            self.session.commit()

            logger.info(f"Document file deleted document {document.id}")


        except Exception as e:
            self.session.rollback()
            logger.error(f"Failed to file for document {document.id}: {str(e)}")
            raise



    def export_document_audit(self, document_id: UUID, export_format: str) -> str:
        """Export award and its associated data
        Args:
            document_id: document UUID
            export_format: Preferred export format
        """
        return self.export_service.export_entity(
            StudentDocument, document_id, export_format
        )
