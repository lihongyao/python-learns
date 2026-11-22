from fastapi import APIRouter
from app.api.v1.users import router as users_router
from app.api.v1.works import router as works_router

router = APIRouter()

router.include_router(users_router, prefix="/users", tags=["用户相关"])
router.include_router(works_router, prefix="/works", tags=["作品管理"])
