from fastapi import APIRouter, Request

app06 = APIRouter()


@app06.get("/items")
async def items(request: Request):
    return {
        "请求URL": request.url,
        "请求IP": request.client.host,
        "请求宿主": request.headers.get("user-agent"),
        "cookies": request.cookies,
    }
