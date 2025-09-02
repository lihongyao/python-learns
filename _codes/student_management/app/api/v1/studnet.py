from fastapi import APIRouter

from app.schemas.response import BaseResponse
from app.services import student as student_service

router = APIRouter()


@router.get("/")
async def read_students():
    data = await student_service.get_students()
    return BaseResponse(data=data)
