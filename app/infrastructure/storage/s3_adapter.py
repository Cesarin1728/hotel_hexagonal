import requests
from app.domain.ports.storage_port import StoragePort
from app.infrastructure.config.settings import settings

class S3StorageAdapter(StoragePort):
    def __init__(self):
        self.supabase_url = settings.AWS_ENDPOINT_URL
        self.anon_key = settings.AWS_ACCESS_KEY
        self.bucket_name = settings.BUCKET_NAME

    def upload_file(self, file_stream, filename: str, content_type: str) -> str:
        file_stream.seek(0)
        file_data = file_stream.read()

        url = f"{self.supabase_url}/storage/v1/object/{self.bucket_name}/{filename}"
        headers = {
            "Authorization": f"Bearer {self.anon_key}",
            "ApiKey": self.anon_key,
            "Content-Type": content_type,
            "x-upsert": "true"
        }

        response = requests.post(url, headers=headers, data=file_data)

        if response.status_code not in [200, 201]:
            raise Exception(f"Fallo al subir: {response.text}")

        return f"{self.supabase_url}/storage/v1/object/public/{self.bucket_name}/{filename}"