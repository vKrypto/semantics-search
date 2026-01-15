from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.templating import Jinja2Templates

from application.services.chat_service import ChatService
from core.config.settings import AppSettings
from core.logging.logger import logger
from domain.models.chat import ChatRequest, ChatResponse, ChatSession
from infrastructure.llm.factory import LLMFactory
from infrastructure.search import SearchStrategyFactory

router = APIRouter(
    prefix=f"{AppSettings.VERSION_STR}/chat",
    tags=["Chat"],
    responses={404: {"description": "Not found"}},
)

# Mount templates
templates_path = Path(__file__).parent.parent.parent / "templates"
templates = Jinja2Templates(directory=str(templates_path))


async def get_chat_service(session_id: str = None) -> ChatService:
    """Dependency to get chat service instance.
    
    Args:
        session_id: Optional session ID for conversation continuity
    """
    llm_provider = LLMFactory.create_provider(session_id=session_id)
    search_strategy = SearchStrategyFactory.create_strategy()
    return ChatService(llm_provider, search_strategy)


@router.get("/")
async def get_chat_interface(request: Request):
    """Get the chat interface template."""
    return templates.TemplateResponse("chat.html", {"request": request})


@router.post("/sessions", response_model=ChatSession)
async def create_session(chat_service: ChatService = Depends(get_chat_service)) -> ChatSession:
    """Create a new chat session.
    
    Returns:
        The newly created chat session with a generated session_id
    """
    logger.info("Creating new chat session")
    return await chat_service.create_chat_session()


@router.get("/sessions/{session_id}", response_model=ChatSession)
async def get_session(
    session_id: str,
    chat_service: ChatService = Depends(get_chat_service)
) -> ChatSession:
    """Get a chat session by ID.
    
    Args:
        session_id: The session ID to retrieve
        
    Returns:
        The chat session if found
        
    Raises:
        HTTPException: If session not found
    """
    logger.info(f"Retrieving chat session: {session_id}")
    session = await chat_service.get_chat_session(session_id)
    
    if session is None:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
    
    return session


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """Handle chat requests with session management.
    
    Args:
        request: Chat request containing query and optional session_id
        
    Returns:
        Chat response with generated text, context, and session_id
    """
    logger.info(f"Received chat request: {request.query}, session_id: {request.session_id}")
    
    # Create service with session_id from request
    chat_service = await get_chat_service(session_id=request.session_id)
    
    return await chat_service.process_chat_request(request)