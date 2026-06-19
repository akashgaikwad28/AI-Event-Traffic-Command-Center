from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    page: int
    page_size: int
    total: int


def paginate(
    items: list[T], total: int, page: int, page_size: int
) -> PaginatedResponse[T]:
    return PaginatedResponse(
        items=items,
        page=page,
        page_size=page_size,
        total=total,
    )
