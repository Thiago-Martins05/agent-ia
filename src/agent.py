from gemini_client import get_gemini_response
from settings import SYSTEM_PROMPT

def run_agent():
    print("🤖 Olá! Eu sou seu agente de IA com Gemini. Digite 'sair' para encerrar.\n")
    while True:
        user_input = input("Você: ")
        if user_input.lower() in ["sair", "exit", "quit"]:
            print("👋 Até logo!")
            break

        # Build final prompt with system instructions
        full_prompt = f"{SYSTEM_PROMPT}\n\nUser: {user_input}"
        try:
            response = get_gemini_response(full_prompt)
            print("Agente:", response)
        except Exception as e:
            print("⚠️ Ocorreu um erro:", str(e))
