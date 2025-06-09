import time
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Body, Query, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from llms import *
from search import search_query_and_create_context

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
    responses={404: {"description": "Not found"}},
)


# Mount templates
templates_path = Path(__file__).parent.parent / "templates"
templates = Jinja2Templates(directory=str(templates_path))


class ChatRequest(BaseModel):
    query: Optional[str] = None


@router.get("/")
async def get_chat_interface(request: Request):
    """
    Handle GET requests to return the chat interface.

    Args:
        request: The FastAPI request object
    Returns:
        The chat template
    """
    return templates.TemplateResponse("chat.html", {"request": request})


@router.post("/")
async def chat(request: Request, chat_request: ChatRequest = Body(...)):
    """
    Handle POST requests for chat functionality.
    Processes the chat query and returns the response.

    Args:
        request: The FastAPI request object
        chat_request: The chat request containing the query
    Returns:
        A dictionary containing chat results
    """
    query = chat_request.query

    # If no query, return empty results
    if not query:
        return {"results": [], "server_time": 0}

    # Process the chat query
    start_time = time.time()
    context = search_query_and_create_context(query)
    server_time = round((time.time() - start_time) * 1000, 2)  # Convert to milliseconds
    # llm = OllamaRestAPIBasedGenerator("llama3.2", context, "user_session_id")
    # llm = GPTRestAPIBasedGenerator("gpt-4o-mini", context, "session_id")
    llm = GPTGenerator("gpt-4o-mini", context, "session_id")

    response = llm.get_response(query)
    response["context_creation_time"] = server_time
    return response
