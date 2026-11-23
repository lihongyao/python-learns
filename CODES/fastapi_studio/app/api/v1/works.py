from fastapi import APIRouter
from enum import StrEnum

router = APIRouter()


class WorksCategoryEnum(StrEnum):
    gallery = "gallery"
    video = "video"
    writing = "writing"


@router.get("/", summary="作品列表")
async def list(category: WorksCategoryEnum):
    return {"code": 200, "data": {"items": [1, 2, 3]}, "msg": "success"}


@router.get("/{id}", summary="作品详情")
async def details(id: int):
    return {"code": 200, "data": {"id": id}, "msg": "success"}
