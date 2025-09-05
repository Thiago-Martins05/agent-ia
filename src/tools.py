import requests
import subprocess
from pathlib import Path

# --- Web search (mock with DuckDuckGo API) ---
def search_web(query: str) -> str:
    try:
        url = f"https://api.duckduckgo.com/?q={query}&format=json"
        response = requests.get(url, timeout=5)
        data = response.json()
        abstract = data.get("AbstractText") or "Nenhum resultado encontrado."
        return f"Resultado da busca: {abstract}"
    except Exception as e:
        return f"Erro na busca: {str(e)}"

# --- Read text file ---
def read_file(file_path: str) -> str:
    try:
        path = Path(file_path)
        if path.exists():
            return path.read_text(encoding="utf-8")
        return "Arquivo não encontrado."
    except Exception as e:
        return f"Erro ao ler arquivo: {str(e)}"

# --- Run shell command ---
def run_command(command: str) -> str:
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout if result.stdout else result.stderr
    except Exception as e:
        return f"Erro ao executar comando: {str(e)}"
