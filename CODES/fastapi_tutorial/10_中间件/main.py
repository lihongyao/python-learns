from fastapi import FastAPI, Request, Response

# import uvicorn
import time

app = FastAPI()


# 定义中间件
@app.middleware("http")
async def m2(request: Request, call_next):

    # 请求代码块
    print("m2 request")
    start_time = time.perf_counter()

    # 响应代码块
    response: Response = await call_next(request)
    print("m2 response")
    end_time = time.perf_counter()
    response.headers["author"] = "LiHONGYAO"
    response.headers["X-Process-Time"] = str(end_time - start_time)

    return response


@app.middleware("http")
async def m1(request: Request, call_next):
    # 请求代码块
    print("m1 request")
    # 响应代码块
    response: Response = await call_next(request)
    print("m1 response")
    return response


# 定义路由
@app.get("/user")
async def get_user():
    print("get_user 函数执行")
    return {"user": "current user"}


@app.get("/item/{item_id}")
async def get_item(item_id: int):
    print("get_item 函数执行")
    return {"item_id": item_id}


# if __name__ == "__main__":
#     uvicorn.run("main:app", port=8080, reload=True)
