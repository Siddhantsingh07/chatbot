"""
config.py – Centralised settings loaded from .env
"""
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./university_chatbot.db")
SIMILARITY_THRESHOLD: float = float(os.getenv("SIMILARITY_THRESHOLD", "0.25"))
MAX_HISTORY_RECORDS: int = int(os.getenv("MAX_HISTORY_RECORDS", "50"))

_raw_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000")
CORS_ORIGINS: list[str] = [o.strip() for o in _raw_origins.split(",")]

# Gemini AI Settings
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
USE_GEMINI: bool = os.getenv("USE_GEMINI", "true").lower() in ("true", "1", "yes")
