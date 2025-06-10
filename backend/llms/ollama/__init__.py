import os
from typing import Dict, List

import ollama

from .._session_store import DEFAULT_SESSION_STORE


class OllamaGenerator:
    SESSION_STORE = DEFAULT_SESSION_STORE()
    # base_url = "http://localhost:11434"

    def __init__(self, model_name: str, context: str, base_url: str = "http://localhost:11434"):
        prompt_template = os.path.join(os.path.dirname(__file__), "prompt_format.md")
        prompt = open(prompt_template, "r", encoding="utf-8").read()
        self.model_name = model_name
        self.PROMPT_TEMPLATE = prompt
        self.context = context
        if base_url:
            self.ollama = ollama.Client(host=base_url)
        else:
            self.ollama = ollama

    def _format_first_session(self, query: str) -> str:
        return [{"role": "user", "content": self.PROMPT_TEMPLATE.format(context=self.context, query=query)}]

    def _chat(self, messages: List[Dict[str, str]]) -> str:
        return self.ollama.chat(model=self.model_name, messages=messages)

    def _get_or_create_session(self, user_id: str, query: str) -> List[Dict[str, str]]:
        return self.SESSION_STORE.get(user_id) or self._format_first_session(query)

    def get_response(self, user_id: str, user_input: str) -> str:
        session = self._get_or_create_session(user_id, user_input)
        session.append({"role": "user", "content": user_input})
        response = ollama.chat(model=self.model_name, messages=session)
        session.append({"role": "assistant", "content": response["message"]["content"]})
        return response["message"]["content"]
