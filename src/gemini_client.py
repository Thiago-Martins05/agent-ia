import google.generativeai as genai
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from settings import GOOGLE_API_KEY, GEMINI_MODEL

# Configure Gemini API
genai.configure(api_key=GOOGLE_API_KEY)

# Create a client function
def get_gemini_response(prompt: str) -> str:
    model = genai.GenerativeModel(GEMINI_MODEL)
    response = model.generate_content(prompt)
    return response.text if response else "⚠️ Não recebi resposta do modelo."
