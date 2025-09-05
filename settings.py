from dotenv import load_dotenv
import os

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
if not GOOGLE_API_KEY:
    raise RuntimeError("Please set GOOGLE_API_KEY in .env")

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")

SYSTEM_PROMPT = (
    "You are an AI agent that helps users by reasoning clearly. "
    "You can call tools when needed. "
    "Available tools: search_web(query), read_file(path), run_command(command). "
    "Always respond in Portuguese when talking to the user."
)
