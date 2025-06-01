import os
from typing import Dict, List

import requests


class OllamaRestAPIBasedGenerator:
    # base_url = "http://localhost:11434"

    def __init__(self, model_name: str, context: str, base_url: str = "http://localhost:11434"):
        prompt_template = os.path.join(os.path.dirname(__file__), "prompt_format.md")
        prompt = open(prompt_template, "r", encoding="utf-8").read()
        self.model_name = model_name
        self.PROMPT_TEMPLATE = prompt
        self.context = context
        self.base_url = base_url

    def _get_prompt(self, query: str) -> str:
        return self.PROMPT_TEMPLATE.format(context=self.context, query=query)

    def get_response(self, query: str) -> str:
        prompt = self._get_prompt(query)
        response = requests.post(
            "http://localhost:11434/api/generate", json={"model": "llama3.2", "prompt": prompt, "stream": False}
        )
        data = response.json()
        resp = data.pop("response", None)
        print("----" * 20)
        print(query)
        print("\t" * 2, resp)
        # return resp
