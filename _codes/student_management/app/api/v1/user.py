from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.response import BaseResponse
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.core.database import get_db
from app.services.user import UserService

router = APIRouter()


@router.post("/register", summary="用户注册")
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return BaseResponse(data=await UserService.create_user(db, user))


@router.post("/login", summary="用户登录")
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    return BaseResponse(data=await UserService.login(db, user))


@router.post("/info", summary="用户信息", response_model=UserResponse)
async def info(db: AsyncSession = Depends(get_db)):
    return BaseResponse(data=await UserService.info(db))
