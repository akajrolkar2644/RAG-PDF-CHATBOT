import os
import shutil
from backend.config.settings import VECTOR_STORE_PATH

def reset_faiss_index():
    """Reset the FAISS index by removing all stored data."""
    if os.path.exists(VECTOR_STORE_PATH):
        shutil.rmtree(VECTOR_STORE_PATH)
        print(f"FAISS index at {VECTOR_STORE_PATH} has been reset.")
    else:
        print(f"No FAISS index found at {VECTOR_STORE_PATH}")

if __name__ == "__main__":
    reset_faiss_index()