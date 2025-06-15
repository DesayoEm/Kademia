from uuid import uuid4
import boto3
import magic
from V2.app.core.shared.exceptions import FileTooLargeError
from V2.app.core.shared.exceptions.entry_validation_errors import EmptyFileError, FileTooSmallError, \
    UnsupportedFileFormatError
from V2.app.infra.log_service.logger import logger
from V2.app.infra.settings import config



s3 = boto3.resource('s3')
bucket = s3.Bucket(config.AWS_BUCKET_NAME)

AWS_ACCESS_KEY_ID = config.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = config.AWS_SECRET_ACCESS_KEY
AWS_DEFAULT_REGION = config.AWS_DEFAULT_REGION
AWS_BUCKET_NAME = config.AWS_BUCKET_NAME


class S3Upload:
    def __init__(self):
        self.s3 = boto3.resource(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_DEFAULT_REGION
        )
        self.bucket = self.s3.Bucket(AWS_BUCKET_NAME)
        self.KB = 1024
        self.MB = 1024 * self.KB


        if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
            logger.error("AWS credentials not found in environment variables")
            raise ValueError("AWS credentials are required but not found in .env file")

        logger.info(f"S3Upload initialized for bucket: {AWS_BUCKET_NAME} in region: {AWS_DEFAULT_REGION}")



    def s3_upload(self,contents: bytes, key: str) -> None:
        """
        Upload file to S3 with proper folder structure.
        Args:
            contents: File contents as bytes
            key: File name/key (folder path will be prepended)
        """

        logger.info(f'Uploading {key} to s3')
        try:
            self.bucket.put_object(Key = key, Body = contents)
        except Exception as e:
            logger.error(f'Failed to upload {key}: {str(e)}')
            raise


    def validate_file_upload(self, file, min_size, max_size, supported_types: dict) -> bytes:
        """
        Validate uploaded file for size, type, and content.
        Args:
            file: The uploaded file
            min_size: Minimum file size in bytes
            max_size: Maximum file size in bytes
            supported_types: Dict of supported MIME types and extensions
        Returns:
            bytes: File contents if valid
        """

        if not file or not file.filename:
            raise EmptyFileError(entry=str(file))

        contents = file.file.read()
        file.file.seek(0)

        size = len(contents)
        if size < min_size:
            raise FileTooSmallError(
                size=size,
                threshold=f"{min_size // self.KB}KB",
            )

        if size > max_size:
            raise FileTooLargeError(
                size=size,
                threshold=f"{max_size // self.MB}MB",
            )

        detected_type = magic.from_buffer(contents, mime=True)
        if detected_type not in supported_types:
            acceptable_formats = ", ".join(supported_types.keys())
            raise UnsupportedFileFormatError(
                file_type=detected_type,
                acceptable_types=acceptable_formats
            )

        logger.info(f"File validation successful: {file.filename}, size: {size} bytes, type: {detected_type}")
        return contents


    @staticmethod
    def generate_unique_filename(user, s3_folder: str, file_extension: str) -> str:
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

