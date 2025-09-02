# 概述

https://www.cnblogs.com/ltyc/p/18664047

FastAPI 是一个用于构建 API 的现代、快速（高性能）的 web 框架，使用 Python 并基于标准的 Python 类型提示。

FastAPI 是建立在 Starlette 和 Pydantic 基础上的。

Pydantic 是一个基于Python类型提示来定义数据验证、序列化和文档的库。

Starlete 是种轻量级的ASGI框架/工具包，是构建高性能Asyncio服务的理性选择。

> - [Starlette ↪](https://www.starlette.io/) 负责 Web 部分（Asyncio）
> - [Pydantic ↪](https://docs.pydantic.dev/latest/) 负责数据部分（类型提示）

FastApi 是站在前人肩膀上，集成了多种框架的优点的新秀框架。它出现的比较晚，2018年底才发布在 GitHub 上。广泛应用于当前各种
前后端分离的项目开发，测试运维自动化以及微服务的场景中。

> 参考：
>
> 1. [三小时学会【fastapi框架教程】从入门到精通 ↪](https://www.bilibili.com/video/BV1cedVYWEE7?spm_id_from=333.788.videopod.episodes&vd_source=b539518f043998f08c722489225f1c3c&p=13)
> 2. [官方指南 ↪](https://fastapi.tiangolo.com/zh/)

# 预备知识

## HTTP 协议

HTTP 协议是 Hyper Text Tramnsfer Protocol（超文本传输协议）的缩写，是用于万维网（WWW，**W**orld **W**ide **w**eb）服务器与本地浏览器之间传输超文本的传送协议。HTTP是一个属于应用层的面向对象的协议，由于其简捷、快速的方式，适用于分布式超媒体信息系统。它于1990年提出，经过几年的使用与发展，得到不断地完善和扩展。HTTP协议工作于客户端-服务端架构为上。浏览器作为HTTP客户端通过URL向HTTP服务端即WEB服务器发送所有请求。Web服务器根据接收到的请求后，向客户端发送响应信息。

### HTTP 协议特性

1. **基于TCP/IP协议** 

   HTTP 协议是基于 TCP/IP 协议之上的应用层协议

2. **基于请求 — 响应模式**

   HTTP协议规定，请求从客户端发出，最后服务器端响应该请求并返回。换句话说，肯定是先从客户端开始建立通信的，服务器端在没有接收到请求之前不会发送响应。

3. **无状态**

   HTTP是一种不保存状态，即无状态（statcless）协议。HTTP协议自身不对请求和响应之间的通信状态进行保存。也就是说在HTTP这个 级别，协议对于发送过的请求或响应都不做持久化处理。

   使用HTTP协议，每当有新的请求发送时，就会有对应的新响应产生。协议本身并不保留之前一切的请求或响应报文的信息。这是为了更快地处理大量事务，确保协议的可伸缩性，而特意把HTTP协议设计成如此简单的。

4. **短连接**

   HTTP1.0默认使用的是短连接。浏览器和服务器每进行一次HTTP操作，就建立一次连接，任务结束就中断连接。
   HTTP/1.1起，默认使用长连接。要使用长连接，客户端和服务器的HTTP首部的Connection都要设置为 `keep-alive`，才能支持长连接。
   HTTP长连接，指的是复用TCP连接。多个HTTP请求可以复用同一个TCP连接，这就节省了TCP连接建立和断开的消耗。

### HTTP 请求协议与响应协议

![](../imgs/soket.jpg)

HTTP 协议包含由浏览器发送数据到服务器需要遵循的请求协议与服务器发送数据到浏览器需要遵循的请求协议。用于HTTP协议交互的信被为HTTP报文。请求端(客户端)的HTTP报文 做请求报文,响应端(服务器端)的 做响应报文。HTTP报文本身是由多行数据构成的字文本。

**DIY一个WEB应用程序测试http 协议格式**

```python
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("127.0.0.1", 5173))  # 正确写法
server_socket.listen(5)
print("服务器已启动，监听端口 5173...")


try:
    while True:
        conn, addr = server_socket.accept()  # 阻塞等待客户端连接
        data = conn.recv(1024)
        print(f"客户端发送的请求信息：\n{data}")
        conn.send(b"HTTP/1.1 200 ok\r\nserver:lee\r\n\r\nHello, World!")
        conn.close()
except Exception as e:
    print(e)
finally:
    server_socket.close()
```

**DIY一个WEB应用程序测试 Content-Type**

```python
# WEB应用程序：遵循HTTP协议

import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("127.0.0.1", 5173))  # 正确写法
server_socket.listen(5)
print("服务器已启动，监听端口 5173...")


try:
    while True:
        conn, addr = server_socket.accept()  # 阻塞等待客户端连接
        data = conn.recv(1024)
        print(f"客户端发送的请求信息：\n{data}")
        conn.send(
            b'HTTP/1.1 200 ok\r\nserver:lee\r\ncontent-type:application/json\r\n\r\n{"user_id": 1001}'
        )
        conn.close()
except Exception as e:
    print(e)
finally:
    server_socket.close()

```

## API接口

在开发Web应用中，有两种应用模式:

1. 前后端不分离 — 客户端看到的内容和所有界面效果都是由服务端提供出来的
2. 前后端分离 — 把前端的界面效果（html，css，js）分离到另一个服务端，Python服务端只需要返回数据即可

应用程序编程接口（**A**pplication **P**rogramming **l**nterace，API接口），就是应用程序对外提供了一个操作数据的入口，这个入口可以是一个函数或类方法，也可以是一个url地址或者一个网络地址。当客户端调用这个入口，应用程序则会执行对应代码操作，给客户端完成相对应的功能。

当然，api接口在工作中是比较常见的开发内容，有时候，我们会调用其他人编写的api接口，有时候，我们也需要提供api接口给其他人操作。由此就会带来一个问题，api接口往往都是一个函数、类方法、或者url或其他网络地址，不管是哪一种，在api接口编写过程中，我们都要考虑一个问题就是这个接口应该怎么编写？接口怎么写的更加容易维护和清晰，这就需要大家在调用或者编写api接口的时候要有一个明确的编写规范！！！

为了在团队内部形成共识、防止个人习惯差异引起的混乱，我们都需要找到一种大家都觉得很好的接口实现规范，而且这种规范能够让后端写的接口，用途一目了然，减少客户端和服务端双方之间的合作成本。

目前市面上大部分公司开发人员使用的接口实现规范主要有：RESTful API、RPC。

REST全称是 Representational State Transfer，中文意思是表述（编者注：通常译为表征）性状态转移。 它首次出现在2000年Roy
Fielding 的博士论文中。

RESTful是一种专门为Web 开发而定义API接口的设计风格，尤其适用于前后端分离的应用模式中。

关键：面向资源开发

这种风格的理念认为后端开发任务就是提供数据的，对外提供的是数据资源的访问接口，所以在定义接口时，客户端访问的URL路径就表示这种要操作的数据资源。

而对于数据资源分别使用 POST、DELETE、GET、UPDATE 等请求动作来表达对数据的增删查改。

| 请求方法 | 请求地址     | 后端操作        |
| :------- | :----------- | :-------------- |
| POST     | `/student/`  | 增加学生        |
| GET      | `/student/`  | 获取所有学生    |
| GET      | `/student/1` | 获取ID为1的学生 |
| PUT      | `/student/1` | 修改ID为1的学生 |
| DELETE   | `/student/1` | 删除ID为1的学生 |

RESTful 规范是一种通用的规范，不限制语言和开发框架的使用。事实上，我们可以使用任何一门语言，任何一个框架都可以实现符合
RESTful 规范的API接口。

# 快速体验

构建项目：

```shell
💬 进入主目录
$ cd 
💬 创建一个用于存放所有代码工程的目录
$ mkdir code
💬 进入 code 目录
$ cd code
💬 创建一个用于存放这个工程的目录
$ mkdir fastapi_tutorial
💬 进入这个工程的目录
$ cd fastapi_tutorial
```

创建虚拟环境：

```shell
$ conda env -n fastapi_tutorial python=3.13.2
$ conda activate fastapi_tutorial
```

> **提示**：每次你在这个环境中安装一个 **新的包** 时，都需要 **重新激活** 这个环境。

检查虚拟环境是否激活：

```shell
$ which python
/opt/homebrew/Caskroom/miniconda/base/envs/fastapi_tutorial/bin/python
```

> **提示**：如果它显示在 `envs` 目录下，那么它就生效了 🎉。

升级 pip，如果你使用 `pip` 来安装包（它是 Python 的默认组件），你应该将它 **升级** 到最新版本。

在安装包时出现的许多奇怪的错误都可以通过先升级 `pip` 来解决。

通常你只需要在创建虚拟环境后 **执行一次** 这个操作。

```shell
$ python -m pip install --upgrade pip
```

安装依赖：
```shell
$ pip install fastapi
```

你还会需要一个 ASGI 服务器，生产环境可以使用 [Uvicorn ↪](https://www.uvicorn.org/) 或者 [Hypercorn ↪](https://github.com/pgjones/hypercorn)。

```shell
$ pip install "uvicorn[standard]"
```

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
$ uvicorn main:app --reload
INFO:     Will watch for changes in these directories: ...
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [35811] using WatchFiles
ERROR:    Error loading ASGI app. Could not import module "main".
```

> 注意：指令中的 `main` 是执行文件名，假设你的文件是 `index.py`，那么启动指令就是：`uvicorn index:app --reload`

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
6. 运行开发服务器，如：`uvicorn main:app --reload`

此外，FastAPI 有着非常棒的交互式 API文档，这一点很吸引人，跳转到 http://127.0.0.1:8000/docs，你将会看到自动生成的交互式 API 文档。关于文档的配置细节，可以参考 [这里 >>](https://fastapi.tiangolo.com/zh/tutorial/metadata/)

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
    uvicorn.run("main:app", port=8080, reload=True)
```

[http://127.0.0.1:8080/docs ↪ ](http://127.0.0.1:8080/docs)

![](../imgs/router_methods.jpg)

路径操作装饰器参数：

```python
@app.post(
    "/items/{item_id}",
    response_model=Item,
    status_code=status.HTTP_200_OK
    tags=["AAA"],
    summary="this is summary",
    description="this is description",
    response_deseription="this is response_description",
    deprecated=False,
)
```

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


router = APIRouter(prefix="/user")


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


router = APIRouter(prefix="/works")


@router.get("/", summary="作品列表")
async def list():
    return {"code": 200, "data": [1, 2, 3], "msg": "success"}


@router.get("/{id}", summary="作品详情")
async def details():
    return {"code": 200, "data": {"id": 1}, "msg": "success"}
```

> **`app/api/api/__init__.py`**

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
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent)) # 添加项目根目录到Python路径

from app.api.v1 import router as api_router
from fastapi import FastAPI
import uvicorn

app = FastAPI()

app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)
```

[http://127.0.0.1:8080/docs ↪ ](http://127.0.0.1:8080/docs)

![](../imgs/include_router.jpg)

# 请求与响应

## 路径参数

**（1）基本用法**

FastAPI 支持使用 Python 字符串格式化语法声明**路径参数**（**变量**）

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

本例把 `item_id` 的类型声明为 `int`。

> 类型声明将为函数提供错误检查、代码补全等编辑器支持。

**（3）注意顺序**

在创建 **路径操作** 时，你会发现有些情况下路径是固定的。

比如 `/users/me`，我们假设它用来获取关于当前用户的数据。

然后，你还可以使用路径 `/user/{username}` 来通过用户名获取关于特定用户的数据。

由于路径操作是 **按顺序依次运行** 的，你需要确保路径 `/user/me` 声明在路径 `/user/{username}` 之前。

## 查询参数

声明的参数不是路径参数时，路径操作函数会把该参数自动解释为**查询**参数。

查询参数就是 `ur?` 之后用 `&` 分割的 `key-value` 键值对。

```python
import uvicorn
from fastapi import FastAPI
from typing import Union, Optional

app = FastAPI()


@app.get("/job/{kd}")
async def get_jobs(kd: str, xl: Union[str, None] = None, gj: Optional[str] = None):
    # 基于 kd, xl, gj 数据库查询岗位信息（拉勾网）
    return {
        "kd": kd,
        "xl": xl,
        "gj": gj,
    }


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
```

在这个例子中，函数参数 `xl` 和 `gj` 是可选的，并且默认值为 None

自 python3.5 开始，PEP484为 Python 引入了类型注解（type hints），typing 的主要作用有：

> 1. 类型检查，防止运行时出现参数、返回值类型不符。
> 2. 作为开发文档附加说明，方便使用者调用时传入和返回参数类型。
> 3. 模块加入不会影响程序的运行不会报正式的错误，pycharm 支持 typing 检查错误时会出现黄色警告。

`type hints` 主要是要指示函数的输入和输出的数据类型，数据类型在 typing 包中，基本类型有 `str` `list` `dict` 等等。

`Union` 是当有多种可能的数据类型时使用，比如函数有可能根据不同情况有时返回 `str` 或返回 `list`，那么就可以写成 `Union[list, str]`，`Optional` 是`Union`的一个简化， 当 数据类型中有可能是None时，比如有可能是`str`也有可能是`None`，则`Optional[str],` 相当于`Union[str, None]`

**📖 查询参数校验**

```python
import uvicorn
from fastapi import FastAPI, Query
from typing import Union

app = FastAPI()


@app.get("/items/")
async def read_items(
    # 查询参数 q 的默认值为 None，最小长度为 3，最大长度为 50
    q: Union[str, None] = Query(default=None, min_length=3, max_length=50),
):
    pass


if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)
```

**📖 查询参数模型**

```python
import uvicorn
from typing import Annotated, Optional
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()


class FilterParams(BaseModel):
    page: int = Field(1, gt=0)
    size: int = Field(10, gt=0, le=100)
    keywords: Optional[str] = Field(None)


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

 `Pydantic` 主要用来做类型强制检查（校验数据），不符合类型要求就会抛出异常。

对于 API 服务，支持类型检查非常有用，会让服务更加健壮，也会加快开发速度，因为开发者再也不用自己写一行一行的做类型检查。

安装依赖：

```shell
$ pip install pydantic
```

代码示例：

```python
import uvicorn
from fastapi import FastAPI
from typing import Union, Optional
from pydantic import BaseModel, Field, field_validator
from datetime import date
from typing import List

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
    birth: Union[date, None] = None
    # 描述信息
    description: Optional[str] = None
    # 兴趣爱好
    interest: List[str] = []
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
async def user(user: User):
    print(user, type(user))
    print(f"user.name >>> {user.name}")
    print(user.model_dump())
    return user


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

```

## form 表单数据

在 OAuth2 规范的一种使用方式（密码流）中，需要将用户名、密码作为表单字段发送，而不是 JSON。

FastAPI 可以使用Form组件来接收表单数据，需安装依赖 `python-multipart`：

```shell
$ pip install python-multipart
```

```python
import uvicorn
from fastapi import FastAPI, Form

app = FastAPI()


@app.post("/register")
async def register(
    username: str = Form(..., min_length=8, max_length=8, pattern="[a-zA-Z]{8}"),
    password: str = Form(..., min_length=8, max_length=8, pattern="[0-9]{8}"),
):
    print(f"username = {username}, password = {password}")
    # 注册，实现数据库添加操作...
    return {"username": username}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
```

## 文件上传

```python
import os
import uvicorn
from fastapi import FastAPI, File, UploadFile
from typing import List

app = FastAPI()


# file: bytes = File()：适合小文件上传
@app.post("/file", summary="文件上传")
async def file(file: bytes = File()):
    return {"file_size": len(file)}


@app.post("/multiFiles", summary="多文件上传")
async def multi_files(files: List[bytes] = File()):
    return {"file_sizes": [len(file) for file in files]}


# 最佳示例
os.makedirs("images", exist_ok=True)


# file: UploadFile：适合大文件上传
@app.post("/uploadFile", summary="文件上传")
async def upload_file(file: UploadFile):
    # 文件保存
    path = os.path.join("images", file.filename or "xxx.jpg")
    with open(path, "wb") as f:
        # 使用chunk方式写入（适合大文件）
        while content := await file.read(1024 * 1024):  # 每次读取1MB
            f.write(content)
    return {"file": file.filename}


@app.post("/uploadFiles", summary="多文件上传")
async def upload_files(files: List[UploadFile]):
    # ...
    return {"names": [file.filename for file in files]}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
```

## Request 对象

有些情况下我们希望能直接访问 Request 对象。例如我们在路径操作函数中想获取客户端的IP地址，需要在函数中声明 **Request** 类型的参数，FastAPI 就会自动传递 Request 对象给这个参数，我们就可以获取到 Request 对象及其属性信息，例如 `header`、`url`、`cookie`、`session` 等。

```python
from fastapi import APIRouter, Request

app = APIRouter()


@app.get("/items")
async def items(request: Request):
    return {
        "请求URL": request.url,
        "请求IP": request.client.host,
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
from typing import Generic, TypeVar, Optional

app = FastAPI()

"""
定义全局响应模型
"""

T = TypeVar("T")


class BaseResponse(BaseModel, Generic[T]):
    code: int = 200
    message: str = "success"
    data: Optional[T] = None


"""
定义业务接口
"""


@app.get("/")
async def root():
    return BaseResponse(data="Hello World")


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)

```

## 静态文件

在 Web 开发中，有时需要请求存储在服务器的静态资源，如 css 或者图片，比如在我们将 `logo.jpg` 文件放置在 `static` 目录中，然后开放接口给前端访问，可以使用 `StaticFiles`从目录中自动提供静态文件。

```python
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
```

彼此，前端可以通过链接 http://127.0.0.1:8000/static/logo.jpg 访问到图片资源。

# 元数据和文档配置

@see https://fastapi.tiangolo.com/zh/tutorial/metadata/

# jinjia2 模板

要了解 jinja2，那么需要先理解模板的概念。模板在 Python 的 web 开发中广泛使用，它能够有效的将业务逻辑和页面逻辑分开，使代码可读性增强、并且更加容易理解和维护。

模板简单来说就是一个其中包涵占位变量表示动态的部分的文件，模板文件在经过动态赋值后，返回给用户。

jinja2 是 Flask 作者开发的一个模板系统，起初是仿 django 模板的一个模板引擎，为 Flask 提供模板支持，由于其灵活，快速和安全等优点被广泛使用。

在jinjia2中， 存在两种语法：

- 变量插值：`{{  }}`
- 控制结构：`{% %}`

 使用前，现安装 jinjia2：

```shell
$ pip install jinja2
```

## 模板语法 — 变量渲染

> **`main.py`**

```python
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import uvicorn


# 实例化 FastAPI 对象
app = FastAPI()
# 实例化 jinjia2 对象，并将文件夹路径设置为以 templates 命名的文件夹
templates = Jinja2Templates(directory="templates")


@app.get("/index")
async def index(request: Request):
    name = "root"
    age = 32
    books = ["西游记", "红楼梦", "三国演义", "聊斋志异"]
    info = {"name": "张三", "age": 32, "gender": "男"}

    return templates.TemplateResponse(
        # 模板文件
        "index.html",
        # context 上下文对象
        {
            # 注意：返回模板响应时，必须有 request 键值对，且值为 Request 请求对象
            "request": request,
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
        <li>{{ books.0 }}</li>
        <li>{{ books.1 }}</li>
        <li>{{ books.2 }}</li>
        <li>{{ books.3 }}</li>
      </ol>
    </div>
    <p>用户信息：{{ info.name }} - {{ info.age }} - {{ info.gender }}</p>
  </body>
</html>
```

## 模板语法 — 过滤器

变量可以通过 “过滤器” 进行修改，过滤器可以理解为是 jinja2 里面的内置函数和字符串处理函数。常用的过滤器有:

| 过滤器名称 | 说明                                         |
| ---------- | -------------------------------------------- |
| capitalize | 把值的首字母转换成大写，其他字母转换为小写   |
| lower      | 把值转换成小写形式                           |
| title      | 把值中每个单词的首字母都转换成大写           |
| trim       | 把值的首尾空格去掉                           |
| striptags  | 渲染之前把值中所有的HTML标签都删掉           |
| join       | 拼接多个值为字符串                           |
| round      | 默认对数字进行四舍五入，也可以用参数进行控制 |
| safe       | 渲染时值不转义                               |

那么如何使用这些过滤器呢?只需要在变量后面使用管道（`|`）分割，多个过滤器可以链式调用，前一个过滤器的输出会作为后一个过
滤器的输入。

```python
# Jinja2 过滤器代码示例及预期结果

{{ 'abc'|capitalize }}      # 输出: Abc
{{ 'abc'|upper }}           # 输出: ABC
{{ 'hello world'|title }}   # 输出: Hello World
{{ 'hello world'|replace('world', 'yuan')|upper }}  # 输出: HELLO YUAN
{{ 18.18|round|int }}      # 输出: 18
```

## 模板语法 — 控制结构

### 分支控制

jinja2 中的 `if` 语句类似 Python 的 `if` 语句，支持单分支、多分支结构，不同的是，条件语句 **不需要冒号** 结尾，而结束
控制语句，必须显式使用 `{% endif %}` 结束。

代码示例：

```python
{% if user.is_admin %}
  <p>管理员用户</p>
{% elif user.is_member %}
  <p>会员用户</p>
{% else %}
  <p>普通用户</p>
{% endif %}
```

### 循环语句

jinjia2 中的 `for` 循环用于迭代 Python 数据类型：**列表、元组、字典**，**不支持** `while` 循环。

语法结构：

```python
{% for item in iterable %}
  <p>{{ item }}</p>  {# 循环体 #}
{% endfor %}         {# 必须显式结束 #}
```

代码示例：

```python
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

@See https://fastapi.tiangolo.com/zh/tutorial/security/

OAuth2 流程：

- 用户通过 `/token` 端点登录获取Token
- 前端在请求头中添加 `Authorization: Bearer <token>`
- 后端通过 `get_current_user` 依赖项验证Token

创建用于 JWT 令牌签名的随机密钥：

```shell
$ openssl rand -hex 32
```

## 安装依赖

安装依赖：`python-jose`，用于生成和校验 access_token。

```shell
$ pip install 'python-jose[cryptography]' types-python-jose
```

> **提示**：`'python-jose[cryptography]'` 是 `pyjwt` 的超集，不仅支持JWT标准（RFC 7519），还完整实现了JOSE标准（包括JWS/JWE/JWK等），其API设计与PyJWT高度兼容，可直接替代PyJWT的所有功能。

## 核心代码

> **`app/core/security.py`**

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError
from pydantic import BaseModel
from datetime import datetime, timezone
from typing import Annotated


# 安全配置常量
# 使用 openssl rand -hex 32 生成的256位(32字节)随机密钥
SECRET_KEY = "39003c5d088944c4db8fe0fa96d65c95936027537d478a7c220f5be2d8944f81"
ALGORITHM = "HS256"  # HMAC + SHA256 签名算法
ACCESS_TOKEN_EXPIRE_HOURS = 15  # 访问令牌有效期


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
        str: Base64编码的JWT字符串
    Note:
        使用UTC时间戳确保跨时区一致性
    """
    timestamp = int(datetime.now(timezone.utc).timestamp())
    payload = TokenPayload(
        sub=str(user_id),
        exp=timestamp + ACCESS_TOKEN_EXPIRE_HOURS,
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
        HTTPException 403: 令牌无效(JWTError)
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
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token 无效",
            headers={"WWW-Authenticate": "Bearer"},
        )


#  OAuth2密码模式Bearer令牌方案
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/user/login",  # 令牌获取端点
    auto_error=False,  # 允许公共接口不传token
)


async def get_current_user(token: str = Depends(oauth2_scheme)):
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
    # 实际项目应从数据库验证用户
    user_id = 1
    return {"access_token": create_access_token(user_id)}


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

- 纯业务逻辑错误 → `Exception`
- HTTP 协议相关错误 → `HTTPException`

## 创建自定义异常类

> **`app/core/exceptions/errors.py`**

```python
from app.core.exceptions.codes import E
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from fastapi import HTTPException, status
from typing import Optional, Dict, Any


class ErrorModel(BaseModel):
    code: int
    msg: str
    data: Optional[Dict[str, Any]] = None


class BizException(HTTPException):
    """业务异常基类"""

    def __init__(
        self,
        error_code: E,
        *,
        status_code: int = status.HTTP_200_OK,
        data: Optional[dict] = None
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

> **`app/core/exceptions/codes`**

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
    PAY_NOT_AMOUNT = (30000, "订单不存在")

    @property
    def code(self):
        """获取错误码"""
        return self.value[0]

    @property
    def msg(self):
        """获取错误码码信息"""
        return self.value[1]

```

> **提示**：你可以根据需要自行按业务模块定义错误。

## 挂载注册异常

```python
from fastapi import FastAPI, HTTPException
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

![](../imgs/middleware_model.jpg)

> 如果你使用了 `yield` 关键字依赖, 依赖中的退出代码将在执行中间后执行。
>
> 如果有任何后台任务(稍后记录), 它们将在执行中间件后运行。

要创建中间件你可以在函数的顶部使用装饰器 `@app.middleware("http")`

中间件参数接收如下参数：

- `request`
- 一个函数 `call_next` 它将接收 `request` 作为参数
  - 这个函数将 `request` 传递给相应的 路径操作。
  - 然后它将返回由相应的路径操作生成的 `response`
- 你可以在返回 `response` 前进一步修改它



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

> **提示**：
>
> 1. 可以 [用 `X-` 前缀 ↪](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers) 添加专有自定义请求头。
> 2. 你也可以使用 `from starlette.requests import Request`，**FastAPI** 为了开发者方便提供了该对象，但其实它直接来自于 Starlette。

# 日志管理

1）安装依赖

```shell
$ pip install loguru
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

CORS 指浏览器中运行的前端拥有与后端通信的 JavaScript 代码，而后端处于与前端不同的「源」的情况。

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
    # 一个允许跨域请求的源列，可以使用 ['*'] 允许任何源
    allow_origins=origins,
    # 指示跨域请求支持 cookies。默认是 False。另外，允许凭证时 allow_origins 不能设定为 ['*']，必须指定源
    allow_credentials=True,
    # 一个允许跨域请求的 HTTP 方法列表
    allow_methods=["*"],
    # 一个允许跨域请求的 HTTP 请求头列表
    allow_headers=["*"],
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
DB_PASSWORD=123456
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

print(db_user, db_password)
```

> **提示**：你可能需要安装 `dotenv` 依赖，执行指令：`pip install dotenv`

## 从 Pydantic 的 `Settings` 中读取

[Pydantic: Settings management ↪](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)

```
your_project/
├── .env                # 根目录
└── app/
    ├── main.py         # 服务入口
    └── core/
        └── configs.py  # 配置类
```

1）安装

```shell
$ pip install pydantic-settings
```

2）新建 **`app/core/config.py`**，内容如下：

```python
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
import atexit


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


def clear_cache():
    """
    清除配置缓存
    用于在需要重新加载配置时调用
    """
    get_settings.cache_clear()


# 注册程序退出时的清理函数
# 确保程序退出时清除配置缓存
atexit.register(clear_cache)

```

2）根目录新建 **`.env`** 文件，填写环境变量

```
DATABASE_URL=postgresql+asyncpg://user:password@host:port/db_name
DEBUG=true
```

3）读取配置

```python
"""
项目路径设置
确保可以正确导入项目模块(如app.api.v1)
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))  # 将项目根目录加入Python路径


"""
模块导入
"""
import uvicorn
from typing import Annotated
from fastapi import FastAPI, Depends
from app.core.configs import Settings, get_settings


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
    return {"settings": settings}


"""
开发服务器启动
"""
if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)
```

# 部署

@See https://fastapi.tiangolo.com/zh/deployment/docker/

