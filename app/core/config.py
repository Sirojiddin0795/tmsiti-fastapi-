import os
from typing import Optional, List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./tmsiti.db"
    
    # Security
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # File upload
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_image_extensions: List[str] = [".jpg", ".jpeg", ".png", ".gif", ".webp"]
    allowed_document_extensions: List[str] = [".pdf", ".doc", ".docx"]
    
    # Pagination
    default_page_size: int = 20
    max_page_size: int = 100
    
    # Languages
    supported_languages: List[str] = ["uz", "ru", "en"]
    default_language: str = "uz"
    
    model_config = {"env_file": ".env", "extra": "ignore"}

settings = Settings()
