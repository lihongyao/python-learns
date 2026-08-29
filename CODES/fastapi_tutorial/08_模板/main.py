from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import uvicorn


# 实例化 FastAPI 对象
app = FastAPI()
# 实例化 jinjia2 对象，并将文件夹路径设置为以 templates 命名的文件夹
templates = Jinja2Templates(directory="templates")


@app.get("/index")
async def index(request: Request):
    name = "root"
    age = 32
    books = ["西游记", "红楼梦", "三国演义", "聊斋志异"]
    info = {"name": "张三", "age": 32, "gender": "男"}

    return templates.TemplateResponse(
        # 模板文件
        "index.html",
        # context 上下文对象
        {
            # 注意：返回模板响应时，必须有 request 键值对，且值为 Request 请求对象
            "request": request,
            "username": name,
            "age": age,
            "books": books,
            "info": info,
        },
    )


if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)
