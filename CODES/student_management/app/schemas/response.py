from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar("T")


class BaseResponse(BaseModel, Generic[T]):
    """
    通用返回数据
    """

    code: int = 200
    msg: str = "success"
    data: Optional[T] = None
