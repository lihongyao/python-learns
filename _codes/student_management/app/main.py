import sys
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent.parent))


import uvicorn
from typing import Annotated
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from app.core.database import lifespan
from app.api.v1 import router as api_router


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI(lifespan=lifespan)
app.include_router(api_router, prefix="/api")


@app.get("/")
async def root(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
