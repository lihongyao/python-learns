from fastapi import APIRouter
from app.api.v1.studnet import router as students_router
from app.api.v1.user import router as users_router

router = APIRouter()


router.include_router(users_router, prefix="/user", tags=["用户相关"])
router.include_router(students_router, prefix="/student", tags=["学生管理"])
