from dotenv import load_dotenv
import os

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
if not GOOGLE_API_KEY:
    raise RuntimeError("Please set GOOGLE_API_KEY in .env")

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")

SYSTEM_PROMPT = (
    "You are an AI agent that helps users by reasoning clearly. "
    "You have access to these tools:\n"
    "- search_web(query): to search information on the web.\n"
    "- read_file(path): to read local text files.\n"
    "- run_command(command): to execute shell commands.\n\n"
    "Rules:\n"
    "1. If you need external info, call a tool in this format: TOOL: <tool_name>: <argument>\n"
    "2. Otherwise, answer directly in Portuguese.\n"
)
