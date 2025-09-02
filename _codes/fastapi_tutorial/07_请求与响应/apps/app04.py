from fastapi import APIRouter, Form

app04 = APIRouter()


@app04.post("/register")
async def register(
    username: str = Form(..., min_length=8, max_length=8, pattern="[a-zA-Z]{8}"),
    password: str = Form(..., min_length=8, max_length=8, pattern="[0-9]{8}"),
):
    print(f"username = {username}, password = {password}")
    # 注册，实现数据库添加操作...
    return {"username": username}
