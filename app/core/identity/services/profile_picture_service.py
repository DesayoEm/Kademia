import magic
from uuid import uuid4
from typing import Dict, Any
from sqlalchemy.orm import Session
from app.core.shared.services.file_storage.s3_upload import S3Upload
from app.infra.log_service.logger import logger
from app.infra.settings import config


class ProfilePictureService:
    def __init__(self, session: Session, current_user = None):
        self.session = session
        self.current_user = current_user
        self.upload = S3Upload(session, current_user=current_user)


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
            s3_key = self.generate_profile_pic_key(user, s3_folder, file_extension)
            profile_pic_key_name = "profile_s3_key"

            self.upload.s3_upload(contents=contents, key=s3_key)

            logger.info(f"Profile picture uploaded successfully for user {user.id}: {s3_key}")

            self.upload.save_key_in_db(user, s3_key, profile_pic_key_name)

            return {
                "filename": s3_key.split('/')[-1],
                "size": len(contents),
                "file_type": detected_type
            }

        except Exception as e:
            logger.error(f"Profile picture upload failed for user {user.id}: {str(e)}")
            raise


    @staticmethod
    def generate_profile_pic_key(user, s3_folder: str, file_extension: str) -> str:
        """
        Generate a unique filename for the uploaded file.
        Args:
            user: User object with user_type, first_name, last_name
            s3_folder: S3 folder path (e.g., "profile-pictures/")
            file_extension: File extension
        Returns:
            str: Unique filename
        """

        unique_id = str(uuid4())[:8]

        first_name = user.first_name
        last_name = user.last_name
        user_type = user.user_type.value.lower()

        return f"{s3_folder}{user_type}_{first_name}_{last_name}_{unique_id}_profile.{file_extension}"


    def remove_profile_pic(self, user) -> None:
        """
        Delete profile picture from S3 and database.
        Args:
            user: User object
        """
        try:
            s3_key = user.profile_s3_key
            self.upload.s3_client.delete_object(Bucket=self.upload.AWS_BUCKET_NAME, Key=s3_key)

            user.profile_s3_key = None
            user.last_modified_by = self.current_user.id
            self.session.commit()

            logger.info(f"Profile picture deleted for user {user.id}")


        except Exception as e:
            self.session.rollback()
            logger.error(f"Failed to delete profile picture for user {user.id}: {str(e)}")
            raise





