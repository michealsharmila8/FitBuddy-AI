import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


APP_NAME = "FitBuddy"

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{(BASE_DIR / 'fitbuddy.db').as_posix()}"
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()

GEMINI_WORKOUT_MODEL = os.getenv(
    "GEMINI_WORKOUT_MODEL",
    "gemini-3.8-flash"
)

GEMINI_NUTRITION_MODEL = os.getenv(
    "GEMINI_NUTRITION_MODEL",
    "gemini-3.8-flash"
)