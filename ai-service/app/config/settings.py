from dotenv import load_dotenv
import os

load_dotenv()

# Gemini API Key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Embedding Model
EMBEDDING_MODEL = "all-MiniLM-L6-v2"