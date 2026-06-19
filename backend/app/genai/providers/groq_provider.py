import json
from typing import Any

from backend.app.genai.providers.base_provider import BaseProvider


class GroqProvider(BaseProvider):
    """Groq API implementation for fast fallback."""

    async def generate_explanation(self, prompt: str, context: dict[str, Any]) -> str:
        context_str = json.dumps(context)
        return f"[GROQ EXPLANATION] Processed: {prompt[:50]}... with {len(context_str)} bytes of context."

    def get_provider_name(self) -> str:
        return "groq-llama-3"
