from dotenv import load_dotenv
import os

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
if not GOOGLE_API_KEY:
    raise RuntimeError("Please set GOOGLE_API_KEY in .env")

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")

SYSTEM_PROMPT = (
    "You are an AI agent that helps users by reasoning clearly, "
    "calling tools when needed, and giving structured answers."
)
