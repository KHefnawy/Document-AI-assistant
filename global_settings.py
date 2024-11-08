import os
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

# Load environment variables from  .env file
load_dotenv()

# File paths
LOG_FILE = "session_data/user_actions.log"
CACHE_FILE = "cache/pipeline_cache.json"
CONVERSATION_FILE = "cache/chat_history.json"
STORAGE_PATH = "ingestion_storage/"
INDEX_STORAGE = "index_storage"

# API Settings
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY or not OPENAI_API_KEY.startswith('sk-'):
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]


def initialize_settings():
    # Create necessary directories
    directories = [
        os.path.dirname(LOG_FILE),
        os.path.dirname(CACHE_FILE),
        STORAGE_PATH,
        INDEX_STORAGE
    ]
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    # Validate API key
    if not OPENAI_API_KEY or not OPENAI_API_KEY.startswith('sk-'):
        raise ValueError("Valid OPENAI_API_KEY not found in environment variables or Streamlit secrets")
