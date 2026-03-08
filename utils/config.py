import os
from pathlib import Path
from dotenv import load_dotenv

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Load environment variables from .env file (explicit path)
env_path = PROJECT_ROOT / ".env"
load_dotenv(dotenv_path=env_path)

# Groq Settings
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Validate API Key
if not GROQ_API_KEY:
    raise ValueError(f"GROQ_API_KEY not found! Check your .env file at: {env_path}")

# App Settings
APP_NAME = "Math Mentor"
APP_VERSION = "1.0.0"

# Confidence Thresholds (for HITL triggers)
OCR_CONFIDENCE_THRESHOLD = 0.7
ASR_CONFIDENCE_THRESHOLD = 0.7
VERIFIER_CONFIDENCE_THRESHOLD = 0.8

# RAG Settings
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K_RESULTS = 3

# Database
MEMORY_DB_PATH = str(PROJECT_ROOT / "memory" / "memory.db")
CHROMA_DB_PATH = str(PROJECT_ROOT / "rag" / "chroma_store")