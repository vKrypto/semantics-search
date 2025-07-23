import pytest
from fastapi.testclient import TestClient
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import app

from domain.models.search import SearchResponse, SearchRequest
from domain.models.chat import ChatResponse, ChatRequest


class DummySearchService:
    async def search(self, request: SearchRequest) -> SearchResponse:
        return SearchResponse(results=[], server_time=1.0, total_results=0, query=request.query)


class DummyChatService:
    async def process_chat_request(self, request: ChatRequest) -> ChatResponse:
        return ChatResponse(response="ok", context=[], server_time=1.0)


def test_search_endpoint(monkeypatch):
    from api.routes import search as search_route

    monkeypatch.setattr(search_route, "_get_search_service", lambda: DummySearchService())

    client = TestClient(app)
    resp = client.post("/app/v1/search/", params={"q": "hello"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["query"] == "hello"
    assert data["total_results"] == 0


def test_chat_endpoint(monkeypatch):
    from api.routes import chat as chat_route

    async def _dummy_service():
        return DummyChatService()

    app.dependency_overrides[chat_route.get_chat_service] = _dummy_service

    client = TestClient(app)
    resp = client.post("/app/v1/chat/", json={"query": "hi"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["response"] == "ok"

    app.dependency_overrides.clear()
