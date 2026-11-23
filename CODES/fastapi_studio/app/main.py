from pathlib import Path
import sys

# 兼容 IDE 或命令行直接执行 app/main.py。
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if __package__ in (None, ""):
    sys.path.insert(0, str(PROJECT_ROOT))

# 必须先设置模块搜索路径，再导入项目中的 app 包。
from app.api.v1 import router as api_router
from fastapi import FastAPI
import uvicorn

app = FastAPI(
    title="示例 API",
    description="用于学习 FastAPI 的接口示例",
    version="1.0.0",
)


app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run("app.main:app", port=8000, reload=True, reload_dirs=[str(PROJECT_ROOT)])
