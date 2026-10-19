from pathlib import Path
import os
from dotenv import load_dotenv


# ============================================================
# EXAMORA CONFIGURATION
# ============================================================

# Load environment variables from .env
load_dotenv()


# ============================================================
# BASE DIRECTORIES
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

UPLOAD_DIR = BASE_DIR / "uploads"

DATA_DIR = BASE_DIR / "data"

EXTRACTED_DIR = DATA_DIR / "extracted"

PROCESSED_DIR = DATA_DIR / "processed"


# ============================================================
# UPLOAD DIRECTORIES
# ============================================================

SYLLABUS_DIR = UPLOAD_DIR / "syllabus"

MODULE_DIRS = {
    1: UPLOAD_DIR / "module_1",
    2: UPLOAD_DIR / "module_2",
    3: UPLOAD_DIR / "module_3",
    4: UPLOAD_DIR / "module_4",
    5: UPLOAD_DIR / "module_5",
}


# ============================================================
# SUPPORTED FILE TYPES
# ============================================================

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".pptx",
    ".docx",
    ".txt"
}


# ============================================================
# FILE LIMIT
# ============================================================

MAX_CONTENT_MB = 50

MAX_CONTENT_LENGTH = MAX_CONTENT_MB * 1024 * 1024


# ============================================================
# FLASK SECRET KEY
# ============================================================

SECRET_KEY = os.getenv(
    "EXAMORA_SECRET_KEY",
    "examora-development-secret-key"
)


# ============================================================
# APPLICATION SETTINGS
# ============================================================

APP_NAME = "EXAMORA"

APP_TAGLINE = "AI-Powered Exam Preparation Assistant"

DEBUG = True


# ============================================================
# HELPER FUNCTION
# ============================================================

def create_required_directories():
    """
    Create all directories required by EXAMORA.
    """

    directories = [
        UPLOAD_DIR,
        SYLLABUS_DIR,
        DATA_DIR,
        EXTRACTED_DIR,
        PROCESSED_DIR,
    ]

    directories.extend(MODULE_DIRS.values())

    for directory in directories:
        directory.mkdir(
            parents=True,
            exist_ok=True
        )