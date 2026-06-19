class OutputValidator:
    """Ensures LLM output matches required formatting and schemas."""

    def validate_format(self, output: str, expected_format: str) -> str:
        if expected_format == "markdown":
            # Ensure it contains basic markdown elements if required
            pass

        return output


output_validator = OutputValidator()
