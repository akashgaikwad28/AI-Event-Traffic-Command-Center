from typing import Any


class BaseAPIException(Exception):
    def __init__(
        self,
        message: str,
        error_code: str,
        status_code: int = 400,
        details: Any = None,
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details
        super().__init__(self.message)

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"code={self.error_code}, "
            f"status={self.status_code}, "
            f"message={self.message})"
        )

    def __repr__(self) -> str:
        return self.__str__()
