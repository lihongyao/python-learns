# 概述

[HTTP 协议参考 ↪](https://www.cnblogs.com/ltyc/p/18664047)

[FastAPI ↪](https://fastapi.tiangolo.com/zh/) 是一个用于构建 API 的现代、高性能 Web 框架，使用 Python 并基于标准的类型提示。

[FastAPI ↪](https://fastapi.tiangolo.com/zh/) 是建立在 Starlette 和 Pydantic 基础上的。

Pydantic 是一个基于 Python 类型提示来定义数据验证、序列化和文档的库。

Starlette 是一种轻量级的 ASGI 框架/工具包，负责处理 Web 请求和响应。

> - [Starlette ↪](https://starlette.dev/) 负责 Web 部分（asyncio）
> - [Pydantic ↪](https://docs.pydantic.dev/latest/) 负责数据部分（类型提示）

FastAPI 建立在 Starlette 和 Pydantic 之上，适合开发前后端分离的 API、自动化服务和微服务。

> 本章示例基于 [Python 3.15.2 ↪](https://www.python.org/downloads/release/python-3152/)，使用 Python 3.10+ 语法。

> **查阅约定**：本章使用 Pydantic 2；截至 2026-11-23，对照 FastAPI 官方文档核查。涉及版本要求的功能会在示例旁单独标注。除明确给出多文件目录结构的示例外，各代码块按独立示例阅读，不要直接把多个 `app = FastAPI()` 合并到同一文件中。

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

![HTTP 请求与响应](../imgs/socket.png)

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
uv 0.13.9 (Homebrew 2026-11-17 aarch64-apple-darwin)
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
$ uv python install 3.15.2
$ uv python pin 3.15.2
```

> **提示**：
>
> `uv python install` 会安装指定版本的 Python。
>
> `uv python pin` 会在当前项目记录版本。
>
> 若系统中已经有可用的 Python 3.15.2，也可以跳过第一条命令。

安装依赖：

```shell
$ uv add "fastapi[standard]"
```

`uv add` 会更新 `pyproject.toml`，并生成或更新 `uv.lock`；项目虚拟环境默认位于 `.venv`。后续使用 `uv run` 执行命令，不需要手动激活虚拟环境。

检查项目使用的 Python 版本：

```shell
$ uv run python --version
Python 3.15.2
```

`fastapi[standard]` 会安装运行开发服务器所需的常用依赖，其中包含 [FastAPI CLI ↪](https://fastapi.tiangolo.com/fastapi-cli/) 和 Uvicorn。生产环境也可以使用 [Uvicorn ↪](https://www.uvicorn.org/) 或 [Hypercorn ↪](https://github.com/pgjones/hypercorn)。

代码示例：

> `main.py`

```python
from fastapi import FastAPI

app = FastAPI(
    title="示例 API",
    description="用于学习 FastAPI 的接口示例",
    version="1.0.0",
)

@app.get("/")
async def home():
    return {"message": "Hello, World!"}

```

通过以下命令运行服务器：

```shell
$ uv run fastapi dev

 ⚡️ Starting FastAPI in development mode
 
 🐍 Using import string: main:app (auto-discovered, use --verbose to learn more)
 
 💡 You can configure an entrypoint in pyproject.toml for this app with:
 
    [tool.fastapi]
    entrypoint = "main:app"
 
 🌐 Server started at http://127.0.0.1:8000
    Documentation at http://127.0.0.1:8000/docs
```

> 注意：`fastapi dev` 默认查找 `main.py`。如果文件名是 `index.py`，可以执行：`uv run fastapi dev index.py`。需要显式指定模块时，也可以使用 `uv run uvicorn index:app --reload`。

> 提示：如果你从 GitHub 下载了一个使用 uv + FastAPI 的 Python 项目，通常可以按照下面的步骤安装依赖并运行。
>
> 1）进入项目目录
>
> 2）先查看项目根目录是否有以下文件：
>
> - `pyproject.toml`
> - `uv.lock`
>
> 如果有，直接执行：
>
> ```shell
> $ uv sync
> ```
>
> - 创建 `.venv` 虚拟环境（如果不存在）。
> - 根据 `pyproject.toml` 安装项目依赖。
> - 如果有 `uv.lock`，优先按照锁定版本安装。
> - 安装项目本身。

也可以直接运行：

```python
import uvicorn
if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
```

流程：

1. 导入 FastAPI
2. 创建一个 FastAPI（app） 实例
3. 创建一个路径操作
4. 定义路径操作函数
5. 返回内容
6. 运行开发服务器，如：`uv run fastapi dev`
7. 部署

此外，FastAPI 会自动生成交互式 API 文档。打开 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) 即可查看。

**`def` 与 `async def` 怎么选**

| 路径操作或依赖中的主要工作 | 常用写法 | 原因 |
| --- | --- | --- |
| 调用支持 `await` 的 HTTP 客户端、数据库驱动等 | `async def`，并 `await` 对应操作 | 等待 I/O 时允许事件循环处理其他请求 |
| 调用同步数据库驱动、同步 HTTP 客户端或同步文件操作 | 普通 `def` | FastAPI 在线程池中执行普通 `def` 路径操作和依赖 |
| 异步流程中夹有一段同步阻塞调用 | `async def`，将阻塞调用交给线程池 | 避免直接阻塞事件循环 |
| 长时间的 CPU 密集计算 | 按需使用进程池或独立任务服务 | 改成 `async def` 或放入线程池不会自动解决 CPU 瓶颈 |

FastAPI 只会对它负责调用的普通 `def` 路径操作和依赖做线程池调度。你在 `async def` 内直接调用的普通函数，仍在当前执行线程中运行。例如，直接使用 `time.sleep()`、同步 HTTP 请求或同步磁盘写入，都会阻塞事件循环。

需要保留异步路径操作时，可以显式转移同步调用：

```python
from starlette.concurrency import run_in_threadpool


def blocking_operation(item_id: int) -> dict:
    # 代表项目中无法改为异步的同步 I/O 调用
    return {"item_id": item_id}


@app.get("/blocking-demo/{item_id}")
async def blocking_demo(item_id: int):
    return await run_in_threadpool(blocking_operation, item_id)
```

> 上例接在已有的 `app` 定义后使用。普通 `def` 同样适合简单接口，无须为了“异步”而把所有函数都写成 `async def`。
>
> 参考：[并发与 async / await ↪](https://fastapi.tiangolo.com/zh/async/)。

# 路径操作

这里的「操作」指的是一种 HTTP「方法」

下列之一：

- `POST`
- `GET`
- `PUT`
- `DELETE`

...以及更少见的几种：

- `OPTIONS`
- `HEAD`
- `PATCH`
- `TRACE`

## 路径操作装饰器


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
from pathlib import Path
import sys

# 兼容 IDE 或命令行直接执行 app/main.py。
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if __package__ in (None, ""):
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi import FastAPI
from app.api.v1 import router as api_router
import uvicorn

app = FastAPI()

app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run("app.main:app", port=8000, reload=True, reload_dirs=[str(PROJECT_ROOT)])

```

> 在项目根目录执行 `uv run uvicorn app.main:app --reload`，即可启动这个多文件应用。

[http://127.0.0.1:8000/docs ↪ ](http://127.0.0.1:8000/docs)

![路由拆分与聚合](../imgs/include_router.jpg)

# 请求与响应

## 路径参数

**（1）基本用法**

FastAPI 支持使用路径模板声明 **路径参数**（**变量**）。建议同时使用类型注解，让 FastAPI 自动完成转换和校验。

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

使用 Python 标准类型注解，声明路径操作函数中路径参数的类型：

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

> **提示**：类型声明还可以为函数提供错误检查、代码补全等编辑器支持。

**（3）注意顺序**

在创建 **路径操作** 时，你会发现有些情况下路径是固定的。

比如 `/users/me`，我们假设它用来获取关于当前用户的数据。

然后，你还可以使用路径 `/users/{username}` 来通过用户名获取关于特定用户的数据。

由于路径操作是**按顺序依次运行**的，因此，一定要在 `/users/{user_id}` 之前声明 `/users/me` ：

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}
```

## 查询参数

对于未显式声明来源的普通标量参数（如 `str`、`int`、`bool`），如果参数名不在路径模板中，FastAPI 通常将其解释为**查询参数**。Pydantic 模型默认通常被解释为请求体；`Request`、依赖参数等另有专门的处理规则。

查询参数就是 URL 中 `?` 之后用 `&` 分割的 `key-value` 键值对。

**参数来源速查**

| 声明方式 | 参数来源或用途 |
| --- | --- |
| 路径含 `{item_id}`，函数声明 `item_id: int` | 路径参数；可以用 `Path()` 添加约束 |
| 不在路径中的普通标量参数，或显式使用 `Query()` | 查询参数 |
| 直接声明 Pydantic 模型，或使用 `Body()` | 请求体；模型默认按 JSON 解析 |
| `Annotated[FilterParams, Query()]` | 从查询参数构建模型，见下方查询参数模型示例 |
| `Form()` | 表单字段 |
| `File()` / `UploadFile` | 上传文件，使用 `multipart/form-data` |
| `Header()` / `Cookie()` | 请求头 / Cookie |
| `Request` / `Depends(...)` | 原始请求对象 / 依赖注入，不按普通查询参数处理 |

> **是否必填取决于默认值**：`q: str` 必填；`q: str | None` 仍必填，只是类型允许 `None`；`q: str | None = None` 才允许省略。查询串中的文本 `null` 不会自动变成 Python 的 `None`。集合类型的查询参数建议显式声明 `Query()`，避免被解释为请求体。

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

Python 3.10 起，多个类型可以使用 `str | list` 表示，可能为空可以使用 `str | None` 表示。`Optional[str]` 仍然可用，它等价于 `str | None`，不代表参数可以省略。

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

API 通常会发送**响应体**，但 `204 No Content` 等响应不携带响应体；客户端也不一定发送**请求体**。

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

**请求体模型常用操作（Pydantic 2）**

| 操作 | 用途 |
| --- | --- |
| `user.model_dump()` | 转成 Python 字典；`date` 等值可能仍是 Python 对象 |
| `user.model_dump(mode="json")` | 转成由 JSON 可用值组成的字典 |
| `user.model_dump(exclude_unset=True)` | 只保留请求中显式传入的字段，常用于 PATCH 局部更新 |
| `User.model_validate(data)` | 从字典等数据校验并构建模型 |

`exclude_unset=True` 会保留客户端显式传入的 `null`；它与 `exclude_none=True`（排除值为 `None` 的字段）含义不同。局部更新应另定义允许省略待更新字段的模型，然后用 `exclude_unset=True` 提取更新内容。

> 参考：[请求体 ↪](https://fastapi.tiangolo.com/zh/tutorial/body/)、[请求体更新 ↪](https://fastapi.tiangolo.com/zh/tutorial/body-updates/)。

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

`bytes` 会把整个文件内容载入内存；`UploadFile` 使用可转存磁盘的临时文件，便于分块处理。两者接收的都是表单文件。上传文件和其他表单字段可以组合，但不能在同一个请求体中同时按普通 JSON 模型和 `multipart/form-data` 两种编码解析。

```python
from pathlib import Path
from uuid import uuid4
import uvicorn
from fastapi import FastAPI, File, HTTPException, UploadFile, status

app = FastAPI()
upload_dir = Path("images")
upload_dir.mkdir(exist_ok=True)
MAX_FILE_SIZE = 10 * 1024 * 1024  # 单个文件最多 10 MiB


# file: bytes = File()：适合小文件上传
@app.post("/file", summary="文件上传")
async def file(file: bytes = File()):
    return {"file_size": len(file)}


@app.post("/multiFiles", summary="多文件上传")
async def multi_files(files: list[bytes] = File()):
    return {"file_sizes": [len(file) for file in files]}


# file: UploadFile：适合大文件上传
@app.post("/uploadFile", summary="文件上传")
def upload_file(file: UploadFile):
    # 本例使用同步磁盘 I/O，因此采用普通 def，由 FastAPI 在线程池执行。
    # 不直接使用客户端文件名，避免路径穿越和文件名冲突
    original_name = Path(file.filename or "upload.bin").name
    path = upload_dir / f"{uuid4().hex}{Path(original_name).suffix.lower()}"
    size = 0
    try:
        with path.open("wb") as f:
            while content := file.file.read(1024 * 1024):
                size += len(content)
                if size > MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=status.HTTP_413_CONTENT_TOO_LARGE,
                        detail="文件不能超过 10 MiB",
                    )
                f.write(content)
    except Exception:
        path.unlink(missing_ok=True)  # 超限或写入失败时删除未完成文件
        raise
    finally:
        file.file.close()
    return {"file": path.name, "original_filename": original_name}


@app.post("/uploadFiles", summary="多文件上传")
async def upload_files(files: list[UploadFile]):
    # ...
    return {"names": [file.filename for file in files]}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
```

> 实际项目还应校验文件大小、MIME 类型和扩展名，并根据业务限制允许上传的文件类型。

**大小限制要区分两个阶段**

- 上面的累计检查在路径操作执行时限制单个文件大小；到达这里之前，框架已经解析了 multipart 数据并准备了上传临时文件。
- 应用或入口代理的请求体限制，用来限制整个请求，包含文件、其他表单字段和 multipart 编码开销。多文件上传还要考虑文件数量和总大小。

当前官方文档提供 `max_body_size`（以下写法按 **FastAPI 0.165.0** 核对；旧版本应先确认是否支持）。在上例创建应用的位置，可按业务替换为：

```python
app = FastAPI(max_body_size=11 * 1024 * 1024)  # 整个请求最多 11 MiB
```

> 整个请求超限时返回 HTTP 413；11 MiB 只是本例为 10 MiB 文件预留表单开销的配置示意。扩展名与客户端声明的 `content_type` 都不能单独证明文件真实类型。若只需异步读取，可使用 `await file.read(...)`；同步的 `open()`、`write()` 仍需另外处理，不能因分块读取就视为完全非阻塞。
>
> 参考：[请求文件 ↪](https://fastapi.tiangolo.com/zh/tutorial/request-files/)、[请求体大小限制 ↪](https://fastapi.tiangolo.com/advanced/request-body-limits/)。

## Request 对象

有些情况下我们希望直接访问 Request 对象。例如获取客户端 IP 地址时，可以在路径操作函数中声明 **Request** 类型的参数。FastAPI 会自动传递 Request 对象，我们可以读取 `headers`、`url` 和 `cookies` 等信息。`session` 需要额外配置 SessionMiddleware。

```python
from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/items")
async def items(request: Request):
    return {
        "请求URL": str(request.url),
        "请求IP": request.client.host if request.client else None,
        "User-Agent": request.headers.get("user-agent"),
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
    msg: str = "success"
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

**响应模型不只是文档说明**

FastAPI 会依据响应模型校验、序列化并过滤输出字段。输入和输出需求不同时，应分别定义模型：

```python
from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()


class UserCreate(BaseModel):
    username: str
    password: str


class UserPublic(BaseModel):
    username: str


@app.post("/users", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    # 演示输出字段过滤；实际注册还需要密码哈希和数据库写入。
    return user.model_dump()
```

发送 `{"username": "alice", "password": "example-password"}`，响应只有 `{"username": "alice"}`。本章通用响应包装约定使用 `code`、`msg`、`data`；包装结构按项目需要使用，FastAPI 不要求采用固定业务格式。

**状态码与校验错误速查**

| 情况 | 说明 |
| --- | --- |
| `return {"code": 404}` | 只设置 JSON 业务字段；接口默认仍可能是 HTTP 200 |
| `@app.post(..., status_code=201)` | 设置实际 HTTP 状态码，并记录到 OpenAPI 文档 |
| `raise HTTPException(status_code=404, detail="资源不存在")` | 中断正常执行，返回实际 HTTP 404 |
| 请求参数或请求体不符合声明 | 默认返回 HTTP 422；属于客户端输入问题 |
| 返回数据不符合响应模型 | 属于服务端实现错误，通常返回 HTTP 500，应修正返回值或模型 |
| 直接返回 `Response` / `JSONResponse` 对象 | 自行负责响应内容；不会再经过通常的响应模型校验和字段过滤 |

> 同时声明返回类型与 `response_model` 时，FastAPI 的响应处理以 `response_model` 为准。直接构造 `JSONResponse` 时，如内容含 `datetime` 等 Python 对象，可先用 `jsonable_encoder()` 转为 JSON 可用值。
>
> 参考：[响应模型 ↪](https://fastapi.tiangolo.com/zh/tutorial/response-model/)、[响应状态码 ↪](https://fastapi.tiangolo.com/zh/tutorial/response-status-code/)。

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

**先理解依赖注入：`Depends` 与 `Annotated`**

依赖可以是函数等可调用对象。FastAPI 先解析并调用依赖，再把它的返回值传给路径操作；依赖也可以继续依赖其他函数。认证、公共查询条件和配置读取都适合用这种方式复用。

下面是独立的公共分页参数示例：

```python
from typing import Annotated
from fastapi import Depends, FastAPI, Query

app = FastAPI()


def pagination(
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1, le=100)] = 10,
) -> dict[str, int]:
    return {"page": page, "size": size}


Pagination = Annotated[dict[str, int], Depends(pagination)]


@app.get("/items")
def list_items(params: Pagination):
    return params
```

访问 `/items?page=2&size=20` 会得到 `{"page": 2, "size": 20}`；传入 `page=0` 会触发参数校验错误。

| 写法 | 用途 |
| --- | --- |
| `params: Annotated[T, Depends(func)]` | 执行依赖，并使用其返回值；`T` 是返回值类型 |
| `params: T = Depends(func)` | 同样支持依赖注入；`Annotated` 便于复用类型声明 |
| `dependencies=[Depends(func)]` | 执行依赖检查，不把返回值传给路径函数 |
| `APIRouter(dependencies=[...])` / `FastAPI(dependencies=[...])` | 给一组路由 / 整个应用统一添加依赖 |

`Annotated[T, ...]` 中的 `T` 描述类型，后面的 `Depends()`、`Query()` 等提供框架处理所需的信息。传给 `Depends` 的是可调用对象，如 `Depends(pagination)`，不要写成提前调用的 `Depends(pagination())`。

> 同一次请求中，同一个依赖的结果默认会复用；这与配置部分的 `@lru_cache`（跨请求、在当前进程内缓存）不同。带 `yield` 的依赖适合管理每次请求使用的资源，应用共享资源则可由部署部分的 `lifespan` 管理。`yield` 依赖的清理时机与其 `scope` 有关。
>
> 参考：[依赖注入 ↪](https://fastapi.tiangolo.com/zh/tutorial/dependencies/)、[带 yield 的依赖 ↪](https://fastapi.tiangolo.com/zh/tutorial/dependencies/dependencies-with-yield/)。

OAuth2 密码模式的基本流程：

- 用户通过令牌端点提交用户名和密码，获取 Token
- 前端在请求头中添加 `Authorization: Bearer <token>`
- 后端通过 `get_current_user` 依赖项验证 Token

创建用于 JWT 令牌签名的随机密钥：

```shell
$ openssl rand -hex 32
```

本地运行本节示例前，在启动服务的终端注入密钥（macOS / Linux）：

```shell
$ export SECRET_KEY="$(openssl rand -hex 32)"
```

每次重新生成密钥后，之前签发的令牌会失效。也可以先用 `.env` 保存本地密钥，再按环境变量一节加载；`os.getenv()` 本身不会读取 `.env` 文件。

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
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("请先设置 SECRET_KEY 环境变量")
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
        认证失败时返回 WWW-Authenticate: Bearer 响应头
    """
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"require": ["sub", "exp", "iat"]},
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
    tokenUrl="login",  # 相对令牌端点；用于 OpenAPI，不会自动创建登录路由
    auto_error=False,  # 缺少 Bearer 认证信息时返回 None，由下方依赖统一处理
)


async def get_current_user(
    token: Annotated[str | None, Depends(oauth2_scheme)],
) -> TokenPayload:
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

> **`main.py`**（与上面的 `app/core/security.py` 配合使用）

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

> 令牌端点必须与 `OAuth2PasswordBearer(tokenUrl=...)` 保持一致。这里的相对地址 `login` 对应 `/login`；如果项目加入了 `/api/v1` 等前缀，需要同步检查实际路由地址。相对地址便于部署在代理的路径前缀之下。

**认证边界与常见误区**

- 本例 `/login` 不验证用户名密码，只用于演示签发令牌。手动调用后，将返回的令牌填入 `Authorization: Bearer <token>` 即可验证受保护接口；公开接口不挂认证依赖，无须额外设置 `auto_error=False`。
- Swagger UI 的 OAuth2 授权流程会提交表单中的 `username`、`password`。需要完整登录时，应使用 `OAuth2PasswordRequestForm` 接收并验证，验证成功后才签发令牌。本例的简化登录端点不能作为真实账号认证使用。
- JWT 的签名用于校验完整性，不代表内容被加密，不要把密码等秘密放入 payload。解码时固定允许的算法，不使用客户端提供的算法作为验证依据。
- `TokenPayload` 是经过验证的令牌数据，并非数据库中的用户对象。实际业务还需根据 `sub` 查询用户是否存在、是否被禁用，再检查访问权限；通常认证失败用 HTTP 401，已认证但权限不足用 HTTP 403。
- 本例要求 `sub`、`exp`、`iat` 存在，并由 PyJWT 校验时间声明、Pydantic 校验字段类型。令牌有效不等于具有刷新、注销或立即撤销能力，这些需要单独设计。

密码应保存为安全哈希。若要补齐密码处理，可按官方示例安装 `uv add "pwdlib[argon2]"`，使用 `PasswordHash.recommended().hash(...)` 生成哈希、`verify(...)` 校验密码；耗时的同步密码哈希操作也要考虑前文的线程池处理规则。

> 参考：[OAuth2、密码哈希与 JWT ↪](https://fastapi.tiangolo.com/zh/tutorial/security/oauth2-jwt/)、[安全工具参数 ↪](https://fastapi.tiangolo.com/reference/security/)。

# 异常处理

本节采用的约定：**统一错误响应格式，保留真实 HTTP 状态；业务异常表达失败原因，由 API 层决定如何响应；未知故障返回 500 并记录堆栈。**

```mermaid
sequenceDiagram
    participant Client
    participant Route
    participant Service
    participant Handler
    Client->>Route: 发起请求
    Route->>Service: 调用业务逻辑
    Service-->>Handler: 抛出业务异常
    Handler-->>Client: HTTP 状态 + 业务码 + 请求标识
```

**异常分类速查**

| 情况 | 处理方式 | HTTP 状态示例 |
| --- | --- | --- |
| 请求字段缺失、类型错误 | 直接处理 `RequestValidationError` | 422 |
| 资源不存在、状态冲突等预期业务失败 | 抛出 `BizException`，集中映射状态 | 404、409 |
| 未认证、无权限、路由不存在 | 处理 Starlette `HTTPException`，保留协议响应头 | 401、403、404 |
| 程序缺陷、响应模型校验失败、未处理的数据库或外部服务故障 | 返回安全的通用错误，记录堆栈并告警 | 500；明确识别后可按语义使用 502、503、504 |

- HTTP 状态用于描述请求结果，业务码用于描述具体原因，`msg` 用于展示。客户端按状态和业务码处理逻辑，不要匹配提示文案。
- “查询是否有资格”正常返回“没有资格”，可以是 HTTP 200；“执行购买”因资格不足被拒绝，应按接口语义返回相应 4xx。预期内的失败并不自动等于请求成功。
- 不在每个路由里重复 `try/except`。业务层抛出异常，API 边界统一生成响应；只有需要恢复、清理资源或转换已知异常时，才在局部捕获。

## 创建自定义异常类

> **`app/core/exceptions/errors.py`**

```python
from typing import Any

from pydantic import BaseModel

from app.core.exceptions.codes import E


class ErrorModel(BaseModel):
    code: int
    msg: str
    data: dict[str, Any] | None = None
    request_id: str


class BizException(Exception):
    """预期业务失败；不负责选择 HTTP 状态或构造响应。"""

    def __init__(self, error_code: E, *, data: dict[str, Any] | None = None):
        self.error_code = error_code
        self.data = data
        super().__init__(error_code.msg)
```

`BizException` 继承普通 `Exception`，不继承 `HTTPException`；调用处只传入业务码和允许公开的数据。同一套业务逻辑用于 HTTP 接口、任务或命令行时，可以由不同入口决定处理方式。

请求参数校验失败直接由 `RequestValidationError` 处理，不再包装成业务异常。输出模型校验失败、业务内部的 Pydantic 校验错误不能一律当作客户端参数错误。

> `msg` 和 `data` 都属于对外契约，不要放入 SQL、连接串、密码、令牌或第三方服务的原始报错。

## 创建自定义异常处理器

> **`app/core/exceptions/handlers.py`**

```python
import logging
from uuid import uuid4

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.exceptions.codes import E
from app.core.exceptions.errors import BizException, ErrorModel


logger = logging.getLogger("api.errors")

# HTTP 映射放在 API 层；新增业务异常时一并补齐，不在调用处临时选择状态。
BIZ_HTTP_STATUS = {
    E.USER_NOT_FOUND: status.HTTP_404_NOT_FOUND,
    E.USER_ALREADY_EXISTS: status.HTTP_409_CONFLICT,
    E.PAY_ORDER_NOT_FOUND: status.HTTP_404_NOT_FOUND,
    E.PAY_ORDER_NOT_CANCELLABLE: status.HTTP_409_CONFLICT,
}

HTTP_ERROR_CODES = {
    400: E.BAD_REQUEST,
    401: E.UNAUTHORIZED,
    403: E.FORBIDDEN,
    404: E.NOT_FOUND,
    409: E.CONFLICT,
    422: E.VALIDATION_ERROR,
    429: E.TOO_MANY_REQUESTS,
}


def error_response(
    request: Request,
    *,
    status_code: int,
    error: E,
    msg: str | None = None,
    data: dict | None = None,
    headers: dict[str, str] | None = None,
) -> JSONResponse:
    request_id = getattr(request.state, "request_id", None) or uuid4().hex
    request.state.request_id = request_id
    body = ErrorModel(
        code=error.code,
        msg=error.msg if msg is None else msg,
        data=data,
        request_id=request_id,
    )
    response = JSONResponse(
        status_code=status_code,
        content=jsonable_encoder(body),
        headers=headers,
    )
    # 500 处理发生在普通用户中间件外层，因此这里也直接设置响应头。
    response.headers["X-Request-ID"] = request_id
    return response


def log_server_error(request: Request, exc: Exception):
    # 使用路由模板，不把原始查询串、请求体或认证头直接写入日志。
    route = getattr(request.scope.get("route"), "path", "<unmatched>")
    logger.error(
        "Server error request_id=%s method=%s route=%s",
        request.state.request_id,
        request.method,
        route,
        exc_info=(type(exc), exc, exc.__traceback__),
    )


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(BizException)
    async def handle_biz_error(request: Request, exc: BizException):
        status_code = BIZ_HTTP_STATUS.get(exc.error_code)
        if status_code is None:
            # 漏配映射属于服务端配置缺陷，不悄悄回退成 HTTP 400。
            return await handle_unexpected_error(request, exc)
        return error_response(
            request, status_code=status_code, error=exc.error_code, data=exc.data
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(request: Request, exc: RequestValidationError):
        return error_response(
            request,
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            error=E.VALIDATION_ERROR,
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

    @app.exception_handler(StarletteHTTPException)
    async def handle_http_error(request: Request, exc: StarletteHTTPException):
        is_server_error = exc.status_code >= 500
        error = (
            E.INTERNAL_ERROR if is_server_error
            else HTTP_ERROR_CODES.get(exc.status_code, E.HTTP_ERROR)
        )
        response = error_response(
            request,
            status_code=exc.status_code,
            error=error,
            # 4xx detail 必须由应用保证可公开；5xx 不返回内部 detail。
            msg=exc.detail if not is_server_error and isinstance(exc.detail, str) else None,
            headers=exc.headers,
        )
        if is_server_error:
            log_server_error(request, exc)
        return response

    @app.exception_handler(Exception)
    async def handle_unexpected_error(request: Request, exc: Exception):
        response = error_response(
            request,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error=E.INTERNAL_ERROR,
        )
        log_server_error(request, exc)
        return response
```

**处理器的职责边界**

- 业务失败和请求校验失败通常不打印堆栈；按需要记录业务事件、计数和少量上下文。未知故障才作为系统错误处理，不通过 `str(exc)` 向客户端暴露细节。
- 注册 Starlette 的 `HTTPException`，可以同时覆盖 FastAPI 主动抛出的 HTTP 异常和框架生成的 404、405；保留 `exc.headers`，避免丢失 `WWW-Authenticate`、`Allow`、`Retry-After` 等头。
- `HTTPException` 应在路由或依赖等异常处理覆盖范围内抛出。中间件若需提前拒绝请求，应直接返回相应响应，不要假定路由异常处理器会捕获中间件抛出的 `HTTPException`。
- 校验响应只提取 `loc`、`msg`、`type`，不直接返回 `exc.body`、`input`、`ctx`；自定义校验器的提示也不要拼入敏感数据。
- `HTTPException` 用于表达 4xx、5xx 等 HTTP 错误；不要拿它生成成功响应。
- 本例把非字符串 HTTP `detail` 替换为公共提示；需要结构化错误时，使用约定的业务异常或显式设计对应处理器。
- 500 兜底仅适用于仍能生成 HTTP 响应的阶段。后台任务、流式响应开始发送后发生的异常，无法改写已经发送的状态码和响应体；需要单独记录和处理失败。
- 堆栈中的异常消息本身也可能带有 SQL 参数或业务数据，日志采集链路应配置脱敏和访问控制；不主动记录请求体，并不代表堆栈天然没有敏感信息。
- Starlette 在执行 500 处理器后仍会将原异常向外抛出，Uvicorn 或错误采集系统可能再次记录。实际部署应确定一个完整堆栈的主要采集入口并配置去重；不要为减少日志而在普通中间件中吞掉异常。

> 数据库事务应在服务或事务依赖的边界管理：需要原子性的操作在提交成功后才报告成功，异常时回滚并释放资源。异常处理器不负责提交或回滚，也不要把所有数据库异常都转换成“业务失败”。只转换能够明确识别的情况，例如已知唯一约束冲突；其他错误继续抛出。

## 创建自定义异常码

> **`app/core/exceptions/codes.py`**

```python
from enum import Enum, unique


@unique
class E(Enum):
    """稳定的业务码与公开提示；HTTP 状态另在 API 层映射。"""

    """
    自定义错误码
    格式: <业务>_<错误类型> = (code, msg)
    """

    # 公共错误
    HTTP_ERROR = (10000, "请求失败")
    BAD_REQUEST = (10001, "请求不合法")
    UNAUTHORIZED = (10401, "认证失败")
    FORBIDDEN = (10403, "无权访问")
    NOT_FOUND = (10404, "资源不存在")
    CONFLICT = (10409, "资源状态冲突")
    VALIDATION_ERROR = (10400, "参数验证失败")
    TOO_MANY_REQUESTS = (10429, "请求过于频繁")
    INTERNAL_ERROR = (10500, "服务暂时无法完成请求")

    # 用户业务
    USER_NOT_FOUND = (20000, "用户不存在")
    USER_ALREADY_EXISTS = (20001, "用户已存在")

    # 订单业务
    PAY_ORDER_NOT_FOUND = (30000, "订单不存在")
    PAY_ORDER_NOT_CANCELLABLE = (30001, "当前订单状态不允许取消")

    @property
    def code(self) -> int:
        """获取错误码"""
        return self.value[0]

    @property
    def msg(self) -> str:
        """获取错误码码信息"""
        return self.value[1]
```

- 业务码是项目约定，不要求和 HTTP 状态数字对应，例如 `10400` 在本例中对应 HTTP 422。已发布的业务码不要改变含义或分配给其他错误。
- 每个失败原因有稳定、明确的码；“用户已存在”和“数据库连接失败”不能都归为“用户注册失败”。登录时对外使用统一的认证失败提示，避免区分账号不存在与密码错误。
- 新增业务码时同步补充 `BIZ_HTTP_STATUS`、接口声明和测试。本例未映射的业务码会返回 500，便于发现遗漏；应在测试中提前检查覆盖情况。
- `@unique` 能发现完全相同的枚举值，但不能阻止 `(20000, "提示 A")` 与 `(20000, "提示 B")` 共用数字；还需检查 `len({e.code for e in E}) == len(E)`。
- 本例将码表集中展示。项目较大时按业务模块拆分，但公共格式和码的分配规则保持一致；历史码的退役和兼容按接口版本管理。

## 挂载注册异常

> **`app/main.py`**；以下文件与前面的异常模块、后面的路由示例组成同一个应用。

```python
from uuid import uuid4

from fastapi import FastAPI, Request

from app.api.v1.users import router as users_router
from app.core.exceptions.errors import ErrorModel
from app.core.exceptions.handlers import register_exception_handlers


app = FastAPI(
    debug=False,
    responses={
        422: {"model": ErrorModel, "description": "请求参数校验失败"},
        500: {"model": ErrorModel, "description": "服务端错误"},
    },
)
register_exception_handlers(app)


@app.middleware("http")
async def attach_request_id(request: Request, call_next):
    # 服务端生成，避免直接信任客户端传入的任意请求标识。
    request.state.request_id = uuid4().hex
    response = await call_next(request)
    response.headers["X-Request-ID"] = request.state.request_id
    return response


app.include_router(users_router)
```

- 生产环境关闭 `debug`，否则未处理错误可能返回调试堆栈；日志 handler、格式、输出目的地和告警在应用启动或部署配置中统一设置。
- 错误体与响应头携带相同 `request_id`，用于关联日志；成功响应只增加该响应头，不强制修改已有响应体。已有链路追踪时可按团队规范关联 trace ID，不必另建一套无关联标识。
- 浏览器跨域读取 `X-Request-ID` 时，需要把它加入 CORS 的 `expose_headers`。需要 500 响应也携带 CORS 头时，按 Starlette 的全局 CORS 包裹方式配置，避免最外层错误响应绕过普通 CORS 中间件。
- 注册异常处理器不会自动修改 OpenAPI 错误模型。这里声明公共的 422、500，各路由再声明实际会返回的业务状态；这只是文档声明，不会自动实现异常处理。

## 路由中使用

> **`app/api/v1/users.py`**

```python
from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.core.exceptions.codes import E
from app.core.exceptions.errors import BizException, ErrorModel


router = APIRouter(prefix="/users", tags=["用户"])


class UserCreate(BaseModel):
    username: str = Field(min_length=1, max_length=50)


@router.get("/{user_id}", responses={404: {"model": ErrorModel}})
def read_user(user_id: int):
    # 固定数据仅演示异常；实际查询与业务校验应放到服务层。
    if user_id != 1:
        raise BizException(E.USER_NOT_FOUND)
    return {"id": 1, "username": "alice"}


@router.post("", status_code=201, responses={409: {"model": ErrorModel}})
def create_user(data: UserCreate):
    if data.username == "alice":
        raise BizException(E.USER_ALREADY_EXISTS)
    # 仅演示成功响应，不实际写入数据库。
    return {"id": 2, "username": data.username}
```

访问 `GET /users/2` 返回 HTTP 404，示例响应如下；`X-Request-ID` 与响应体中的标识一致。

```json
{
  "code": 20000,
  "msg": "用户不存在",
  "data": null,
  "request_id": "e3ca52a95c634974a3c4f6329d86915a"
}
```

认证等 HTTP 入口问题可以继续使用 `HTTPException`；在本章 Bearer 认证场景中，认证失败这样抛出即可由公共处理器转换格式，并保留认证头：

```python
from fastapi import HTTPException

raise HTTPException(
    status_code=401,
    detail="认证失败",
    headers={"WWW-Authenticate": "Bearer"},
)
```

**处理范围与验收速查**

| 检查场景 | 预期结果 |
| --- | --- |
| `GET /users/1` | HTTP 200，正常数据 |
| `GET /users/2` | HTTP 404，业务码 `20000` |
| `POST /users`，提交 `{"username": "alice"}` | HTTP 409，业务码 `20001` |
| `GET /users/not-an-int` 或提交缺少 `username` 的请求 | HTTP 422，业务码 `10400`，返回字段错误 |
| 访问未注册路径／使用不支持的方法 | 统一错误格式，保留 404／405；405 保留 `Allow` |
| Bearer 认证失败 | HTTP 401，业务码 `10401`，保留 `WWW-Authenticate` |
| 未处理异常／响应模型校验失败 | HTTP 500，业务码 `10500`；客户端看不到内部错误，日志有堆栈和请求标识 |

监控分别统计业务拒绝与系统故障，并关联接口、状态和请求标识；业务失败率升高不等同于程序故障，系统故障也不能仅靠业务码报表发现。

自动化测试还应校验业务码数字唯一、业务映射完整、OpenAPI 中的 422 模型与实际一致，以及必要的事务回滚和敏感信息保护。测试 500 响应时使用 `TestClient(app, raise_server_exceptions=False)`；默认客户端会重新抛出服务端异常，不能据此判断 500 处理器没有执行。

**已有“全部 HTTP 200”协议如何兼容**

已有客户端依赖 `code` 时，不直接切换旧接口状态。将兼容逻辑限定在明确的旧版本入口，仅对约定的业务拒绝保留原协议，并独立统计业务失败率；新版本使用本节约定。认证、参数校验等旧行为的变更要和客户端一起迁移，系统故障不要继续扩展成 HTTP 200。

> 本方案统一的是应用能够生成的 HTTP 错误响应；代理层生成的错误、网络故障以及已开始发送响应后的失败，需要客户端和基础设施分别处理。
>
> 参考：[FastAPI 错误处理 ↪](https://fastapi.tiangolo.com/zh/tutorial/handling-errors/)、[额外响应与 OpenAPI ↪](https://fastapi.tiangolo.com/zh/advanced/additional-responses/)、[Starlette 异常处理 ↪](https://starlette.dev/exceptions/)、[全局 CORS 配置 ↪](https://starlette.dev/middleware/#corsmiddleware)。


# 中间件

你可以向 **FastAPI** 应用添加中间件。

**中间件** 是一个函数，它在每个**请求**被特定的路径操作处理之前，以及在每个**响应**返回之前工作。

![中间件执行流程](../imgs/middleware_model.jpg)

> 如果你使用了 `yield` 关键字依赖，依赖中的退出代码会在请求处理流程的后续阶段执行。
>
> 如果有后台任务（见本节末尾），它们会在响应发送后运行。

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

**响应发送后执行轻量任务：`BackgroundTasks`**

下面是独立示例。`add_task()` 接收函数和参数，不要提前执行函数：

```python
import logging
from fastapi import BackgroundTasks, FastAPI, status

app = FastAPI()
logger = logging.getLogger("api.tasks")


def record_notification(email: str):
    # 示例只记录日志，实际项目可替换为轻量通知等操作。
    logger.info("处理通知：%s", email)


@app.post("/notifications", status_code=status.HTTP_202_ACCEPTED)
def notify(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(record_notification, email)
    return {"msg": "任务已接收"}
```

`email` 在此是查询参数，例如 `/notifications?email=alice@example.com`。后台函数可以是 `def` 或 `async def`；普通 `def` 任务在线程池运行，`async def` 任务仍需避免直接执行阻塞操作。

> `BackgroundTasks` 运行在应用进程中，不提供持久化队列、自动重试或进程重启后的任务恢复。长时间计算或必须可靠完成的任务应交给专门的任务系统。后台异常发生时响应已经发送，不能再修改客户端收到的状态码；需要记录日志并按业务处理失败。任务应传入标识或独立数据，避免依赖已经关闭的请求级资源。
>
> 参考：[后台任务 ↪](https://fastapi.tiangolo.com/zh/tutorial/background-tasks/)。

# 日志管理

| 日志方案     | 主流程度 | 特点                          | 推荐场景                     |
| ------------ | -------- | ----------------------------- | ---------------------------- |
| logging      | ⭐⭐⭐⭐⭐    | Python 标准库，生态兼容性最好 | 企业项目、复杂系统           |
| loguru       | ⭐⭐⭐⭐     | 简单易用，开箱即用            | FastAPI、AI 项目、中小型服务 |
| structlog    | ⭐⭐⭐⭐     | 结构化日志，JSON 日志友好     | 微服务、云原生、日志分析     |
| rich.logging | ⭐⭐⭐      | 终端输出美观                  | CLI、开发调试                |
| logbook      | ⭐⭐       | API 设计简洁                  | 部分特定项目                 |

> 提示：如果你现在在开发 Python 后端，尤其是 FastAPI 项目，Loguru 是一个非常不错的选择。

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

> 本例只配置 Loguru。前面异常处理使用的标准库 `logging`，以及 Uvicorn 自身的日志，不会自动获得相同格式；需要统一日志时再配置标准库日志或转接处理器。查问题时可记录请求路径、耗时和业务标识，避免输出密码、完整令牌和数据库连接串。

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
    # 允许前端 JavaScript 跨域读取的额外响应头
    expose_headers=["X-Process-Time"],
)


@app.get("/")
async def main():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)

```

**常见排查点**

- 源由协议、主机和端口共同决定；`http://localhost:8080`、`http://127.0.0.1:8080` 和 `https://localhost:8080` 是不同的源，需按实际前端地址配置。
- `allow_headers` 允许客户端发送哪些请求头；`expose_headers` 允许前端读取哪些响应头。若结合前面的计时中间件，前端才能跨域读取 `X-Process-Time`；本示例单独运行不会自行生成该响应头。
- 浏览器的 `OPTIONS` 预检通常由 `CORSMiddleware` 处理；实际请求仍需有匹配的路由、方法和认证信息。
- CORS 是浏览器的跨域访问规则，不能代替认证和权限校验。`curl` 请求成功，也不能证明浏览器端的 CORS 配置正确。

> 参考：[CORS ↪](https://fastapi.tiangolo.com/zh/tutorial/cors/)。

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
"""
定义配置结构、类型、默认值、验证规则
"""

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

3）根目录新建 **`.env`** 文件，填写环境变量

```
DATABASE_URL=postgresql+asyncpg://user:password@host:port/db_name
DEBUG=true
```

4）读取配置

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
    return {"settings": {"debug": settings.debug}}  # 仅返回明确允许公开的字段


"""
开发服务器启动
"""
if __name__ == "__main__":
    uvicorn.run("app.main:app", port=8080, reload=True)
```

> `get_settings()` 使用 `@lru_cache` 后，在当前进程内复用配置对象；多个 worker 各有自己的缓存。首次读取后修改 `.env` 不会自动刷新缓存，通常通过重启应用重新加载；测试时可以调用 `get_settings.cache_clear()`。

**配置查阅要点**

- 同名配置同时存在于系统环境变量和 `.env` 时，系统环境变量优先。该优先级适用于这里的默认 Settings 配置，不涉及自定义配置源。
- 当前 `database_url=""` 适合展示可选默认值；如果服务必须依赖数据库，应改为无默认值的必填字段，并在启动阶段读取配置，让缺失配置尽早报错。
- `Settings` 可能包含密钥、密码和连接串，不要把整个对象直接返回给客户端，也不要将完整 `model_dump()` 写入日志。

> 参考：[配置与环境变量 ↪](https://fastapi.tiangolo.com/zh/advanced/settings/)。

# 部署

**共享资源的创建与关闭：`lifespan`**

应用启动时创建、关闭时释放的 HTTP 客户端、数据库连接池等，可以交给 `lifespan` 管理。下面是独立的 `main.py` 示例；`httpx` 已包含在 `fastapi[standard]` 中，使用精简依赖时可执行 `uv add httpx` 安装。

```python
from contextlib import asynccontextmanager
import httpx
from fastapi import FastAPI, Request


@asynccontextmanager
async def lifespan(app: FastAPI):
    # yield 之前：应用开始接收请求前执行。
    async with httpx.AsyncClient(timeout=10.0) as client:
        app.state.http_client = client
        yield
    # 离开 async with 时关闭客户端，释放连接等资源。


app = FastAPI(lifespan=lifespan)


@app.get("/health")
async def health(request: Request):
    client: httpx.AsyncClient = request.app.state.http_client
    return {"status": "ok", "http_client_closed": client.is_closed}
```

`/health` 在这里仅演示读取共享资源，不会发起外部请求。启动完成后 `http_client_closed` 为 `false`；应用关闭时客户端被释放。

> `lifespan` 管理当前应用进程的生命周期，每个 worker 都会创建自己的资源。请求级资源可用 `yield` 依赖管理。新代码优先使用 `lifespan`；配置它后，不要再依赖 `@app.on_event("startup")` / `shutdown` 的事件处理器来做同一套初始化与清理。
>
> 参考：[生命周期事件 ↪](https://fastapi.tiangolo.com/zh/advanced/events/)。

**启动命令速查**

开发环境可以使用：

```shell
$ uv run uvicorn app.main:app --reload
```

生产环境应关闭 `--reload`，并根据服务器资源配置 worker 数量：

```shell
$ uv run fastapi run app/main.py --workers 2
```

`app/main.py` 适用于前面多文件项目的入口；若使用根目录的 `main.py`，对应改为 `uv run fastapi run main.py --workers 2`。

> worker 数量应结合 CPU、内存、连接池大小和部署方式确定，不是越多越好。多个 worker 不共享普通 Python 全局变量或内存缓存。生产启动命令之外，HTTPS、反向代理、进程重启和入口请求大小限制等，按部署环境配置。

**部署前的最小测试：`TestClient` + pytest**

安装测试依赖：

```shell
$ uv add --dev pytest httpx
```

以下 `tests/test_main.py` 对应安全一节的根目录 `main.py` 和 `app/core/security.py`。先按安全一节设置 `SECRET_KEY`，再从项目根目录运行。参数校验测试自行创建最小应用，独立展示 422 行为。

```python
from fastapi import FastAPI
from fastapi.testclient import TestClient
from main import app
from app.core.security import create_access_token


def test_public_api():
    with TestClient(app) as client:
        response = client.get("/public")
    assert response.status_code == 200
    assert response.json() == {"message": "公开接口"}


def test_profile_requires_token():
    with TestClient(app) as client:
        response = client.get("/profile1")
    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"


def test_profile_with_valid_token():
    token = create_access_token(1)
    with TestClient(app) as client:
        response = client.get(
            "/profile1", headers={"Authorization": f"Bearer {token}"}
        )
    assert response.status_code == 200
    assert response.json() == {"user_id": "1"}


def test_profile_with_invalid_token():
    with TestClient(app) as client:
        response = client.get(
            "/profile1", headers={"Authorization": "Bearer invalid-token"}
        )
    assert response.status_code == 401


def test_request_validation():
    validation_app = FastAPI()

    @validation_app.get("/items/{item_id}")
    def read_item(item_id: int):
        return {"item_id": item_id}

    with TestClient(validation_app) as client:
        assert client.get("/items/1").json() == {"item_id": 1}
        assert client.get("/items/not-an-int").status_code == 422
```

执行：

```shell
$ uv run python -m pytest -q
```

> 测试函数可以使用普通 `def`，`TestClient` 的请求也不需要 `await`。使用 `with TestClient(app)` 才会触发应用的 `lifespan`。涉及数据库、外部服务或固定测试配置时，可以用 `app.dependency_overrides[原依赖] = 测试依赖` 替换依赖，并在 `finally` 中移除本次覆盖，避免影响其他测试。
>
> 参考：[测试 ↪](https://fastapi.tiangolo.com/zh/tutorial/testing/)、[测试依赖覆盖 ↪](https://fastapi.tiangolo.com/zh/advanced/testing-dependencies/)。

更多内容参考：[FastAPI 部署文档 ↪](https://fastapi.tiangolo.com/zh/deployment/)
