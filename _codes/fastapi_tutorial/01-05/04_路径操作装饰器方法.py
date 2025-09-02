from fastapi import FastAPI
import uvicorn


app = FastAPI()


@app.get("/get")
async def get_test():
    return {"method": "GET"}


@app.get("/post")
async def post_test():
    return {"method": "POST"}


@app.put("/put")
async def put_test():
    return {"method": "PUT"}


@app.put("/delete")
async def delete_test():
    return {"method": "DELETE"}


if __name__ == "__main__":
    uvicorn.run("04_路径操作装饰器方法:app", port=8080, reload=True)
