import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Type annotations for environment variables
HF_API_KEY: str = os.getenv("HF_API_KEY") or "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"  # Fallback to the provided key
VECTOR_STORE_PATH: str = os.getenv("VECTOR_STORE_PATH", "data/faiss_index")
MODEL_NAME: str = os.getenv("MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")
HF_LLM_MODEL: str = os.getenv("HF_LLM_MODEL", "microsoft/DialoGPT-large")