from fastapi import APIRouter


router = APIRouter(prefix="/user")


@router.post("/register", summary="用户注册")
async def register():
    return {"code": 200, "data": None, "msg": "注册成功"}


@router.post("/login", summary="用户登录")
async def login():
    return {"code": 200, "data": None, "msg": "登录成功"}
