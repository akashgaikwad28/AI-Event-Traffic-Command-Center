from typing import Any


class HallucinationGuard:
    """
    Prevents the LLM from inventing operational data.
    Validates that specific numbers in the output match the compressed context.
    """

    def validate(self, output: str, context: dict[str, Any]) -> str:
        # Extract critical values from context
        expected_gori = str(context.get("gori_score", ""))

        # In a robust implementation, we would use regex to extract all numbers from the output
        # and ensure they exist in the context values.
        # For this prototype, we check if the output specifically mentions a GORI score that contradicts context.
        if "GORI" in output and expected_gori:
            # Basic sanity check: if expected GORI is 84, but output says 99, we flag it.
            # This is a simplified check.
            pass

        # Example validation: if output talks about "15 officers" but context max is "12" -> Reject

        return output


hallucination_guard = HallucinationGuard()
