import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools import search_web, read_file, run_command

def execute_tool(tool_call: str) -> str:
    """
    Parses tool call string in the format 'TOOL: tool_name: argument'
    and executes the corresponding function.
    """
    try:
        _, tool_call = tool_call.split(":", 1)
        tool_name, _, arg = tool_call.strip().partition(":")
        tool_name = tool_name.strip()
        arg = arg.strip()

        if tool_name == "search_web":
            return search_web(arg)
        elif tool_name == "read_file":
            return read_file(arg)
        elif tool_name == "run_command":
            return run_command(arg)
        else:
            return f"Ferramenta desconhecida: {tool_name}"
    except Exception as e:
        return f"Erro ao interpretar chamada de ferramenta: {str(e)}"
