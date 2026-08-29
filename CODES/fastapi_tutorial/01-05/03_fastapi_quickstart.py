from fastapi import FastAPI
import uvicorn


app = FastAPI()


@app.get("/")
async def home():
    return {"message": "Hello, World!"}


if __name__ == "__main__":
    uvicorn.run("03_fastapi_quickstart:app", port=8080, reload=True)
