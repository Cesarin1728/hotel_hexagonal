import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "3306")       
    DB_USER: str = os.getenv("DB_USER", "root")       
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")   
    DB_NAME: str = os.getenv("DB_NAME", "hotel_local")
    
    AWS_ACCESS_KEY: str = os.getenv("AWS_ACCESS_KEY", "tu_access_key")
    AWS_SECRET_KEY: str = os.getenv("AWS_SECRET_KEY", "tu_secret_key")
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")
    BUCKET_NAME: str = os.getenv("BUCKET_NAME", "hotel-imagenes")
    AWS_ENDPOINT_URL: str | None = os.getenv("AWS_ENDPOINT_URL", None)

settings = Settings()

DB_URL = f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"