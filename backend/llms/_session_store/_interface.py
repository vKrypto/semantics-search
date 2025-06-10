from typing import Dict, List


# Interface for session cache
class ISessionStore:

    def get(self, session_id: str) -> List[Dict[str, str]]: ...

    def append(self, session_id: str, role: str, content: str): ...

    def clear(self, session_id: str): ...
