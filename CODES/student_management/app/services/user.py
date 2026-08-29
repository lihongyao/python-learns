from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.core.auth.jwt import create_access_token
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import hashlib


# 生成随机密钥，终端输入：openssl rand -hex 32
SECRET_KEY = "c818556f676d39c9785ea8f48431d747b9f0eb0a917bd89e105aeeebb95c78b4"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24小时过期


class UserService:
    @staticmethod
    async def create_user(db: AsyncSession, form_data: UserCreate):
        # 检查用户是否存在
        result = await db.execute(
            select(User).where(User.username == form_data.username)
        )
        db_user = result.scalars().first()

        if db_user:
            raise HTTPException(status_code=400, detail="用户已注册")

        # 处理密码
        user = form_data.model_dump(exclude={"password"})
        user["password"] = hashlib.sha256(form_data.password.encode()).hexdigest()

        # 写入数据库
        row = User(**user)
        db.add(row)
        await db.commit()
        await db.refresh(row)

    @staticmethod
    async def login(db, form_data: UserLogin):
        # 检查用户是否存在
        result = await db.execute(
            select(User).where(User.username == form_data.username)
        )
        db_user = result.scalars().first()

        if not db_user:
            raise HTTPException(status_code=400, detail="用户不存在")

        # 检查密码
        if db_user.password != hashlib.sha256(form_data.password.encode()).hexdigest():
            raise HTTPException(status_code=400, detail="密码错误")

        # jwt_token
        token = await create_access_token(db_user.id, db_user.username)

        return {"token": token}

    @staticmethod
    async def info(db):
        return {"name": "zansan"}
