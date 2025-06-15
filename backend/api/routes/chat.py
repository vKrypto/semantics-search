from pathlib import Path

from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from application.services.chat_service import ChatService
from core.logging.logger import logger
from domain.models.chat import ChatRequest, ChatResponse
from infrastructure.llm.factory import LLMFactory
from infrastructure.search import HybridSearchStrategy

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
    responses={404: {"description": "Not found"}},
)

# Mount templates
templates_path = Path(__file__).parent.parent.parent / "templates"
templates = Jinja2Templates(directory=str(templates_path))


async def get_chat_service() -> ChatService:
    """Dependency to get chat service instance."""
    llm_provider = LLMFactory.create_provider()
    search_strategy = HybridSearchStrategy()
    return ChatService(llm_provider, search_strategy)


@router.get("/")
async def get_chat_interface(request: Request):
    """Get the chat interface template."""
    return templates.TemplateResponse("chat.html", {"request": request})


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest, chat_service: ChatService = Depends(get_chat_service)) -> ChatResponse:
    """Process a chat request."""
    logger.info(f"Received chat request: {request.query}")
    return await chat_service.process_chat_request(request)
