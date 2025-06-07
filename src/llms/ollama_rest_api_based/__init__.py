import os
import uuid
from typing import Dict, List

import requests

from .._session_store import DEFAULT_SESSION_STORE


class OllamaRestAPIBasedGenerator:
    # base_url = "http://localhost:11434"
    _session_store = DEFAULT_SESSION_STORE()

    def __init__(self, model_name: str, context: str, session_id: str = None, base_url: str = "http://localhost:11434"):
        prompt_template = os.path.join(os.path.dirname(__file__), "prompt_format.md")
        prompt = open(prompt_template, "r", encoding="utf-8").read()
        self.model_name = model_name
        self.PROMPT_TEMPLATE = prompt
        self.session_id = session_id or str(uuid.uuid4())
        self.context = context
        self.base_url = base_url

    def _get_prompt_and_context(self, query: str) -> tuple[str, str]:
        """
        return PROMPT, CONTEXT
        """
        session_store_context = self._session_store.get(self.session_id)
        if not session_store_context:
            return self.PROMPT_TEMPLATE.format(context=self.context, query=query), None
        else:
            return (
                """
            Adding FAQ data: {self.context}
            User Question:
            {query}
            Answer:"
            """,
                session_store_context,
            )

    def get_response(self, query: str) -> dict:
        """
        curl: http://localhost:11434/api/generate -d '{"model": "llama3.2", "prompt": "Hello, how are you?", "stream": false}'
        """
        prompt, context = self._get_prompt_and_context(query)

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3.2", "prompt": prompt, "stream": False, "context": context},
            timeout=10,  # 30 seconds timeout
        )
        data = response.json()
        self._session_store.set(self.session_id, data["context"])

        timings_in_ms = {
            "load_duration": data["load_duration"],  # a
            "prompt_eval_duration": data["prompt_eval_duration"],  # b
            "total_duration": data["total_duration"],  # a + b
        }
        resp = data.pop("response", None)
        return {
            "response": resp,
            "timings": timings_in_ms,
        }
