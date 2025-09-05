from typing import List, Dict

class ChatSession:
    def __init__(self, system_prompt: str):
        self.system_prompt = system_prompt
        self.history: List[Dict[str, str]] = [
            {"role": "system", "content": self.system_prompt}
        ]

    def add_user_message(self, message: str):
        self.history.append({"role": "user", "content": message})

    def add_agent_message(self, message: str):
        self.history.append({"role": "assistant", "content": message})

    def get_history(self) -> List[Dict[str, str]]:
        return self.history
