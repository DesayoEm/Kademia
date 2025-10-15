import magic
from uuid import uuid4
from typing import Dict, Any
from sqlalchemy.orm import Session

from app.core.identity.models.student import Student
from app.core.shared.exceptions.assessment_errors import FileAlreadyExistsError
from app.core.shared.services.file_storage.s3_upload import S3Upload
from app.infra.log_service.logger import logger
from app.settings import config


class AssessmentFileService:
    def __init__(self, session: Session, current_user = None):
        self.session = session
        self.current_user = current_user
        self.upload = S3Upload(session, current_user=current_user)
        

        self.SUPPORTED_FILE_TYPES = {
            'image/png': 'png',
            'image/jpeg': 'jpg',
            'image/jpg': 'jpg',
            'image/webp': 'webp',
            'application/pdf': 'pdf',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx',
            'application/msword': 'doc'
        }

        self.MIN_FILE_SIZE = 1 * self.upload.KB
        self.MAX_FILE_SIZE = 5 * self.upload.MB

    @staticmethod
    def generate_file_key(
            student: Student, grade_type: str, s3_folder: str, file_extension: str
    ) -> str:
        """
        Generate a unique filename for the uploaded file.
        Args:
            student: Student object
            s3_folder: S3 folder path (e.g., "student-documents/")
            grade_type: Type of grade being stored
            file_extension: File extension
        Returns:
            str: Unique filename
        """

        unique_id = str(uuid4())[:8]
        first_name = student.first_name
        last_name = student.last_name

        return f"{s3_folder}_{first_name}_{last_name}_{grade_type.value}_{unique_id}.{file_extension}"


    def upload_assessment_file(self, file, student, grade) -> Dict[str, Any]:
        """
        Upload and validate an assessment file for a grade.
        Args:
            file: The uploaded file
            student: Student to be graded
            grade: Grade object
        Returns:
            dict: Upload result with success status and file info
        """
        if grade.file_url:
            raise FileAlreadyExistsError(grade.id)

        try:
            contents = self.upload.validate_file_upload(
                file, self.MIN_FILE_SIZE, self.MAX_FILE_SIZE, self.SUPPORTED_FILE_TYPES
            )

            detected_type = magic.from_buffer(contents, mime=True)
            file_extension = self.SUPPORTED_FILE_TYPES[detected_type]

            s3_folder = config.ASSESSMENTS_FOLDER
            grade_type = grade.type
            s3_key = self.generate_file_key(student, grade_type, s3_folder, file_extension)

            file_key_name = "file_url"
            self.upload.s3_upload(contents=contents, key=s3_key)

            logger.info(f"File uploaded successfully for grade {grade.id}: {s3_key}")

            self.upload.save_key_in_db(grade, s3_key, file_key_name)

            return {
                "filename": s3_key.split('/')[-1],
                "size": len(contents),
                "file_type": detected_type
            }

        except Exception as e:
            logger.error(f"File upload failed for grade {grade.id}: {str(e)}")
            raise


    def remove_assessment_file(self, grade) -> None:
        """
        Delete assessment file from S3 and database.
        Args:
            grade: Grade object
        """
        if grade.file_url:
            try:
                s3_key = grade.file_url
                self.upload.s3_client.delete_object(Bucket=self.upload.AWS_BUCKET_NAME, Key=s3_key)

                grade.file_url = None
                grade.last_modified_by = self.current_user.id
                self.session.commit()

                logger.info(f"File deleted for grade {grade.id}")


            except Exception as e:
                self.session.rollback()
                logger.error(f"Failed to delete assessment file for grade {grade.id}: {str(e)}")
                raise





