import os
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

# Project root
PROJECT_ROOT = Path(__file__).parent.parent

# Load .env locally (for local testing)
env_path = PROJECT_ROOT / ".env"
load_dotenv(dotenv_path=env_path)

# Groq Settings
GROQ_API_KEY = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile") or st.secrets.get("GROQ_MODEL")
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Validate API Key
if not GROQ_API_KEY:
    raise ValueError(f"GROQ_API_KEY not found! Check your .env locally or Streamlit Secrets at: {env_path}")