from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:8080",
]


app.add_middleware(
    CORSMiddleware,
    # 一个允许跨域请求的源列，可以使用 ['*'] 允许任何源
    allow_origins=origins,
    # 指示跨域请求支持 cookies。默认是 False。另外，允许凭证时 allow_origins 不能设定为 ['*']，必须指定源
    allow_credentials=True,
    # 一个允许跨域请求的 HTTP 方法列表
    allow_methods=["*"],
    # 一个允许跨域请求的 HTTP 请求头列表
    allow_headers=["*"],
)


@app.get("/")
async def main():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)
