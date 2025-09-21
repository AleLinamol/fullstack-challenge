from dotenv import load_dotenv
import os


load_dotenv() 

AGENT_KEY = os.getenv("AGENT_KEY")
AGENT_URL = os.getenv("AGENT_URL")