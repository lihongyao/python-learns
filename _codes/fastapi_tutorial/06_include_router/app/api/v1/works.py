from fastapi import APIRouter


router = APIRouter(prefix="/works")


@router.get("/", summary="作品列表")
async def list():
    return {"code": 200, "data": [1, 2, 3], "msg": "success"}


@router.get("/{id}", summary="作品详情")
async def details():
    return {"code": 200, "data": {"id": 1}, "msg": "success"}
