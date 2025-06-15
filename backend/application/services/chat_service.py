import time
from typing import Optional

from core.logging.logger import logger
from domain.interfaces.llm import LLMProvider
from domain.interfaces.search import SearchStrategy
from domain.models.chat import ChatRequest, ChatResponse, ChatSession, Message


class ChatService:
    """Service for handling chat operations."""

    def __init__(self, llm_provider: LLMProvider, search_strategy: SearchStrategy):
        """Initialize the chat service.

        Args:
            llm_provider: The LLM provider to use for generating responses
            search_strategy: The search strategy to use for context retrieval
        """
        self.llm_provider = llm_provider
        self.search_strategy = search_strategy
        logger.info("Initialized chat service")

    async def process_chat_request(self, request: ChatRequest) -> ChatResponse:
        """Process a chat request and generate a response.

        Args:
            request: The chat request from the user

        Returns:
            Chat response with generated text and context
        """
        start_time = time.time()

        # Get context using search
        context_start = time.time()
        search_results = await self.search_strategy.search(request.query)
        context_time = (time.time() - context_start) * 1000

        # Generate response using LLM
        messages = [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": request.query},
        ]

        response = await self.llm_provider.chat(messages)

        # Calculate total processing time
        total_time = (time.time() - start_time) * 1000

        logger.info(f"Processed chat request in {total_time:.2f}ms")

        return ChatResponse(
            response=response,
            context=[result.content for result in search_results],
            server_time=total_time,
            context_creation_time=context_time,
        )

    async def get_chat_session(self, session_id: str) -> Optional[ChatSession]:
        """Get a chat session by ID.

        Args:
            session_id: The session ID

        Returns:
            The chat session if found, None otherwise
        """
        # TODO: Implement session retrieval from storage
        return None

    async def create_chat_session(self) -> ChatSession:
        """Create a new chat session.

        Returns:
            The newly created chat session
        """
        # TODO: Implement session creation
        return ChatSession(session_id="new_session")
