import boto3
import uuid
from app.domain.ports.storage_port import StoragePort
from app.infrastructure.config.settings import settings

class S3StorageAdapter(StoragePort):
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_SECRET_KEY,
            region_name=settings.AWS_REGION,
            endpoint_url=settings.AWS_ENDPOINT_URL
        )
        self.bucket_name = settings.BUCKET_NAME

    def upload_file(self, file_stream, filename: str, content_type: str) -> str:
        unique_filename = f"{uuid.uuid4()}-{filename}"
        self.s3_client.upload_fileobj(
            file_stream,
            self.bucket_name,
            unique_filename,
            ExtraArgs={"ContentType": content_type}
        )
        if settings.AWS_ENDPOINT_URL:
            return f"{settings.AWS_ENDPOINT_URL}/{self.bucket_name}/{unique_filename}"
        return f"https://{self.bucket_name}.s3.{settings.AWS_REGION}.amazonaws.com/{unique_filename}"