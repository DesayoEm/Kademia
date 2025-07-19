
import boto3
import magic
from sqlalchemy.orm import Session
from botocore.exceptions import ClientError
from app.core.shared.exceptions import FileTooLargeError
from app.core.shared.exceptions.file_errors import EmptyFileError, FileTooSmallError, \
    UnsupportedFileFormatError
from app.core.shared.exceptions.file_errors import AbsentKeyError
from app.infra.log_service.logger import logger
from app.infra.settings import config


s3 = boto3.resource('s3')
bucket = s3.Bucket(config.AWS_BUCKET_NAME)


class S3Upload:
    def __init__(self, session: Session, current_user):
        self.AWS_ACCESS_KEY_ID = config.AWS_ACCESS_KEY_ID
        self.AWS_SECRET_ACCESS_KEY = config.AWS_SECRET_ACCESS_KEY
        self.AWS_DEFAULT_REGION = config.AWS_DEFAULT_REGION
        self.AWS_BUCKET_NAME = config.AWS_BUCKET_NAME
        self.session = session
        self.current_user = current_user

        self.s3_resource = boto3.resource(
            's3',
            aws_access_key_id=self.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY,
            region_name=self.AWS_DEFAULT_REGION
        )

        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=self.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY,
            region_name=self.AWS_DEFAULT_REGION
        )
        self.bucket = self.s3_resource.Bucket(self.AWS_BUCKET_NAME)
        self.KB = 1024
        self.MB = 1024 * self.KB


        if not self.AWS_ACCESS_KEY_ID or not self.AWS_SECRET_ACCESS_KEY:
            logger.error("AWS credentials not found in environment variables")
            raise ValueError("AWS credentials are required but not found in .env file")

        logger.info(f"S3Upload initialized for bucket: {self.AWS_BUCKET_NAME} in region: {self.AWS_DEFAULT_REGION}")



    def s3_upload(self,contents: bytes, key: str) -> str:
        """
        Upload file to S3 with proper folder structure.
        Args:
            contents: File contents as bytes
            key: File name/key (folder path will be prepended)
        """

        logger.info(f'Uploading {key} to s3')
        try:
            self.bucket.put_object(Key = key, Body = contents)
            return key

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


    def save_key_in_db(self, obj, s3_key: str, key_col_name: str):
        """
        Save S3 key to database.
        Args:
            obj: database object
            s3_key: S3 key to save
            key_col_name: column name of the key on the database
        """
        try:
            setattr(obj, key_col_name, s3_key)

            obj.last_modified_by = self.current_user.id
            self.session.commit()

            logger.info(f"S3 key saved to database for obj {obj.id}: {s3_key}")

        except Exception as e:
            self.session.rollback()
            logger.error(f"Failed to save S3 key to database for object {type(obj)}, id: {obj.id}: {str(e)}")
            raise



    def generate_presigned_url(self, s3_key: str, exp: int = 3600 * 24) -> str:
        """
        Generate presigned URL for secure, temporary access.
        Default: 1 hour expiration
        """
        try:
            if not s3_key or not s3_key.strip():
                raise AbsentKeyError(entry=s3_key)

            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.AWS_BUCKET_NAME, 'Key': s3_key},
                ExpiresIn=exp
             )

            logger.info(f"Generated presigned URL for {s3_key} (expires in {exp}s)")
            return url


        except ClientError as e:
            error_code = e.response['Error']['Code']
            logger.error(f"Error generating presigned URL for {s3_key}: {error_code}")
            raise


