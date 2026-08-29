from fastapi import APIRouter

app01 = APIRouter()


# 路由匹配


# @app01.get("/user/1")
# def get_user():
#     return {"user_id": "root user"}


@app01.get("/user/{user_id}")
def get_user(user_id):
    print(user_id, type(user_id))
    return {"user_id": user_id}


@app01.get("/articles/{id}")
def get_article(id: int):
    print(f"{id} {type(id)}")
    return {"article_id": id}
