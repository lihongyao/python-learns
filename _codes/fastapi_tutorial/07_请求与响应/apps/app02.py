from fastapi import APIRouter
from typing import Union, Optional

app02 = APIRouter()


# @app02.get("/job")
# async def get_jobs(kd, xl, gj):
#     # 基于 kd, xl, gj 数据库查询岗位信息（拉勾网）
#     return {
#         "kd": kd,
#         "xl": xl,
#         "gj": gj,
#     }


@app02.get("/job/{kd}")
async def get_jobs(kd: str, xl: Union[str, None] = None, gj: Optional[str] = None):
    # 基于 kd, xl, gj 数据库查询岗位信息（拉勾网）
    return {
        "kd": kd,
        "xl": xl,
        "gj": gj,
    }
