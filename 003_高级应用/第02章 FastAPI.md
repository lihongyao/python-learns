# 概述

[HTTP 协议参考 ↪](https://www.cnblogs.com/ltyc/p/18664047)

[FastAPI ↪](https://fastapi.tiangolo.com/zh/) 是一个用于构建 API 的现代、高性能 Web 框架，使用 Python 并基于标准的类型提示。

[FastAPI ↪](https://fastapi.tiangolo.com/zh/) 是建立在 Starlette 和 Pydantic 基础上的。

Pydantic 是一个基于 Python 类型提示来定义数据验证、序列化和文档的库。

Starlette 是一种轻量级的 ASGI 框架/工具包，负责处理 Web 请求和响应。

> - [Starlette ↪](https://www.starlette.io/) 负责 Web 部分（asyncio）
> - [Pydantic ↪](https://docs.pydantic.dev/latest/) 负责数据部分（类型提示）

FastAPI 建立在 Starlette 和 Pydantic 之上，适合开发前后端分离的 API、自动化服务和微服务。

> 本章示例基于 [Python 3.14.7 ↪](https://www.python.org/downloads/release/python-3147/)，使用 Python 3.10+ 语法。

> 参考：
>
> 1. [三小时学会【fastapi框架教程】从入门到精通 ↪](https://www.bilibili.com/video/BV1cedVYWEE7?spm_id_from=333.788.videopod.episodes&vd_source=b539518f043998f08c722489225f1c3c&p=13)
> 2. [官方指南 ↪](https://fastapi.tiangolo.com/zh/)

# 预备知识

## HTTP 协议

HTTP 协议是 Hyper Text Transfer Protocol（超文本传输协议）的缩写，属于应用层协议，采用客户端—服务端的请求—响应模式。浏览器等客户端通过 URL 向 Web 服务器发送请求，服务器处理请求后返回响应。

### HTTP 协议特性

1. **属于应用层协议**

   HTTP 通常运行在 TCP 之上，也可以运行在其他可靠的传输协议之上。

2. **基于请求 — 响应模式**

   客户端先发送请求，服务器再返回响应。

3. **无状态**

   HTTP 是一种无状态（stateless）协议。协议本身不会保存不同请求之间的业务状态；如果需要保存状态，通常由 Cookie、Session 或令牌等机制完成。

   每个请求都需要对应的响应，服务器不会仅依靠 HTTP 协议记住上一次请求的内容。

4. **支持连接复用**

   HTTP/1.0 通常使用短连接，HTTP/1.1 默认支持持久连接。连接复用可以减少重复建立和关闭 TCP 连接的开销。

### HTTP 请求协议与响应协议

![HTTP 请求与响应](../imgs/soket.jpg)

HTTP 交互包含请求报文和响应报文。报文由起始行、请求头或响应头、空行以及可选的消息体组成。

**使用 socket 简单观察 HTTP 报文格式**

```python
import socket
import json

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("127.0.0.1", 5173))
server_socket.listen(5)
print("服务器已启动，监听端口 5173...")

try:
    while True:
        conn, _ = server_socket.accept()
        with conn:
            data = conn.recv(4096)
            print(f"客户端发送的请求信息：\n{data.decode('utf-8', errors='replace')}")

            body = json.dumps({"user_id": 1001}).encode("utf-8")
            response = (
                b"HTTP/1.1 200 OK\r\n"
                b"Content-Type: application/json; charset=utf-8\r\n"
                + f"Content-Length: {len(body)}\r\n\r\n".encode()
                + body
            )
            conn.sendall(response)
except Exception as e:
    print(e)
finally:
    server_socket.close()

```

## API

在开发 Web 应用时，常见有两种模式：

1. 前后端不分离 — 页面内容和界面效果主要由服务端生成
2. 前后端分离 — 前端（HTML、CSS、JavaScript）独立开发，Python 服务端主要返回数据

应用程序编程接口（**A**pplication **P**rogramming **I**nterface，API）是应用程序对外提供的操作入口，可以是函数、类方法或 URL。当客户端调用 API 时，应用程序会执行对应逻辑并返回结果。

在实际开发中，我们既会调用别人提供的 API，也会为别人提供 API。统一的路径、参数和响应规范，可以降低客户端与服务端之间的沟通成本。

为了形成团队共识，需要选择一种清晰、易维护的接口设计规范。

常见的接口风格主要有 RESTful API 和 RPC。

REST 全称是 Representational State Transfer，通常译为“表征性状态转移”。它首次出现在 Roy Fielding 于 2000 年发表的博士论文中。

RESTful 是一种面向资源的 Web API 设计风格，尤其适用于前后端分离的应用。

关键：面向资源开发

这种风格强调面向资源设计接口：客户端访问的 URL 路径表示要操作的数据资源。

对于数据资源，通常使用 POST、GET、PUT/PATCH、DELETE 等请求方法表达增、查、改、删操作。

| 请求方法 | 请求地址     | 后端操作        |
| :------- | :----------- | :-------------- |
| POST     | `/student/`  | 增加学生        |
| GET      | `/student/`  | 获取所有学生    |
| GET      | `/student/1` | 获取ID为1的学生 |
| PUT      | `/student/1` | 修改ID为1的学生 |
| DELETE   | `/student/1` | 删除ID为1的学生 |

RESTful 是一种通用的设计风格，不限制语言和开发框架。任何语言和框架都可以实现符合 RESTful 风格的 API。

# 快速体验

> `uv` 的安装、项目初始化和依赖管理详见[第01章：Python 项目与依赖管理（Poetry 与 uv）](<第01章 Python 项目与依赖管理.md>)。

## 安装 uv（macOS）

macOS 推荐使用 Homebrew 安装 `uv`：

```shell
$ brew install uv
$ uv --version
```

如果尚未安装 Homebrew，可参考 [Homebrew 官方文档](https://brew.sh/zh-cn/)。也可以使用 `uv` 官方安装脚本：

```shell
$ curl -LsSf https://astral.sh/uv/install.sh | sh
```

> 通过 Homebrew 安装后，使用 `brew upgrade uv` 升级；通过官方安装脚本安装后，可以使用 `uv self update` 升级。更多安装方式参考 [`uv` 官方文档](https://docs.astral.sh/uv/getting-started/installation/)。

## 创建项目

创建并进入工程目录：

```shell
$ mkdir fastapi_tutorial && cd fastapi_tutorial
$ uv init --bare
```

指定项目使用的 Python 版本：

```shell
$ uv python install 3.14.7
$ uv python pin 3.14.7
```

> **提示**：
>
> `uv python install` 会安装指定版本的 Python。
>
> `uv python pin` 会在当前项目记录版本。
>
> 若系统中已经有可用的 Python 3.14.7，也可以跳过第一条命令。

安装依赖：

```shell
$ uv add "fastapi[standard]"
```

`uv add` 会更新 `pyproject.toml`，并生成或更新 `uv.lock`；项目虚拟环境默认位于 `.venv`。后续使用 `uv run` 执行命令，不需要手动激活虚拟环境。

检查项目使用的 Python 版本：

```shell
$ uv run python --version
Python 3.14.7
```

`fastapi[standard]` 会安装运行开发服务器所需的常用依赖，其中包含 [FastAPI CLI ↪](https://fastapi.tiangolo.com/fastapi-cli/) 和 Uvicorn。生产环境也可以使用 [Uvicorn ↪](https://www.uvicorn.org/) 或 [Hypercorn ↪](https://github.com/pgjones/hypercorn)。

代码示例：

> `main.py`

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def home():
    return {"message": "Hello, World!"}

```

通过以下命令运行服务器：

```shell
$ uv run fastapi dev
INFO:     Will watch for changes in these directories: ...
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [35811] using WatchFiles
```

> 注意：`fastapi dev` 默认查找 `main.py`。如果文件名是 `index.py`，可以执行：`uv run fastapi dev index.py`。需要显式指定模块时，也可以使用 `uv run uvicorn index:app --reload`。

也可以直接运行：

```python
import uvicorn
if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
```

流程：

1. 导入 FastAPI
2. 创建一个 app 实例
3. 编写一个路径操作装饰器，如：`@app.get("/")`
4. 编写一个路径操作函数
5. 定义返回值
6. 运行开发服务器，如：`uv run fastapi dev`

此外，FastAPI 会自动生成交互式 API 文档。打开 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) 即可查看。关于文档配置，可以参考 [元数据和文档配置 ↪](https://fastapi.tiangolo.com/zh/tutorial/metadata/)。

# 路径操作

## 路径操作装饰器

FastAPI 支持各种请求方式：

- `@app.get()`

- `@app.post()`
- `@app.put()`
- `@app.delete()`

- `@app.options()`
- `@app.head()`
- `@app.patch()`
- `@app.trace()`

代码示例：

```python
from fastapi import FastAPI
import uvicorn


app = FastAPI()


@app.get("/get")
async def get_test():
    return {"method": "GET"}


@app.post("/post")
async def post_test():
    return {"method": "POST"}


@app.put("/put")
async def put_test():
    return {"method": "PUT"}


@app.delete("/delete")
async def delete_test():
    return {"method": "DELETE"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)
```

[http://127.0.0.1:8080/docs ↪ ](http://127.0.0.1:8080/docs)

![路由请求方法](../imgs/router_methods.jpg)

路径操作装饰器参数：

```python
@app.post(
    "/items/{item_id}",
    response_model=Item,
    status_code=status.HTTP_200_OK,
    tags=["AAA"],
    summary="this is summary",
    description="this is description",
    response_description="this is response_description",
    deprecated=False,
)
async def create_item(item_id: int, item: Item):
    ...
```

> 上例主要展示装饰器参数，函数体使用 `...` 表示省略实现；`Item` 和 `status` 需要在完整项目中自行导入或定义。

## include_router

新建目录结构如下：

```
.
├── app
│   ├── __init__.py
│   ├── api
│   │   ├── __init__.py
│   │   └── v1
│   │       ├── __init__.py
│   │       ├── users.py
│   │       └── works.py
│   └── main.py
└── README.md

4 directories, 7 files
```

```shell
$ mkdir -p app/api/v1 && touch  README.md app/{__init__,main}.py app/api/__init__.py app/api/v1/{__init__,users,works}.py
```

文件内容：

> **`app/api/v1/users.py`**

```python
from fastapi import APIRouter


router = APIRouter()


@router.post("/register", summary="用户注册")
async def register():
    return {"code": 200, "data": None, "msg": "注册成功"}


@router.post("/login", summary="用户登录")
async def login():
    return {"code": 200, "data": None, "msg": "登录成功"}
```

> **`app/api/v1/works.py`**

```python
from fastapi import APIRouter


router = APIRouter()


@router.get("/", summary="作品列表")
async def list_works():
    return {"code": 200, "data": [1, 2, 3], "msg": "success"}


@router.get("/{id}", summary="作品详情")
async def details(id: int):
    return {"code": 200, "data": {"id": id}, "msg": "success"}
```

> **`app/api/v1/__init__.py`**

```python
from fastapi import APIRouter
from app.api.v1.users import router as users_router
from app.api.v1.works import router as works_router

router = APIRouter()

router.include_router(users_router, prefix="/users", tags=["用户相关"])
router.include_router(works_router, prefix="/works", tags=["作品管理"])
```

> **`app/main.py`**

```python
from app.api.v1 import router as api_router
from fastapi import FastAPI
import uvicorn

app = FastAPI()

app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run("app.main:app", port=8080, reload=True)
```

> 在项目根目录执行 `uv run uvicorn app.main:app --reload`，即可启动这个多文件应用。

[http://127.0.0.1:8080/docs ↪ ](http://127.0.0.1:8080/docs)

![路由拆分与聚合](../imgs/include_router.jpg)

# 请求与响应

## 路径参数

**（1）基本用法**

FastAPI 支持使用路径模板声明**路径参数**（**变量**）。建议同时使用类型注解，让 FastAPI 自动完成转换和校验。

```python
import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
```

这段代码把路径参数 `item_id` 的值传递给路径函数的参数 `item_id`。

**（2）有类型的路径参数**

使用 Python 标准类型注解，声明路径操作函数中路径参数的类型。

```python
import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    print(item_id, type(item_id))
    return {"item_id": item_id}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
```

本例把 `item_id` 的类型声明为 `int`。FastAPI 会在请求进入路径函数前，将字符串形式的路径参数转换为整数并完成校验。

> 类型声明还可以为函数提供错误检查、代码补全等编辑器支持。

**（3）注意顺序**

在创建 **路径操作** 时，你会发现有些情况下路径是固定的。

比如 `/users/me`，我们假设它用来获取关于当前用户的数据。

然后，你还可以使用路径 `/users/{username}` 来通过用户名获取关于特定用户的数据。

由于路径操作是 **按顺序依次匹配** 的，你需要确保路径 `/users/me` 声明在路径 `/users/{username}` 之前。

## 查询参数

声明的参数不是路径参数时，路径操作函数会把该参数自动解释为**查询**参数。

查询参数就是 URL 中 `?` 之后用 `&` 分割的 `key-value` 键值对。

```python
import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/jobs/{keyword}")
async def get_jobs(keyword: str, education: str | None = None, location: str | None = None):
    # 基于 keyword、education、location 查询岗位信息
    return {
        "keyword": keyword,
        "education": education,
        "location": location,
    }


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
```

在这个例子中，函数参数 `education` 和 `location` 是可选的，并且默认值为 `None`。

PEP 484 自 Python 3.5 起引入了类型注解（type hints），它们的主要作用有：

> 1. 作为开发文档附加说明，方便使用者了解参数和返回值类型。
> 2. 为编辑器、静态检查工具提供类型检查和代码补全支持。
> 3. 类型注解本身不会执行运行时校验；在 FastAPI 中，运行时校验由 FastAPI 和 Pydantic 完成。

类型注解用于说明函数输入和输出的数据类型，常见类型包括 `str`、`list` 和 `dict`。

在 Python 3.14 中，多个类型可以使用 `str | list` 表示，可能为空可以使用 `str | None` 表示。`Optional[str]` 仍然可用，它等价于 `str | None`。

**📖 查询参数校验**

```python
import uvicorn
from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/items/")
async def read_items(
    # 查询参数 q 的默认值为 None，最小长度为 3，最大长度为 50
    q: str | None = Query(default=None, min_length=3, max_length=50),
):
    return {"q": q}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)
```

**📖 查询参数模型**

> 查询参数模型需要 FastAPI 0.115.0 或更高版本。

```python
import uvicorn
from typing import Annotated
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()


class FilterParams(BaseModel):
    page: int = Field(1, gt=0)
    size: int = Field(10, gt=0, le=100)
    keywords: str | None = None


@app.get("/items/")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query


if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)
```



## 请求体

FastAPI 使用**请求体**从客户端（例如浏览器）向 API 发送数据。

**请求体**是客户端发送给 API 的数据。**响应体**是 API 发送给客户端的数据。

API 基本上肯定要发送**响应体**，但是客户端不一定发送**请求体**。

FastAPI 基于 `Pydantic` 模型声明**请求体**。

Pydantic 主要用来做类型校验和数据转换，不符合模型要求的数据会触发校验错误。

对于 API 服务，使用模型校验可以让服务更加健壮，也能减少重复的手动校验代码。

安装依赖：

```shell
$ uv add "pydantic>=2"
```

> FastAPI 本身已经依赖 Pydantic；这里单独列出安装命令，是为了明确本节使用 Pydantic 2 的写法。

代码示例：

```python
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator
from datetime import date

app = FastAPI()


class Addr(BaseModel):
    province: str
    city: str


# 把数据模型声明为继承 BaseModel 的类
class User(BaseModel):
    # 姓名
    name: str
    # 年龄，默认为 0，范围为 0-100
    age: int = Field(default=0, ge=0, le=100)
    # 出生日期，可为空
    birth: date | None = None
    # 描述信息
    description: str | None = None
    # 兴趣爱好
    interest: list[str] = Field(default_factory=list)
    # 手机号
    phone: str = Field(pattern=r"^1[3-9]\d{9}$", min_length=11, max_length=11)
    # 地址
    addr: Addr  # 类型嵌套

    # 也可以使用校验函数
    @field_validator("name")
    @classmethod
    def check_name(cls, name: str):
        if name.isalpha():
            return name
        raise ValueError("name must be alpha.")


@app.post("/user/register")
async def create_user(user: User):
    print(user, type(user))
    print(f"user.name >>> {user.name}")
    print(user.model_dump())
    return user


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

```

## Form 表单数据

在 OAuth2 规范的一种使用方式（密码流）中，需要将用户名、密码作为表单字段发送，而不是 JSON。

FastAPI 可以使用 `Form` 组件接收表单数据，需安装依赖 `python-multipart`：

```shell
$ uv add python-multipart
```

```python
import uvicorn
from fastapi import FastAPI, Form

app = FastAPI()


@app.post("/register")
async def register(
    username: str = Form(..., pattern=r"^[a-zA-Z]{8}$"),
    password: str = Form(..., pattern=r"^[0-9]{8}$"),
):
    print(f"username = {username}")
    # 注册，实现数据库添加操作...
    return {"username": username}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
```

## 文件上传

```python
from pathlib import Path
from uuid import uuid4
import uvicorn
from fastapi import FastAPI, File, UploadFile

app = FastAPI()
upload_dir = Path("images")
upload_dir.mkdir(exist_ok=True)


# file: bytes = File()：适合小文件上传
@app.post("/file", summary="文件上传")
async def file(file: bytes = File()):
    return {"file_size": len(file)}


@app.post("/multiFiles", summary="多文件上传")
async def multi_files(files: list[bytes] = File()):
    return {"file_sizes": [len(file) for file in files]}


# file: UploadFile：适合大文件上传
@app.post("/uploadFile", summary="文件上传")
async def upload_file(file: UploadFile):
    # 不直接使用客户端文件名，避免路径穿越和文件名冲突
    original_name = Path(file.filename or "upload.bin").name
    path = upload_dir / f"{uuid4().hex}{Path(original_name).suffix.lower()}"
    with path.open("wb") as f:
        # 使用chunk方式写入（适合大文件）
        while content := await file.read(1024 * 1024):  # 每次读取1MB
            f.write(content)
    await file.close()
    return {"file": path.name, "original_filename": original_name}


@app.post("/uploadFiles", summary="多文件上传")
async def upload_files(files: list[UploadFile]):
    # ...
    return {"names": [file.filename for file in files]}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
```

> 实际项目还应校验文件大小、MIME 类型和扩展名，并根据业务限制允许上传的文件类型。

## Request 对象

有些情况下我们希望直接访问 Request 对象。例如获取客户端 IP 地址时，可以在路径操作函数中声明 **Request** 类型的参数。FastAPI 会自动传递 Request 对象，我们可以读取 `headers`、`url` 和 `cookies` 等信息。`session` 需要额外配置 SessionMiddleware。

```python
from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/items")
async def items(request: Request):
    return {
        "请求URL": request.url,
        "请求IP": request.client.host if request.client else None,
        "请求宿主": request.headers.get("user-agent"),
        "cookies": request.cookies,
    }
```

## 响应模型

你可以在任意的路径操作中使用 `response_model` 参数来声明用于响应的模型：

```python
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Generic, TypeVar

app = FastAPI()

"""
定义全局响应模型
"""

T = TypeVar("T")


class BaseResponse(BaseModel, Generic[T]):
    code: int = 200
    message: str = "success"
    data: T | None = None


"""
定义业务接口
"""


@app.get("/", response_model=BaseResponse[str])
async def root() -> BaseResponse[str]:
    return BaseResponse(data="Hello World")


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)

```

## 静态文件

在 Web 开发中，有时需要向客户端提供服务器上的静态资源，如 CSS 或图片。将 `logo.jpg` 放在 `static` 目录中后，可以使用 `StaticFiles` 挂载该目录。

```python
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()

Path("static").mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")
if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
```

此时，前端可以通过链接 [http://127.0.0.1:8000/static/logo.jpg](http://127.0.0.1:8000/static/logo.jpg) 访问图片资源。

# 元数据和文档配置

FastAPI 会根据类型注解、路径操作参数和 Pydantic 模型自动生成 OpenAPI 文档。也可以在创建应用时配置标题、描述和版本：

```python
from fastapi import FastAPI

app = FastAPI(
    title="示例 API",
    description="用于学习 FastAPI 的接口示例",
    version="1.0.0",
)
```

> 参考：[元数据和文档配置 ↪](https://fastapi.tiangolo.com/zh/tutorial/metadata/)

# Jinja2 模板

要了解 Jinja2，首先需要理解模板的概念。模板在 Python 的 Web 开发中广泛使用，可以将业务逻辑和页面逻辑分开，使代码更容易维护。

模板简单来说就是一个包含占位变量的文件，模板经过动态赋值后生成页面并返回给用户。

Jinja2 是一个常用的 Python 模板引擎，具有变量插值、过滤器和控制结构等功能。

在 Jinja2 中，存在两种常用语法：

- 变量插值：`{{  }}`
- 控制结构：`{% %}`

使用前，先安装 Jinja2：

```shell
$ uv add jinja2
```

## 模板语法 — 变量渲染

> **`main.py`**

```python
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn


# 实例化 FastAPI 对象
app = FastAPI()
# 实例化 Jinja2 对象，并将模板目录设置为 templates
templates = Jinja2Templates(directory="templates")


@app.get("/index", response_class=HTMLResponse)
async def index(request: Request):
    name = "root"
    age = 32
    books = ["西游记", "红楼梦", "三国演义", "聊斋志异"]
    info = {"name": "张三", "age": 32, "gender": "男"}

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "username": name,
            "age": age,
            "books": books,
            "info": info,
        },
    )


if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)

```

> **`templates/index.html`**

```html
<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Jinja2Templates</title>
  </head>
  <body>
    <p>用户名：{{ username }}</p>
    <p>年龄：{{ age }}</p>
    <p>四大名著：{{ books }}</p>
    <div>
      <p>四大名著：</p>
      <ol>
        <li>{{ books[0] }}</li>
        <li>{{ books[1] }}</li>
        <li>{{ books[2] }}</li>
        <li>{{ books[3] }}</li>
      </ol>
    </div>
    <p>用户信息：{{ info.name }} - {{ info.age }} - {{ info.gender }}</p>
  </body>
</html>
```

## 模板语法 — 过滤器

变量可以通过“过滤器”进行修改。过滤器可以理解为 Jinja2 提供的内置转换函数。常用的过滤器有：

| 过滤器名称 | 说明                                         |
| ---------- | -------------------------------------------- |
| capitalize | 把值的首字母转换成大写，其他字母转换为小写   |
| lower      | 把值转换成小写形式                           |
| title      | 把值中每个单词的首字母都转换成大写           |
| trim       | 把值的首尾空格去掉                           |
| striptags  | 渲染之前把值中所有的HTML标签都删掉           |
| join       | 拼接多个值为字符串                           |
| round      | 对数字进行舍入，也可以用参数进行控制         |
| safe       | 渲染时不转义（只对可信内容使用）             |

> `safe` 会关闭 HTML 自动转义，只能用于明确可信的内容；不要直接用于用户输入。

那么如何使用这些过滤器呢?只需要在变量后面使用管道（`|`）分割，多个过滤器可以链式调用，前一个过滤器的输出会作为后一个过
滤器的输入。

```jinja2
{{ 'abc'|capitalize }}      {# 输出: Abc #}
{{ 'abc'|upper }}           {# 输出: ABC #}
{{ 'hello world'|title }}   {# 输出: Hello World #}
{{ 'hello world'|replace('world', 'yuan')|upper }}  {# 输出: HELLO YUAN #}
{{ 18.18|round|int }}       {# 输出: 18 #}
```

## 模板语法 — 控制结构

### 分支控制

Jinja2 中的 `if` 语句类似 Python 的 `if` 语句，支持单分支、多分支结构。不同的是，条件语句 **不需要冒号** 结尾，而结束
控制语句，必须显式使用 `{% endif %}` 结束。

代码示例：

```jinja2
{% if user.is_admin %}
  <p>管理员用户</p>
{% elif user.is_member %}
  <p>会员用户</p>
{% else %}
  <p>普通用户</p>
{% endif %}
```

### 循环语句

Jinja2 中的 `for` 循环用于迭代 Python 数据类型：**列表、元组、字典**，**不支持** `while` 循环。

语法结构：

```jinja2
{% for item in iterable %}
  <p>{{ item }}</p>  {# 循环体 #}
{% endfor %}         {# 必须显式结束 #}
```

代码示例：

```jinja2
{% for book in books %}
  <p>{{ book }}</p>
{% endfor %}
```

### 注意事项

1. **标签格式**：

   - 控制语句必须包裹在 `{% %}` 中
   - 错误示例：`{ % for % }`（多余空格会导致解析失败）

2. **循环变量**：

   - 支持访问迭代对象的属性（如 `book.title`）

   - 字典迭代示例：

     ```jinja2
     {% for key, value in user.items() %}
       <p>{{ key }}: {{ value }}</p>
     {% endfor %}
     ```

3. **空白控制**：

   - 使用 `-` 去除空白（如 `{% for -%}` 删除换行符）

### 总结对比表

| 控制结构 | Jinja2 语法特点              | 与 Python 的区别       |
| -------- | ---------------------------- | ---------------------- |
| if       | 无冒号，需 `endif` 结尾      | Python 用 `:` 和缩进   |
| for      | 仅支持迭代，需 `endfor` 结尾 | 无 `while`，语法更严格 |

# 安全

参考：[安全 ↪](https://fastapi.tiangolo.com/zh/tutorial/security/)

OAuth2 密码模式的基本流程：

- 用户通过令牌端点提交用户名和密码，获取 Token
- 前端在请求头中添加 `Authorization: Bearer <token>`
- 后端通过 `get_current_user` 依赖项验证 Token

创建用于 JWT 令牌签名的随机密钥：

```shell
$ openssl rand -hex 32
```

## 安装依赖

安装依赖：`PyJWT`，用于生成和校验 JWT。

```shell
$ uv add PyJWT
```

> 本节只演示令牌的签发和校验，不包含完整的用户数据库和密码校验流程。生产环境应使用环境变量保存密钥。

## 核心代码

> **`app/core/security.py`**

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from pydantic import BaseModel
from datetime import datetime, timezone
from typing import Annotated
import os


# 安全配置常量
# 使用 openssl rand -hex 32 生成密钥，并通过环境变量注入
SECRET_KEY = os.getenv("SECRET_KEY", "development-only-change-me")
ALGORITHM = "HS256"  # HMAC + SHA256 签名算法
ACCESS_TOKEN_EXPIRE_MINUTES = 15  # 访问令牌有效期


class TokenPayload(BaseModel):
    """JWT令牌负载数据结构
    Attributes:
        sub (str): 用户唯一标识(Subject)
        exp (int): 过期时间(Unix时间戳)
        iat (int): 签发时间(Unix时间戳)
    """

    sub: str
    exp: int
    iat: int


def create_access_token(user_id: int) -> str:
    """生成JWT访问令牌
    Args:
        user_id: 用户数据库ID
    Returns:
        str: Base64URL 编码并带有签名的 JWT 字符串
    Note:
        使用UTC时间戳确保跨时区一致性
    """
    timestamp = int(datetime.now(timezone.utc).timestamp())
    payload = TokenPayload(
        sub=str(user_id),
        exp=timestamp + ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        iat=timestamp,
    ).model_dump()
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> TokenPayload:
    """验证并解码JWT令牌
    Args:
        token: JWT令牌字符串
    Returns:
        TokenPayload: 解码后的令牌数据
    Raises:
        HTTPException 401: 令牌过期(ExpiredSignatureError)
        HTTPException 401: 令牌无效(InvalidTokenError)
    Important:
        遵循RFC 7519规范返回WWW-Authenticate头
    """
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        return TokenPayload(**payload)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token 已过期",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except (InvalidTokenError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token 无效",
            headers={"WWW-Authenticate": "Bearer"},
        )


#  OAuth2密码模式Bearer令牌方案
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login",  # 令牌获取端点
    auto_error=False,  # 允许公共接口不传token
)


async def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenPayload:
    """FastAPI依赖项：获取当前认证用户
    Args:
        token: 从Authorization头提取的Bearer令牌
    Returns:
        TokenPayload: 解码后的令牌数据
    Throws:
        HTTPException 401: 缺少令牌或验证失败
    Security:
        必须配合HTTPS使用，防止令牌泄露
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="需要认证Token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return verify_token(token)


# 类型注解快捷方式
# 用户依赖注入
CurrentUser = Annotated[TokenPayload, Depends(get_current_user)]  # 需使用用户数据的场景
DependsJwtUser = Depends(get_current_user)  # 仅需验证的场景
```

## 定义路由，按需注入依赖

```python
import uvicorn
from fastapi import FastAPI
from app.core.security import create_access_token, CurrentUser, DependsJwtUser

# ------------------------------
# FastAPI应用初始化
# ------------------------------
app = FastAPI()


# ------------------------------
# 公共接口（无需认证）
# ------------------------------
@app.post("/login")
async def login():
    # 这里只演示签发令牌；实际项目应接收表单并验证用户密码
    user_id = 1
    return {"access_token": create_access_token(user_id), "token_type": "bearer"}


@app.get("/public")
async def public_api():
    return {"message": "公开接口"}


# ------------------------------
# 需认证接口
# ------------------------------
@app.get("/profile1")
async def profile1(user: CurrentUser):
    """需使用用户数据的场景"""
    return {"user_id": user.sub}


@app.get("/profile2", dependencies=[DependsJwtUser])
async def profile2():
    """仅需验证的场景"""
    return {"user_id": "xxx"}


"""
开发服务器启动​
"""
if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)
```

> 令牌端点必须与 `OAuth2PasswordBearer(tokenUrl=...)` 保持一致。

# 异常处理

```mermaid
sequenceDiagram
    participant Client
    participant Route
    participant Exception
    participant Handler
    Client->>Route: 发起请求
    Route->>Exception: 抛出业务异常
    Exception->>Handler: 捕获异常
    Handler->>Client: 返回结构化错误
```

- 预期的业务错误 → 自定义业务异常
- HTTP 协议相关错误 → `HTTPException`
- 未预期的程序错误 → 保留为服务器错误并记录日志

## 创建自定义异常类

> **`app/core/exceptions/errors.py`**

```python
from app.core.exceptions.codes import E
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from fastapi import HTTPException, status
from typing import Any


class ErrorModel(BaseModel):
    code: int
    msg: str
    data: dict[str, Any] | None = None


class BizException(HTTPException):
    """业务异常基类"""

    def __init__(
        self,
        error_code: E,
        *,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        data: dict | None = None
    ):
        super().__init__(
            status_code=status_code,
            detail=ErrorModel(
                code=error_code.code,
                msg=error_code.msg,
                data=data,
            ).model_dump(),
        )


class ValidationException(BizException):
    """参数校验异常"""

    @classmethod
    def from_pydantic_error(cls, exc: RequestValidationError):
        return cls(
            E.VALIDATION_ERROR,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            data={
                "errors": [
                    {
                        "field": "->".join(map(str, err["loc"])),
                        "message": err["msg"],
                        "type": err["type"],
                    }
                    for err in exc.errors()
                ]
            },
        )

```

## 创建自定义异常处理器

> **`app/core/exceptions/handlers.py`**

```python
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.core.exceptions.errors import BizException, ValidationException


logger = logging.getLogger("api.errors")


def register_exception_handlers(app: FastAPI):
    logger.info("注册异常处理器")

    @app.exception_handler(BizException)
    async def handle_biz_exception(request: Request, exc: BizException):
        return JSONResponse(
            status_code=exc.status_code, content=exc.detail  # 动态获取状态码
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(request: Request, exc):
        return await handle_biz_exception(
            request, ValidationException.from_pydantic_error(exc)
        )

```

## 创建自定义异常码

> **`app/core/exceptions/codes.py`**

```python
from enum import Enum


class E(Enum):
    """
    自定义错误码
    格式: <业务>_<错误类型> = (code, msg)
    """

    # ～～～～～～～～～～～～～～～～～～～～～～～
    # 公共模块
    # ～～～～～～～～～～～～～～～～～～～～～～～
    VALIDATION_ERROR = (10400, "参数验证失败")
    NOT_FOUND = (10404, "资源不存在")

    # ～～～～～～～～～～～～～～～～～～～～～～～
    # 用户模块
    # ～～～～～～～～～～～～～～～～～～～～～～～
    USER_NOT_FOUND = (20000, "用户不存在")
    USER_ALREADY_EXISTS = (20001, "用户已存在")
    USER_PASSWORD_ERROR = (20002, "密码错误")
    USER_REGISTER_FAILED = (20100, "用户注册失败")

    # ～～～～～～～～～～～～～～～～～～～～～～～
    # 支付模块
    # ～～～～～～～～～～～～～～～～～～～～～～～
    PAY_ORDER_NOT_FOUND = (30000, "订单不存在")

    @property
    def code(self):
        """获取错误码"""
        return self.value[0]

    @property
    def msg(self):
        """获取错误码信息"""
        return self.value[1]

```

> **提示**：你可以根据需要自行按业务模块定义错误。

## 挂载注册异常

```python
from fastapi import FastAPI
from app.core.exceptions.handlers import register_exception_handlers

app = FastAPI()
register_exception_handlers(app)

...
```

## 路由中使用

```python
from app.core.exceptions.errors import BizException
from app.core.exceptions.codes import E

@app.post("/user/login")
def login(data: dict):
    raise BizException(E.USER_NOT_FOUND)
```

# 中间件

你可以向 **FastAPI** 应用添加中间件。

**中间件** 是一个函数，它在每个**请求**被特定的路径操作处理之前，以及在每个**响应**返回之前工作。

![中间件执行流程](../imgs/middleware_model.jpg)

> 如果你使用了 `yield` 关键字依赖，依赖中的退出代码会在请求处理流程的后续阶段执行。
>
> 如果有后台任务（后文会介绍），它们将在中间件执行完成后运行。

要创建中间件你可以在函数的顶部使用装饰器 `@app.middleware("http")`

中间件函数接收如下参数：

- `request`
- 一个函数 `call_next`，它接收 `request` 作为参数，并返回路径操作生成的 `response`
- 在返回 `response` 前，可以进一步修改响应



代码示例：

```python
from fastapi import FastAPI, Request, Response
import uvicorn
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


if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)

```

> 多个中间件会形成调用栈：最后添加的中间件在请求时最先执行，在响应时最后执行。本例的请求顺序为 `m1 -> m2 -> 路径操作`。

> **提示**：
>
> 1. 可以 [用 `X-` 前缀 ↪](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers) 添加专有自定义请求头。
> 2. 你也可以使用 `from starlette.requests import Request`，**FastAPI** 为了开发者方便提供了该对象，但其实它直接来自于 Starlette。

# 日志管理

1）安装依赖

```shell
$ uv add loguru
```

2）配置：`app/core/logger.py`

```python
from loguru import logger
import sys


def setup_logger():
    logger.remove()
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | {level} | {message}",
        level="INFO",
    )
```

3）初始化配置项：`app/main.py`

```python
from app.core.logger import setup_logger
setup_logger()
```

4）调用示例：

```python
from loguru import logger
logger.info("直接使用已配置的logger")
```

# CORS（跨域资源共享）

CORS（Cross-Origin Resource Sharing，跨域资源共享）用于控制浏览器中不同源的前端 JavaScript 是否可以访问后端 API。

你可以在 **FastAPI** 应用中使用 `CORSMiddleware` 来配置它。

- 导入 `CORSMiddleware`。
- 创建一个允许的源列表（由字符串组成）。
- 将其作为「中间件」添加到你的 **FastAPI** 应用中。

你也可以指定后端是否允许：

- 凭证（授权 headers，Cookies 等）。
- 特定的 HTTP 方法（`POST`，`PUT`）或者使用通配符 `"*"` 允许所有方法。
- 特定的 HTTP headers 或者使用通配符 `"*"` 允许所有 headers。

```python
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:8080",
]


app.add_middleware(
    CORSMiddleware,
    # 一个允许跨域请求的源列表
    allow_origins=origins,
    # 允许携带 Cookie 或 Authorization 等凭证；此时不能使用 ['*'] 作为允许源
    allow_credentials=True,
    # 一个允许跨域请求的 HTTP 方法列表
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    # 一个允许跨域请求的 HTTP 请求头列表
    allow_headers=["Authorization", "Content-Type"],
)


@app.get("/")
async def main():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)

```

# 环境变量

## 从 `.env` 读取

目录结构：

```
.
├── main.py
└── .env
```

> **`.env`**

```
DB_USER=root
DB_PASSWORD=change-me
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
```

> **`main.py`**

```python
import os
from dotenv import load_dotenv

load_dotenv()
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
...

print(db_user)
```

> **提示**：需要安装 `python-dotenv` 依赖，执行指令：`uv add python-dotenv`。`.env` 只用于本地配置，不要提交真实密码，也不要把密码打印到日志中。

## 从 Pydantic 的 `Settings` 中读取

[Pydantic: Settings management ↪](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)

```
your_project/
├── .env                # 根目录
└── app/
    ├── main.py         # 服务入口
    └── core/
        └── config.py   # 配置类
```

1）安装

```shell
$ uv add pydantic-settings
```

2）新建 **`app/core/config.py`**，内容如下：

```python
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    应用配置类，继承自Pydantic的BaseSettings
    用于定义和管理应用程序的配置参数

    Attributes:
        database_url (str): 数据库连接URL，默认为空字符串
        debug (bool): 调试模式开关，默认为False
    """

    database_url: str = ""
    debug: bool = False

    # 模型配置字典，指定如何加载配置
    model_config = SettingsConfigDict(
        env_file=".env",  # 从.env文件加载环境变量
        env_file_encoding="utf-8",  # 指定.env文件编码格式
        case_sensitive=False,  # 环境变量名不区分大小写
        extra="ignore",  # 忽略配置中多余的字段
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    获取应用配置单例
    使用LRU缓存装饰器确保只加载一次配置

    Returns:
        Settings: 配置类的实例
    """
    return Settings()

```

> `env_file` 使用相对路径时，默认相对于启动命令所在目录；本例应在项目根目录启动服务。

2）根目录新建 **`.env`** 文件，填写环境变量

```
DATABASE_URL=postgresql+asyncpg://user:password@host:port/db_name
DEBUG=true
```

3）读取配置

```python
import uvicorn
from typing import Annotated
from fastapi import FastAPI, Depends
from app.core.config import Settings, get_settings


"""
FastAPI应用初始化
"""
app = FastAPI(title="ChatAI")


"""
路由配置
使用依赖注入获取配置
"""
@app.get("/settings")
def settings(settings: Annotated[Settings, Depends(get_settings)]):
    return {"settings": settings.model_dump()}


"""
开发服务器启动
"""
if __name__ == "__main__":
    uvicorn.run("app.main:app", port=8080, reload=True)
```

> `get_settings()` 使用 `@lru_cache` 后只会创建一次配置对象，测试时可以调用 `get_settings.cache_clear()` 重新加载配置。接口中不要返回密钥、密码等敏感配置。

# 部署

开发环境可以使用：

```shell
$ uv run uvicorn app.main:app --reload
```

生产环境应关闭 `--reload`，并根据服务器资源配置 worker 数量：

```shell
$ uv run fastapi run app/main.py --workers 2
```

更多内容参考：[FastAPI 部署文档 ↪](https://fastapi.tiangolo.com/zh/deployment/)
