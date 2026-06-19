import asyncio
import os
from typing import Any

import requests

from backend.app.genai.providers.base_provider import BaseProvider


class GemmaProvider(BaseProvider):
    def __init__(self):
        self.api_key = os.getenv("GEMMA_API_KEY")

    def _call_nvidia_api(self, prompt: str) -> str:
        invoke_url = "https://integrate.api.nvidia.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
        }
        payload = {
            "model": "google/diffusiongemma-2b-it",  # standardizing model name based on Nvidia spec
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1024,
            "temperature": 0.7,
            "top_p": 0.95,
            "stream": False,
        }

        # User specified google/diffusiongemma-26b-a4b-it but standard is often different, keeping their exact requested model just in case:
        payload["model"] = (
            "google/diffusiongemma-2b-it"
            if "2b" in prompt
            else "google/diffusiongemma-2b-it"
        )
        # Overriding with their exact string to be completely safe:
        payload["model"] = "google/diffusiongemma-26b-a4b-it"
        payload["chat_template_kwargs"] = {"enable_thinking": True}

        response = requests.post(invoke_url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()

        data = response.json()
        return data["choices"][0]["message"]["content"]

    async def generate_explanation(self, prompt: str, context: dict[str, Any]) -> str:
        if not self.api_key:
            raise ValueError("GEMMA_API_KEY not set in .env")

        # Run the synchronous requests library in a background thread to prevent blocking FastAPI
        response_text = await asyncio.to_thread(self._call_nvidia_api, prompt)
        return response_text

    def get_provider_name(self) -> str:
        return "diffusiongemma-26b-a4b-it"
