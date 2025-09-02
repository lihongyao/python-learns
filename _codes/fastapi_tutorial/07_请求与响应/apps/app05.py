import os
from fastapi import APIRouter, File, UploadFile
from typing import List

app05 = APIRouter()


# file: bytes = File()：适合小文件上传
@app05.post("/file")
async def file(file: bytes = File()):
    return {"file_size": len(file)}


@app05.post("/multiFiles")
async def multi_files(files: List[bytes] = File()):
    return {"file_sizes": [len(file) for file in files]}


# 最佳示例
os.makedirs("images", exist_ok=True)


# file: UploadFile：适合大文件上传
@app05.post("/uploadFile")
async def upload_file(file: UploadFile):

    # 文件保存
    path = os.path.join("images", file.filename)
    with open(path, "wb") as f:
        # 使用chunk方式写入（适合大文件）
        while content := await file.read(1024 * 1024):  # 每次读取1MB
            f.write(content)
    return {"file": file.filename}


@app05.post("/uploadFiles")
async def upload_files(files: List[UploadFile]):
    # ...
    return {"names": [file.filename for file in files]}
