from collections import defaultdict
from typing import Dict, List

import ollama

from ._interface import ISessionStore


# Interface for session cache
class ChatSessionStore(ISessionStore):
    def __init__(self):
        # This can be replaced by a Redis client in production
        self._store: Dict[str, List[Dict[str, str]]] = defaultdict(list)

    def get(self, session_id: str) -> List[Dict[str, str]]:
        return self._store[session_id]

    def set(self, session_id: str, context: str):
        self._store[session_id] = context

    def append(self, session_id: str, role: str, content: str):
        self._store[session_id].append({"role": role, "content": content})

    def clear(self, session_id: str):
        self._store[session_id] = []
