import os
from dotenv import load_dotenv

load_dotenv()

# parametros para utilização do serviço de LLM
OLLAMA_SERVICE_URL = f"{os.getenv('OLLAMA_SERVICE_HOST')}:{os.getenv('OLLAMA_SERVICE_PORT')}"
OLLAMA_API_URL = f"{OLLAMA_SERVICE_URL}/v1/chat/completions"
MODEL_NAME = os.getenv("OLLAMA_MODEL_NAME")

# parametros de comportamento do chat na aplicação
CHAT_MESSAGES_HIST_ITERATIONS = 3
STREAM_DELAY = 0.04

# parametros de comportamento do modelo LLM
ENVIAR_PARAMETROS_OPCIONAIS = False
TEMPERATURE = 0.8
TOP_P = 0.9
NUM_PREDICT = 300
REPEAT_PENALTY = 1.1