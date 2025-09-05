from gemini_client import get_gemini_response
from settings import SYSTEM_PROMPT
from chat_session import ChatSession

def run_agent():
    print("🤖 Olá! Eu sou seu agente de IA com memória. Digite 'sair' para encerrar.\n")

    session = ChatSession(SYSTEM_PROMPT)

    while True:
        user_input = input("Você: ")
        if user_input.lower() in ["sair", "exit", "quit"]:
            print("👋 Até logo!")
            break

        session.add_user_message(user_input)

        try:
            response = get_gemini_response(session.get_history())
            print("Agente:", response)
            session.add_agent_message(response)
        except Exception as e:
            print("⚠️ Ocorreu um erro:", str(e))
