from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


# 基础模型（共享字段）
class UserBase(BaseModel):
    # ... 表示必填字段
    username: str = Field(..., min_length=11, max_length=11, pattern=r"^(1[3-9]\d{9})$")
    real_name: Optional[str] = Field(None, max_length=20)


# 注册请求模型
class UserCreate(UserBase):
    password: str = Field(..., min_length=4, max_length=20)


# 登录请求模型
class UserLogin(BaseModel):
    username: str = Field(..., min_length=11, max_length=11)
    password: str = Field(..., min_length=6, max_length=100)


class UserResponse(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")},
    )
