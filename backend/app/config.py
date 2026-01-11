import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(ENV_PATH)

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL")                # Supabase URL
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    BACKEND_HOSTS = ["http://localhost:5173", "http://localhost:3000"]
