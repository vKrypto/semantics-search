from abc import ABC, abstractmethod
from typing import Any, Dict, List


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    async def generate_text(self, prompt: str, **kwargs) -> str:
        """Generate text from the LLM."""
        pass

    @abstractmethod
    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for the given texts."""
        pass

    @abstractmethod
    async def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Chat with the LLM using a list of messages."""
        pass

    @abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the model being used."""
        pass
