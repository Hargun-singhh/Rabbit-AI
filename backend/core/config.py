from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Data Analysis API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey-change-me")
    CORS_ORIGINS: list[str] = ["*"] # In production, restrict this
    
    # Upload limits
    MAX_UPLOAD_SIZE_MB: int = int(os.getenv("MAX_UPLOAD_SIZE_MB", "10"))
    
    # AI Integration
    GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY")
    ENABLE_AI_SUMMARY: bool = os.getenv("ENABLE_AI_SUMMARY", "true").lower() == "true"
    
    # Email
    EMAIL_SENDER: str | None = os.getenv("EMAIL_SENDER")
    EMAIL_FROM: str | None = os.getenv("EMAIL_FROM")
    EMAIL_PASSWORD: str | None = os.getenv("EMAIL_PASSWORD") # App password if using Gmail/Yagmail
    SENDGRID_API_KEY: str | None = os.getenv("SENDGRID_API_KEY") # Optional SendGrid Support
    
    # DB
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./reports.db")

settings = Settings()
