import time
import uuid
from datetime import datetime
from typing import Optional

from core.logging.logger import logger
from core.config.settings import AppSettings
from core.utils.conversation_history import load_conversation_history
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
        search_results = [item async for item in self.search_strategy.search(request.query)]
        context_time = (time.time() - context_start) * 1000

        # Generate response using LLM
        # Note: System message is handled by the LLM provider's _merge_with_history method
        messages = [
            {"role": "user", "content": request.query},
        ]

        response = await self.llm_provider.chat(messages)

        # Get session_id from the LLM provider (it may have generated a new one)
        model_info = self.llm_provider.get_model_info()
        session_id = model_info.get("session_id", "")

        # Calculate total processing time
        total_time = (time.time() - start_time) * 1000

        logger.info(f"Processed chat request in {total_time:.2f}ms for session: {session_id}")
        context = [item["value"]["value"] if isinstance(item["value"], dict) else item["value"] for item in search_results]

        return ChatResponse(
            session_id=session_id,
            response=response,
            context=context,
            server_time=total_time,
            context_creation_time=context_time,
        )

    async def get_chat_session(self, session_id: str) -> Optional[ChatSession]:
        """Get a chat session by ID.

        Loads the conversation history from Redis and converts it to a ChatSession object.

        Args:
            session_id: The session ID

        Returns:
            The chat session if found, None otherwise
        """
        # Get provider name from the LLM provider
        model_info = self.llm_provider.get_model_info()
        provider_name = model_info.get("provider", AppSettings.DEFAULT_LLM_PROVIDER)
        
        # Load conversation history from Redis using shared utility
        history = load_conversation_history(provider_name, session_id)
        
        if not history:
            # No history found - session doesn't exist or has expired
            logger.info(f"No conversation history found for session: {session_id}")
            return None
        
        # Convert Redis history format to Message objects
        # Filter out system messages for the ChatSession model (they're internal)
        messages = []
        created_at = None
        
        for msg_dict in history:
            role = msg_dict.get("role")
            content = msg_dict.get("content")
            
            # Skip system messages in the session view
            if role == "system":
                continue
            
            # Create Message object
            message = Message(
                role=role,
                content=content,
                timestamp=datetime.utcnow()  # Redis doesn't store timestamps, use current time
            )
            messages.append(message)
            
            # Use first message timestamp as created_at if not set
            if created_at is None:
                created_at = message.timestamp
        
        # If no non-system messages found, return None
        if not messages:
            return None
        
        return ChatSession(
            session_id=session_id,
            messages=messages,
            created_at=created_at or datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

    async def create_chat_session(self) -> ChatSession:
        """Create a new chat session.

        Generates a new session ID. The session will be persisted when the first
        message is sent via process_chat_request.

        Returns:
            The newly created chat session
        """
        session_id = str(uuid.uuid4())
        logger.info(f"Created new chat session: {session_id}")
        
        return ChatSession(
            session_id=session_id,
            messages=[],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )