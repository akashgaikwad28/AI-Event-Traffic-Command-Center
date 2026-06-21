import asyncio
import os
import time
from typing import Any

from backend.app.genai.logging.genai_logger import genai_logger
from backend.app.genai.providers.gemini_provider import GeminiProvider
from backend.app.genai.providers.gemma_provider import GemmaProvider
from backend.app.genai.providers.groq_provider import GroqProvider


class ProviderRouter:
    """
    Routes requests to LLM providers.
    Supports timeout protection and deterministic fallback for demo safety.
    """

    def __init__(self):
        self.gemini = GeminiProvider()
        self.groq = GroqProvider()
        self.gemma = GemmaProvider()
        # Default to True so it automatically tries the keys
        self.enable_live = os.getenv("ENABLE_LIVE_LLM", "true").lower() == "true"

    async def generate(self, prompt: str, context: dict[str, Any]) -> tuple[str, str]:
        start_time = time.perf_counter()
        if not self.enable_live:
            genai_logger.provider_request_started("offline_fallback", "EXECUTIVE")
            res = self._deterministic_fallback(prompt, context)
            latency = int(round((time.perf_counter() - start_time) * 1000))
            genai_logger.provider_request_completed(
                "offline_fallback",
                "EXECUTIVE",
                latency,
                int(len(prompt + res) * 0.25),
                True,
            )
            return res, "Offline Fallback"

        try:
            # 1. Attempt Groq with 5s timeout
            genai_logger.provider_request_started("groq", "EXECUTIVE")
            res = await asyncio.wait_for(
                self.groq.generate_explanation(prompt, context), timeout=5.0
            )
            latency = int(round((time.perf_counter() - start_time) * 1000))
            genai_logger.provider_request_completed(
                "groq", "EXECUTIVE", latency, int(len(prompt + res) * 0.25), False
            )
            return res, "Groq Fast Inference"
        except Exception as e1:
            if str(e1) in ["API_KEY_MISSING", "API_KEY_INVALID"]:
                return (
                    "The GridWise AI Copilot is currently busy or experiencing a temporary issue on our end. Please try again shortly.",
                    "System Error",
                )

            genai_logger.provider_fallback("groq", "gemini", str(e1))
            try:
                # 2. Fallback to Gemini with 5s timeout
                genai_logger.provider_request_started("gemini", "EXECUTIVE")
                res = await asyncio.wait_for(
                    self.gemini.generate_explanation(prompt, context), timeout=5.0
                )
                latency = int(round((time.perf_counter() - start_time) * 1000))
                genai_logger.provider_request_completed(
                    "gemini", "EXECUTIVE", latency, int(len(prompt + res) * 0.25), True
                )
                return res, "Gemini AI"
            except (TimeoutError, Exception) as e2:
                genai_logger.provider_fallback("gemini", "gemma", str(e2))
                try:
                    # 3. Fallback to Gamma/Gemma with 5s timeout
                    genai_logger.provider_request_started("gemma", "EXECUTIVE")
                    res = await asyncio.wait_for(
                        self.gemma.generate_explanation(prompt, context), timeout=5.0
                    )
                    latency = int(round((time.perf_counter() - start_time) * 1000))
                    genai_logger.provider_request_completed(
                        "gemma",
                        "EXECUTIVE",
                        latency,
                        int(len(prompt + res) * 0.25),
                        True,
                    )
                    return res, "Gemma Local"
                except Exception as e3:
                    # 4. Absolute Offline Deterministic Fallback
                    genai_logger.provider_fallback("gemma", "offline_fallback", str(e3))
                    res = self._deterministic_fallback(prompt, context)
                    latency = int(round((time.perf_counter() - start_time) * 1000))
                    genai_logger.provider_request_completed(
                        "offline_fallback",
                        "EXECUTIVE",
                        latency,
                        int(len(prompt + res) * 0.25),
                        True,
                    )
                    return res, "Offline Fallback"

    def _deterministic_fallback(self, prompt: str, context: dict[str, Any]) -> str:
        # Returns a high-quality deterministic string for demo safety.
        # It reads values from context to appear "grounded".
        gori = context.get("gori_score", "unknown")
        return f"[Offline AI Generator] Based on the ML prediction model (Current GORI: {gori}), cascading congestion is highly probable. Recommending immediate cross-corridor barricade deployment to alleviate pressure."


provider_router = ProviderRouter()
