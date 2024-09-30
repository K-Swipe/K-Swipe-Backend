from pydantic import BaseModel
from typing import Generic, TypeVar, Optional, List

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    success: bool
    message: Optional[str] = None
    data: T
