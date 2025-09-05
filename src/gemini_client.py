import google.generativeai as genai
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from settings import GOOGLE_API_KEY, GEMINI_MODEL

# Configure Gemini API
genai.configure(api_key=GOOGLE_API_KEY)

# Create a model instance once
model = genai.GenerativeModel(GEMINI_MODEL)

def get_gemini_response(messages: list) -> str:
    """
    messages: list of dicts with role ('user', 'assistant', 'system') and content
    """
    # Convert messages to a simple text format for now
    conversation_text = ""
    for message in messages:
        if message["role"] == "system":
            conversation_text += f"System: {message['content']}\n\n"
        elif message["role"] == "user":
            conversation_text += f"User: {message['content']}\n"
        elif message["role"] == "assistant":
            conversation_text += f"Assistant: {message['content']}\n"
    
    response = model.generate_content(conversation_text)
    return response.text if response else "⚠️ Não recebi resposta do modelo."
