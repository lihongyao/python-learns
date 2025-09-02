from datetime import datetime
from typing import Optional
from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.dialects.postgresql import TIMESTAMP
from app.core.database import Base


class User(AsyncAttrs, Base):
    """
    用户数据模型（SQLAlchemy 2.0语法）
    继承 AsyncAttrs 支持异步属性访问
    继承 Base 作为声明式模型基类
    """

    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    real_name: Mapped[Optional[str]] = mapped_column(
        String(20), server_default="佚名", nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.timezone("UTC", func.now())
    )

    def __repr__(self):
        return (
            f"User(id={self.id}, username={self.username}, real_name={self.real_name})"
        )
