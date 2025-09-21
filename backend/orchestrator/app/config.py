from dotenv import load_dotenv
import os

load_dotenv()

AGENT_URL = os.getenv("AGENT_URL")
AGENT_KEY = os.getenv("AGENT_KEY").strip()
HTTP_TIMEOUT = 5  # segundos
MAX_RETRIES = 3
