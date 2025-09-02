from fastapi import APIRouter
from typing import Union, Optional
from pydantic import BaseModel, Field, field_validator
from datetime import date
from typing import List

app03 = APIRouter()


class Addr(BaseModel):
    province: str
    city: str


class User(BaseModel):
    # name: str = "root"
    name: str
    age: int = Field(default=0, ge=0, le=100)
    birth: Union[date, None] = None
    friends: List[int] = []
    phone: str = Field(pattern=r"^1", min_length=11, max_length=11)
    description: Optional[str] = None
    addr: Addr  # 类型嵌套

    # 终极大招
    @field_validator("name")  # 必须添加
    @classmethod
    def check_name(cls, name: str):
        if name.isalpha():
            return name
        raise ValueError("name must be alpha.")


class Data(BaseModel):
    data: List[User]


@app03.post("/user")
async def user(user: User):
    print(user, type(user))
    print(f"user.name >>> {user.name}")
    print(user.model_dump())
    return user


@app03.post("/data")
async def data(user: Data):
    return user
