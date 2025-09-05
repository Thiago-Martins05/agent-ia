from gemini_client import get_gemini_response
from settings import SYSTEM_PROMPT
from chat_session import ChatSession
from tools import search_web, read_file, run_command

def run_agent():
    print("🤖 Olá! Eu sou seu agente de IA com ferramentas externas. Digite 'sair' para encerrar.\n")

    session = ChatSession(SYSTEM_PROMPT)

    while True:
        user_input = input("Você: ")
        if user_input.lower() in ["sair", "exit", "quit"]:
            print("👋 Até logo!")
            break

        session.add_user_message(user_input)

        try:
            response = get_gemini_response(session.get_history())

            if response.startswith("TOOL:"):
                # Parse tool call
                _, tool_call = response.split(":", 1)
                tool_name, _, arg = tool_call.strip().partition(":")
                tool_name = tool_name.strip()
                arg = arg.strip()

                if tool_name == "search_web":
                    tool_result = search_web(arg)
                elif tool_name == "read_file":
                    tool_result = read_file(arg)
                elif tool_name == "run_command":
                    tool_result = run_command(arg)
                else:
                    tool_result = f"Ferramenta desconhecida: {tool_name}"

                print(f"🔧 Executando {tool_name}...\n{tool_result}")
                session.add_agent_message(tool_result)

            else:
                print("Agente:", response)
                session.add_agent_message(response)

        except Exception as e:
            print("⚠️ Ocorreu um erro:", str(e))
