from abc import ABC, abstractmethod
from typing import Any


class BaseProvider(ABC):
    """Abstract base class for all LLM providers."""

    @abstractmethod
    async def generate_explanation(self, prompt: str, context: dict[str, Any]) -> str:
        """Generates a text response given a prompt and compressed context."""
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        """Returns the name of the provider (e.g., 'Gemini', 'Groq')."""
        pass
