from fastapi import APIRouter

router = APIRouter()


@router.get("/", summary="作品列表")
async def list_works():
    return {"code": 200, "data": [1, 2, 3], "msg": "success"}


@router.get("/{id}", summary="作品详情")
async def details(id: int):
    return {"code": 200, "data": {"id": id}, "msg": "success"}
