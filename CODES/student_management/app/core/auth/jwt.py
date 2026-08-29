from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
import jwt


SECRET_KEY = "Xs_8e1Yp5G4"  # 生产环境建议使用环境变量管理"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24小时过期


async def create_access_token(user_id: int, user_name: str):
    exp = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = {
        "sub": str(user_id),
        "username": user_name,
        "exp": exp,
    }
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    return token


async def verify_token(token: str):
    pass
