from typing import Any

from backend.app.genai.context.context_compressor import context_compressor


class ContextBuilder:
    """
    Aggregates contexts from analytics, prediction, optimization, and simulation.
    Then passes them through the ContextCompressor.
    """

    def build_context(self, source_data: dict[str, Any]) -> dict[str, Any]:
        # 1. Gather
        # In a real system, this might fetch from DB or services if source_data is just an ID.
        # Here we assume source_data contains the necessary nested objects.

        # 2. Compress
        compressed_context = context_compressor.compress(source_data)
        return compressed_context


context_builder = ContextBuilder()
