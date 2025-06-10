import os
import uuid
from typing import Dict, List

import requests
from openai import OpenAI

from .._session_store import DEFAULT_SESSION_STORE


class GPTGenerator:
    """
    connect with ollama but using rest api only.
    """

    API_TOKEN = os.getenv("OPENAI_APIKEY")

    prompt_template_path = os.path.join(os.path.dirname(__file__), "prompt_format.md")
    PROMPT_TEMPLATE = open(prompt_template_path, "r", encoding="utf-8").read()

    # base_url = "http://localhost:11434"
    _session_store = DEFAULT_SESSION_STORE()

    def __init__(self, model_name: str, context: str, session_id: str = None):
        if not self.API_TOKEN:
            raise EnvironmentError("OPENAPI_KEY not found in env variable, required for choosing GPT as LLM")
        self.model_name = model_name
        self.client = OpenAI(api_key=self.API_TOKEN)
        self.session_id = session_id or str(uuid.uuid4())
        self.context = context

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
        # TODO: history is not being passed to chatgpt, we have tomain tain
        prompt, context = self._get_prompt_and_context(query)
        # payload = self.get_payload(context, prompt)
        data = self.client.chat.completions.create(
            model=self.model_name, store=True, messages=[{"role": "user", "content": prompt}]
        )
        self._session_store.set(self.session_id, data.id)
        timings_in_ms = 0
        return {
            "response": data.choices[0].message.content,
            "timings": timings_in_ms,
        }
