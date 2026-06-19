import json
from typing import Any

from backend.app.genai.providers.base_provider import BaseProvider


class GeminiProvider(BaseProvider):
    """Google Gemini 2.5 Flash implementation."""

    async def generate_explanation(self, prompt: str, context: dict[str, Any]) -> str:
        # In a real setup, this would use google-genai SDK
        # For the hackathon, we simulate the output deterministically if live fails
        # or we just simulate the SDK call format
        context_str = json.dumps(context)
        return f"[GEMINI EXPLANATION] Processed: {prompt[:50]}... with {len(context_str)} bytes of context."

    def get_provider_name(self) -> str:
        return "gemini-2.5-flash"
