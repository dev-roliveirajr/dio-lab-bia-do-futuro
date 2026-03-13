import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_SERVICE_URL = f"{os.getenv('OLLAMA_SERVICE_HOST')}:{os.getenv('OLLAMA_SERVICE_PORT')}"
OLLAMA_API_URL = f"{OLLAMA_SERVICE_URL}/api/generate"
MODEL_NAME = os.getenv("OLLAMA_MODEL_NAME")