import json
import os
import httpx
from typing import Any

from backend.app.genai.providers.base_provider import BaseProvider
from backend.app.core.config import get_settings

class GroqProvider(BaseProvider):
    """Real Groq API implementation for ultra-fast inference."""

    def __init__(self):
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"

    async def generate_explanation(self, prompt: str, context: dict[str, Any]) -> str:
        settings = get_settings()
        api_key = settings.groq_api_key or os.getenv("GROQ_API_KEY")
        
        print(f"DEBUG: API Key check -> Settings: {'[SET]' if settings.groq_api_key else '[MISSING]'}, Env: {'[SET]' if os.getenv('GROQ_API_KEY') else '[MISSING]'}")

        if not api_key:
            raise Exception("API_KEY_MISSING")

        context_str = json.dumps(context)
        
        system_prompt = f"""You are the GridWise Operational Intelligence Copilot. 
        You provide strictly operational advice to traffic command centers.
        Do not use bolding or markdown headers that clutter the UI.
        Base your answer STRICTLY on this Context Data:
        {context_str}
        """

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2,
            "max_tokens": 512
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(self.base_url, headers=headers, json=payload, timeout=8.0)
            
            if response.status_code == 401:
                print("❌ GROQ API ERROR: Unauthorized (Invalid API Key)")
                raise Exception("API_KEY_INVALID")
            elif response.status_code != 200:
                print(f"❌ GROQ API ERROR: {response.text}")
                raise Exception(f"Groq API Error: {response.text}")
                
            data = response.json()
            print("✅ GROQ API SUCCESS: Explanation generated successfully via llama3-8b-8192")
            return data["choices"][0]["message"]["content"].strip()

    def get_provider_name(self) -> str:
        return "groq-llama-3"
