from typing import Generic, List, TypeVar ,Optional,Any
from pydantic import BaseModel

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    limit: int
    total_pages: int


class MessageResponse(BaseModel, Generic[T]):
    message: str
    data: Optional[T] = None
    success: bool = True
    status: int = 200


