import os
import uuid
from typing import Dict, List, Optional

from openai import OpenAI

from core.config.settings import get_settings
from core.logging.logger import logger
from domain.interfaces.llm import LLMProvider


class OpenAIProvider(LLMProvider):
    """OpenAI LLM provider implementation."""

    def __init__(self, model_name: str = "gpt-4", session_id: Optional[str] = None):
        """Initialize the OpenAI provider.

        Args:
            model_name: The OpenAI model to use
            session_id: Optional session ID for conversation history
        """
        settings = get_settings()
        if not settings.OPENAI_API_KEY:
            raise EnvironmentError("OPENAI_API_KEY not found in environment variables")

        self.model_name = model_name
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.session_id = session_id or str(uuid.uuid4())
        self._conversation_history: List[Dict[str, str]] = []
        logger.info(f"Initialized OpenAI provider with model: {model_name}")

    async def generate_text(self, prompt: str, **kwargs) -> str:
        """Generate text from the LLM.

        Args:
            prompt: The prompt to generate text from
            **kwargs: Additional arguments for the completion

        Returns:
            Generated text
        """
        try:
            response = await self.client.chat.completions.create(
                model=self.model_name, messages=[{"role": "user", "content": prompt}], **kwargs
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating text: {str(e)}")
            raise

    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for the given texts.

        Args:
            texts: List of texts to generate embeddings for

        Returns:
            List of embeddings
        """
        try:
            response = await self.client.embeddings.create(model="text-embedding-ada-002", input=texts)
            return [embedding.embedding for embedding in response.data]
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise

    async def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Chat with the LLM using a list of messages.

        Args:
            messages: List of message dictionaries with role and content
            **kwargs: Additional arguments for the chat completion

        Returns:
            The model's response
        """
        try:
            # Add system message if not present
            if not any(msg["role"] == "system" for msg in messages):
                messages.insert(0, {"role": "system", "content": "You are a helpful AI assistant."})

            # Add conversation history
            full_messages = self._conversation_history + messages

            response = await self.client.chat.completions.create(
                model=self.model_name, messages=full_messages, **kwargs
            )

            # Update conversation history
            self._conversation_history = full_messages + [
                {"role": "assistant", "content": response.choices[0].message.content}
            ]

            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error in chat: {str(e)}")
            raise

    def get_model_info(self) -> Dict[str, str]:
        """Get information about the model being used.

        Returns:
            Dictionary containing model information
        """
        return {"provider": "openai", "model": self.model_name, "session_id": self.session_id}
