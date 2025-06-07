# Replace this later with redis-py
import json

import redis

from ._interface import ISessionStore


class RedisChatSessionStore(ISessionStore):
    def __init__(self, redis_client):
        self.r = redis_client

    def get(self, session_id):
        raw = self.r.get(session_id)
        return json.loads(raw) if raw else []

    def append(self, session_id, role, content):
        session = self.get(session_id)
        session.append({"role": role, "content": content})
        self.r.set(session_id, json.dumps(session))

    def clear(self, session_id):
        self.r.delete(session_id)
