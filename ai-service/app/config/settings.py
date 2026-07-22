import os
from dotenv import load_dotenv

load_dotenv()

# Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing in .env")

# Gemini Models
EMBEDDING_MODEL = "gemini-embedding-001"
LLM_MODEL = "gemini-2.5-flash"

# ChromaDB Configuration
CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "documents"

# Chunking Configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200