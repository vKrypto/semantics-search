import os
import uuid
from typing import Dict, List

import requests

from .._session_store import DEFAULT_SESSION_STORE


class GPTRestAPIBasedGenerator:
    """
    connect with ollama but using rest api only.
    """

    API_TOKEN = os.getenv("OPENAI_APIKEY")
    prompt_template_path = os.path.join(os.path.dirname(__file__), "prompt_format.md")
    PROMPT_TEMPLATE = open(prompt_template_path, "r", encoding="utf-8").read()

    # base_url = "http://localhost:11434"
    _session_store = DEFAULT_SESSION_STORE()

    def __init__(
        self,
        model_name: str,
        context: str,
        session_id: str = None,
        base_url: str = "https://api.openkey.ai/v1/chat/completions",
    ):
        if not self.API_TOKEN:
            raise EnvironmentError("OPENAPI_KEY not found in env variable, required for choosing GPT as LLM")
        self.model_name = model_name
        self.session_id = session_id or str(uuid.uuid4())
        self.context = context
        self.base_url = base_url

    @property
    def headers(self):
        return {"Authorization": f"Bearer {self.API_TOKEN}", "Content-Type": "application/json"}

    def get_payload(self, context, prompt):
        return {
            "model": self.model_name,
            "messages": [{"role": "system", "content": context}, {"role": "user", "content": prompt}],
            "temperature": 0.2,  #  safe [more relevance, less creativity]
        }

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
        payload = self.get_payload(context, prompt)

        print()
        response = requests.post(self.base_url, json=payload, timeout=30, verify=False)  # 30 seconds timeout
        data = response.json()
        print(data)
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
