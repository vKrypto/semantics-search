import os
import uuid
import asyncio
from typing import Dict, List, Optional

import cohere

from core.config.settings import AppSettings
from core.logging.logger import logger
from core.utils.conversation_history import (
    load_conversation_history,
    save_conversation_history,
    merge_with_history,
)
from domain.interfaces.llm import LLMProvider
import httpx
import json


class CohereProvider(LLMProvider):
    """Cohere LLM provider implementation.

    Implements the same LLMProvider interface used by other providers in the
    project (e.g. OpenAIProvider). Methods are async to match the interface;
    since the official Cohere Python SDK is synchronous we call it via
    ``asyncio.to_thread`` to avoid blocking the event loop.
    """

    def __init__(self, model_name: str = "command-a-03-2025", session_id: Optional[str] = None):
        """Initialize the Cohere provider.

        Args:
            model_name: The Cohere model to use for generation
            session_id: Optional session ID for conversation history

        Raises:
            EnvironmentError: If `COHERE_API_KEY` is not set in settings
        """
        if not AppSettings.COHERE_API_KEY:
            raise EnvironmentError("COHERE_API_KEY not found in environment variables")

        self.model_name = model_name

        # Legacy client (v1) - used for generate/embed if available
        try:
            self.client = cohere.Client(AppSettings.COHERE_API_KEY)
        except Exception:
            self.client = None

        # ClientV2 is required for the v2 Chat API
        ClientV2 = getattr(cohere, "ClientV2", None)
        if ClientV2 is None:
            raise EnvironmentError("Cohere ClientV2 is required for chat interactions. Please install a Cohere SDK that exposes ClientV2.")
        try:
            self.client_v2 = ClientV2(api_key=AppSettings.COHERE_API_KEY)
        except Exception as e:
            raise EnvironmentError(f"Failed to initialize Cohere ClientV2: {e}")

        self.session_id = session_id or str(uuid.uuid4())
        self._conversation_history: List[Dict[str, str]] = load_conversation_history(
            "cohere", self.session_id
        )
        logger.info(f"Initialized Cohere provider with model: {model_name}, session_id: {self.session_id}")

    async def generate_text(self, prompt: str, **kwargs) -> str:
        """Generate text from the Cohere model.

        Args:
            prompt: The prompt to generate text from
            **kwargs: Additional keyword arguments passed to Cohere's generate()

        Returns:
            Generated text (first generation returned by Cohere)
        """
        try:
            # Cohere SDK is synchronous; run in thread to avoid blocking event loop
            def _call():
                return self.client.generate(model=self.model_name, prompt=prompt, **kwargs)

            response = await asyncio.to_thread(_call)
            # response.generations is a list; return first generation text
            return response.generations[0].text
        except Exception as e:
            logger.error(f"Error generating text with Cohere: {str(e)}")
            raise

    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for the given texts using Cohere.

        Args:
            texts: List of texts to generate embeddings for

        Returns:
            A list of float vectors (embeddings) corresponding to the input texts
        """
        try:
            def _call():
                return self.client.embed(model="embed-english-small", texts=texts)

            response = await asyncio.to_thread(_call)
            return response.embeddings
        except Exception as e:
            logger.error(f"Error generating embeddings with Cohere: {str(e)}")
            raise

    async def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Chat with the Cohere model using a list of messages.

        This method follows the same message-style interface as other providers:
        a list of dicts with 'role' and 'content'. Conversation history is loaded
        from Redis, merged with incoming messages, and saved back after the response.

        Args:
            messages: List of message dictionaries with role and content
            **kwargs: Additional args passed to Cohere's chat call

        Returns:
            The model's response text
        """
        try:
            # Reload persisted history each request (provider objects are created per request today)
            persisted = load_conversation_history("cohere", self.session_id)
            full_messages = merge_with_history(persisted, messages)

            # Use Cohere v2 chat API exclusively
            def _call_chat_v2():
                return self.client_v2.chat(model=self.model_name, messages=full_messages, **kwargs)

            resp = await asyncio.to_thread(_call_chat_v2)

            # Parse response according to Cohere v2 chat docs: resp.message.content is a list
            assistant_text = resp.message.content[0].text

            # Update conversation history and save to Redis
            updated_history = full_messages + [{"role": "assistant", "content": assistant_text}]
            self._conversation_history = updated_history
            save_conversation_history("cohere", self.session_id, updated_history)

            return assistant_text
        except Exception as e:
            logger.error(f"Error in Cohere chat: {str(e)}")
            raise

    async def stream_chat(self, messages: List[Dict[str, str]], **kwargs):
        """Stream chat responses from Cohere v2 chat endpoint using SSE.

        Yields partial text chunks as strings. Conversation history is loaded from
        Redis and saved back after streaming completes.

        Args:
            messages: List of message dictionaries with role and content
            **kwargs: Additional args passed to Cohere's chat call

        Yields:
            Partial text chunks from the streaming response
        """
        # Reload persisted history for streaming
        persisted = load_conversation_history("cohere", self.session_id)
        full_messages = merge_with_history(persisted, messages)

        url = "https://api.cohere.com/v2/chat"
        headers = {
            "Authorization": f"Bearer {AppSettings.COHERE_API_KEY}",
            "Content-Type": "application/json",
        }

        payload = {"model": self.model_name, "messages": full_messages, "stream": True}
        # Merge additional kwargs into payload (allow overriding)
        payload.update(kwargs)

        # Accumulate full response text for saving to Redis
        full_response_text = ""

        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream("POST", url, headers=headers, json=payload) as resp:
                resp.raise_for_status()
                buffer = ""
                async for chunk in resp.aiter_bytes():
                    if not chunk:
                        continue
                    text_chunk = chunk.decode(errors="ignore")
                    buffer += text_chunk
                    # SSE events are separated by double newlines; parse lines beginning with 'data: '
                    while "\n\n" in buffer:
                        event, buffer = buffer.split("\n\n", 1)
                        for line in event.splitlines():
                            if line.startswith("data:"):
                                data = line[len("data:"):].strip()
                                if data == "[DONE]":
                                    # Save conversation history after streaming completes
                                    updated_history = full_messages + [{"role": "assistant", "content": full_response_text}]
                                    self._conversation_history = updated_history
                                    save_conversation_history("cohere", self.session_id, updated_history)
                                    return
                                try:
                                    obj = json.loads(data)
                                    # Try to extract message content pieces
                                    message = obj.get("message") or obj.get("output")
                                    if isinstance(message, dict):
                                        content = message.get("content")
                                        if isinstance(content, list):
                                            for part in content:
                                                if isinstance(part, dict) and part.get("type") == "text":
                                                    chunk_text = part.get("text")
                                                    if chunk_text:
                                                        full_response_text += chunk_text
                                                        yield chunk_text
                                                elif isinstance(part, str):
                                                    full_response_text += part
                                                    yield part
                                except Exception:
                                    # non-json data; yield raw
                                    full_response_text += data
                                    yield data
                
                # Save conversation history if streaming completed normally
                if full_response_text:
                    updated_history = full_messages + [{"role": "assistant", "content": full_response_text}]
                    self._conversation_history = updated_history
                    save_conversation_history("cohere", self.session_id, updated_history)

    def get_model_info(self) -> Dict[str, str]:
        """Get information about the configured model and session.

        Returns:
            Dictionary containing provider name, model and session id
        """
        return {"provider": "cohere", "model": self.model_name, "session_id": self.session_id}
