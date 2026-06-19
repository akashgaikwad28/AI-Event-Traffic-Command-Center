from typing import Any

from backend.app.genai.context.context_compressor import context_compressor
from backend.app.genai.prompts.executive_prompts import REPORT_PROMPT
from backend.app.genai.providers.provider_router import provider_router


class ReportService:
    """Generates structured Markdown reports based on specific data inputs."""

    async def generate_report(self, report_type: str, raw_data: dict[str, Any]) -> str:
        # Compress the input data
        context = context_compressor.compress(raw_data)

        # Inject report type into the prompt
        prompt = REPORT_PROMPT.format(context=context)
        prompt += (
            f"\n\nREPORT TYPE: {report_type}\nEnsure the output is valid Markdown."
        )

        # Generate via Provider Router
        markdown_report, _ = await provider_router.generate(prompt, context)

        return markdown_report


report_service = ReportService()
