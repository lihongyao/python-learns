from fastapi import FastAPI
import uvicorn


app = FastAPI()


@app.post(
    "/login",
    tags=["登录相关"],
    summary="登录接口",
    description="详情信息",
    response_description="响应描述信息",
    deprecated=True,
)
async def test():
    return {"method": "items 数据"}


if __name__ == "__main__":
    uvicorn.run("05_路径操作装饰器参数:app", port=8080, reload=True)
