import magic
from typing import Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, Integer
from V2.app.core.identity.models.student import Student
from V2.app.core.shared.services.upload_service.s3_upload import S3Upload
from V2.app.infra.log_service.logger import logger
from V2.app.infra.settings import config



class IdentityService:
    def __init__(self, session: Session, current_user = None):
        self.session = session
        self.upload = S3Upload()
        self.current_user = current_user

        self.SUPPORTED_IMAGE_TYPES = {
            'image/png': 'png',
            'image/jpeg': 'jpg',
            'image/jpg': 'jpg',
            'image/webp': 'webp'
        }

        self.MIN_FILE_SIZE = 1 * self.upload.KB
        self.MAX_FILE_SIZE = 5 * self.upload.MB


    def upload_profile_picture(self, file, user) -> Dict[str, Any]:
        """
        Upload and validate a profile picture for a user.
        Args:
            file: The uploaded file
            user: User object
        Returns:
            dict: Upload result with success status and file info
        """
        try:

            contents = self.upload.validate_file_upload(
                file, self.MIN_FILE_SIZE, self.MAX_FILE_SIZE, self.SUPPORTED_IMAGE_TYPES
            )

            detected_type = magic.from_buffer(contents, mime=True)
            file_extension = self.SUPPORTED_IMAGE_TYPES[detected_type]

            s3_folder = config.PROFILE_PICTURES_FOLDER
            filename = self.upload.generate_unique_filename(user, s3_folder, file_extension)

            self.upload.s3_upload(contents=contents, key=filename)

            logger.info(f"Profile picture uploaded successfully for user {user.id}: {filename}")

            return {
                "filename": filename,
                "size": len(contents),
                "file_type": detected_type
            }

        except Exception as e:
            logger.error(f"Profile picture upload failed for user {user.id}: {str(e)}")
            raise



    def generate_student_id(self, start_year: int):
        school_code = 'SCH'
        year_code = str(start_year)[2:]
        prefix = f"{school_code}-{year_code}-"
        pattern = f"{prefix}%"

        result = self.session.query(
            func.max(
                func.cast(
                    func.substring(Student.student_id, len(prefix) + 1),Integer
                )
            )
        ).filter(
            Student.student_id.like(pattern),
            Student.session_start_year == start_year
        ).scalar()

        next_serial = 1 if result is None else result + 1
        formatted_serial = f"{next_serial:05d}"
        student_id = f"{school_code}-{year_code}-{formatted_serial}"
        return student_id