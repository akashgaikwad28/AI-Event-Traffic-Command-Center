from typing import Any

from backend.app.genai.context.context_compressor import context_compressor
from backend.app.genai.prompts.narrator_prompts import NARRATOR_PROMPT
from backend.app.genai.providers.provider_router import provider_router


class DemoNarratorService:
    """Generates the dramatic, judge-wowing narration for the 1-click executive demo."""

    async def generate_narration(self, simulation_result: dict[str, Any]) -> str:
        # Compress the simulation output
        context = context_compressor.compress(
            {
                "simulation": simulation_result,
                "gori_score": 81.0,
                "incidents": [{"type": "accident"}],
            }
        )

        # Format prompt
        prompt = NARRATOR_PROMPT.format(context=context)

        # Generate via Provider
        narration, _ = await provider_router.generate(prompt, context)

        return narration


demo_narrator_service = DemoNarratorService()
