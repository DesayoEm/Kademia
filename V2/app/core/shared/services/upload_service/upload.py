from V2.app.infra.log_service.logger import logger
from V2.app.infra.settings import config
import boto3



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

        if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
            logger.error("AWS credentials not found in environment variables")
            raise ValueError("AWS credentials are required but not found in .env file")

        logger.info(f"S3Upload initialized for bucket: {AWS_BUCKET_NAME} in region: {AWS_DEFAULT_REGION}")


    def s3_upload(self, contents: bytes, key: str) -> None:
        """
        Upload file to S3 with proper folder structure.
        Args:
            contents: File contents as bytes
            key: File name/key (folder path will be prepended)
        """

        logger.info(f'Uploading {key} to s3')
        try:
            bucket.put_object(Key = key, Body = contents)
        except Exception as e:
            logger.error(f'Failed to upload {key}: {str(e)}')
            raise