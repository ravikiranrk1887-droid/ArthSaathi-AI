import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration class loaded from environment variables."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///finbot.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
    DEBUG = os.environ.get("DEBUG", "False").lower() in ("true", "1", "yes")
