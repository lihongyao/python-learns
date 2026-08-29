# 概述

[SQLAlchemy ↪](https://sqlalchemy.org.cn/) 是 Python SQL 工具包和对象关系映射器，它为应用程序开发者提供了 SQL 的全部力量和灵活性。

它提供了一整套著名的企业级持久化模式，专为高效和高性能的数据库访问而设计，并融入到简洁且 Pythonic 的领域语言中。

# 架构

SQLAlchemy 以其卓越的分层架构在Python ORM领域独树一帜。让我们深入剖析其Core层与ORM层的设计哲学和技术实现。

```mermaid
graph TD
    A[应用程序] --> B[ORM层]
    B --> C[Core层]
    C --> D[数据库驱动]
    C --> E[连接池]
    C --> F[方言系统]
```

分层协作机制：**调用栈分析**

```mermaid
sequenceDiagram
    应用代码->>+ORM层: session.query(User).filter(...)
    ORM层->>+Core层: 转换为select(user_table).where(...)
    Core层->>+数据库驱动: 编译为方言SQL
    数据库驱动-->>-Core层: 返回结果集
    Core层-->>-ORM层: 返回Row对象
    ORM层->>+应用代码: 转换为User实例
```

**Core vs. ORM**

| 对比维度     | Core层                        | ORM层                              |
| :----------- | :---------------------------- | :--------------------------------- |
| **抽象级别** | 接近原生SQL的底层接口         | 面向对象的高级抽象                 |
| **主要用途** | 数据库连接管理、原始SQL操作   | 对象-关系映射（O/R Mapping）       |
| **核心组件** | Engine/Connection/Transaction | Session/Mapper/Relationship        |
| **查询方式** | SQL表达式语言或原生SQL        | 面向对象查询API（如session.query） |
| **性能特点** | 更高执行效率                  | 有对象转换开销                     |
| **灵活性**   | 完全控制SQL细节               | 受限于ORM模型定义                  |
| **事务控制** | 显式控制（begin/commit）      | 通过Session自动管理                |
| **适用场景** | 复杂SQL/批量操作/性能敏感场景 | 常规业务逻辑开发                   |
| **学习曲线** | 需要SQL知识                   | 更符合OOP思维                      |
| **DDL支持**  | 完整支持表创建/修改           | 通过模型类间接支持                 |
| **结果处理** | 返回Row对象或元组             | 返回模型类实例                     |
| **缓存机制** | 无                            | 内置身份映射缓存                   |
| **扩展性**   | 可自定义类型和方言            | 通过混合属性等方式扩展             |

# 基础

## **`relationship`**

### 概述

Relationship 是 SQLAlchemy ORM 的核心功能，用于在 Python 类之间建立数据库表关系的映射。它允许你通过对象属性直接访问相关联的数据，而不需要手动编写 JOIN 查询。

### 为什么需要 Relationship？

- 简化关联查询：无需手动写 JOIN SQL
- 面向对象操作：直接通过属性访问关联对象
- 自动维护关系：自动处理外键更新等操作
- 提高代码可读性：业务逻辑更清晰

### Relationship 核心类型

#### 一对多关系

最常见的关联类型，如"一个用户有多篇文章"：

```python
class User(Base):
    __tablename__ = 'users'
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)
    
    # 一对多关系
    articles = relationship("Article", back_populates="author")

class Article(Base):
    __tablename__ = 'articles'
    id = mapped_column(Integer, primary_key=True)
    title = mapped_column(String)
    user_id = mapped_column(Integer, ForeignKey('users.id'))
    
    # 多对一关系
    author = relationship("User", back_populates="articles")
```

#### 多对一关系

本质上是"一对多"的反向关系，如上例中的 `author` 关系。

#### 一对一关系

如"一个用户对应一个资料档案"：

```python
class User(Base):
    __tablename__ = 'users'
    id = mapped_column(Integer, primary_key=True)
    # ...
    profile = relationship("Profile", back_populates="user", uselist=False)

class Profile(Base):
    __tablename__ = 'profiles'
    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey('users.id'))
    # ...
    user = relationship("User", back_populates="profile")
```

#### 多对多关系

需要中间关联表，如"学生和课程"的关系：

```python
# 中间关联表
student_course = Table(
    'student_course',
    Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id')),
    Column('course_id', Integer, ForeignKey('courses.id'))
)

class Student(Base):
    __tablename__ = 'students'
    id = mapped_column(Integer, primary_key=True)
    # ...
    courses = relationship("Course", secondary=student_course, back_populates="students")

class Course(Base):
    __tablename__ = 'courses'
    id = mapped_column(Integer, primary_key=True)
    # ...
    students = relationship("Student", secondary=student_course, back_populates="courses")
```

### Relationship 参数详解

1）**基本参数**

| 参数             | 说明                          | 示例                        |
| :--------------- | :---------------------------- | --------------------------- |
| `argument`       | 关联的目标模型类              | `relationship("User")`      |
| `back_populates` | 双向关系的反向属性名          | `back_populates="articles"` |
| `backref`        | 自动创建反向引用              | `backref="author"`          |
| `uselist`        | 是否返回列表(False表示一对一) | `uselist=False`             |
| `lazy`           | 加载策略                      | `lazy="select"`             |

2）**加载策略（lazy 参数）**

| 策略       | 说明                     | 适用场景               |
| :--------- | :----------------------- | :--------------------- |
| `select`   | 首次访问时单独查询(默认) | 不确定是否需要关联数据 |
| `joined`   | 使用JOIN立即加载         | 简单关系且确定需要     |
| `selectin` | 使用IN查询预加载         | 一对多/多对多优化      |
| `subquery` | 使用子查询加载(已过时)   | 不推荐                 |
| `dynamic`  | 返回可过滤的查询对象     | 超大结果集分页         |

3）**级联操作（cascade参数）**

```python
cascade="all, delete-orphan"
```

常用选项：

- `save-update`：自动保存关联对象
- `delete`：删除父对象时级联删除
- `delete-orphan`：删除不再关联的子对象
- `all`：包含所有操作(除delete-orphan)
- `all, delete-orphan`：包含所有操作

# 准备

接下来，我们将结合一个案例（学生管理系统，缩写 sms）介绍 SQLAlchemy 的基本用法，数据库使用 [Postgresql ↪](https://www.postgresql.org/)，图形化工具使用 [pgAdmin ↪](https://www.pgadmin.org/)。

> **提示**：本文主要讨论 [SQLAlchemy ORM  ↪](https://docs.sqlalchemy.org.cn/en/20/orm/index.html) 的基本用法，如果你对 Core 语法感兴趣，建议扩展阅读 [SQLAlchemy Core ↪](https://docs.sqlalchemy.org.cn/en/20/core/index.html)。

## 创建虚拟环境

```shell
$ conda create -n sms python=3.13.4 -y 
$ conda activate sms
```

## 创建项目目录

```shell
cd Desktop/ && \
mkdir sms && cd sms && \
mkdir -p app/{core,models,schemas,api/v1,service} && \
touch app/__init__.py && \
touch app/core/{__init__.py,configs.py,database.py} && \
touch app/models/{__init__.py,students.py} && \
touch app/schemas/{__init__.py,students.py} && \
touch app/api/{__init__.py,v1/__init__.py,v1/students.py} && \
touch app/services/{__init__.py,students.py} && \
touch .env requirements.txt main.py
```

```shell
$ tree -L 3
```

```
.
├── app
│   ├── __init__.py
│   ├── api
│   │   ├── __init__.py
│   │   └── v1
│   ├── core
│   │   ├── __init__.py
│   │   ├── configs.py
│   │   └── database.py
│   ├── models
│   │   ├── __init__.py
│   │   └── students.py
│   ├── schemas
│   │   ├── __init__.py
│   │   └── students.py
│   └── services
│       ├── __init__.py
│       └── students.py
├── main.py
└── requirements.txt
```

## 安装相关依赖

```shell
# 数据库相关
$ pip install SQLAlchemy psycopg2 types-psycopg2
# FastAPI相关
$ pip install fastapi "uvicorn[standard]"
# 日志
$ pip install loguru
```

> **提示**：SQLAlchemy 异步链接，需安装 `asyncpg` 依赖，如果是同步链，则需要安装 `psycopg2` 依赖。

## 数据库连接池

> **`app/core/database.py`**

```python
from datetime import datetime
from typing import AsyncGenerator

from fastapi import HTTPException
from loguru import logger
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# 格式示例：postgresql+asyncpg://user:pass@host:port/dbname
DATABASE_URL = f"postgresql+asyncpg://root:lee.123@localhost:5432/sms"


class DatabaseError(Exception):
    """所有数据库相关异常的基类"""

    pass


class Base(DeclarativeBase):
    """
    SQLAlchemy 声明式基类
    所有数据模型应继承此类，用于定义数据库表结构

    特性：
    - 自动表名生成（通过__tablename__）
    - 支持ORM映射和类型注解
    - 内置时间戳字段（UTC时区）
    """

    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="创建时间（UTC时区）",
    )

    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="自动更新时间（UTC时区）",
    )


# 创建异步引擎
async_engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,  # 连接池常驻连接数（建议值：5-20，需根据实际并发量调整）
    max_overflow=30,  # 允许临时超出pool_size的连接数（应对突发流量，建议不超过pool_size的1.5倍）
    pool_recycle=3600,  # 连接自动回收时间（秒），避免数据库因空闲超时主动断开（需匹配数据库的wait_timeout）
    pool_pre_ping=True,  # 执行前检查连接活性（生产环境建议开启，防止数据库重启/网络波动导致连接失效）
    pool_use_lifo=True,  # 使用LIFO策略提高热点连接复用率（降低新建连接开销）
    connect_args={
        "command_timeout": 60,  # 单条SQL执行超时（秒），需长于复杂查询耗时但短于数据库连接超时
        "server_settings": {
            "jit": "off"
        },  # PostgreSQL专用优化（禁用JIT编译提升简单查询性能）
    },
    future=True,  # 启用SQLAlchemy 2.0兼容模式（必选项，支持异步API和现代特性）
    echo=True,  # 开启SQL日志（调试时启用，生产环境必须关闭以避免敏感信息泄露和性能损耗）
)

# 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,  # 绑定已配置的异步引擎
    autoflush=False,  # 禁用自动flush，适合批量操作和高并发场景
    expire_on_commit=False,  # 提交后对象保持可用，避免N+1查询问题
    class_=AsyncSession,  # 显式声明异步会话类（增强可读性）
    future=True,  # 启用SQLAlchemy 2.0特性（如改进的异步API）
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    生成数据库会话的异步上下文管理器

    使用方式：
    - 在路由中声明参数: `db: AsyncSession = Depends(get_db)`

    注意：必须通过FastAPI依赖注入使用
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            logger.debug("Session yielded to route")
            await session.commit()
            logger.debug("Transaction committed")
        except SQLAlchemyError as e:
            await session.rollback()
            raise HTTPException(500, "数据库操作失败") from e
        finally:
            await session.close()


async def init_db():
    """
    异步初始化数据库表结构（自动执行 DDL）

    特性：
    - 自动创建所有继承自 `Base` 的模型表
    - 内置事务管理（通过 `async with` 上下文）
    - 自动处理连接池获取/释放

    异常：
        DatabaseError: 当以下情况发生时抛出：
        - 数据库连接失败
        - 表结构冲突（如重复建表）
        - SQL 语法错误

    示例：
        >>> await init_db()  # 通常在应用启动时调用一次
    """
    logger.info("DB initialization started")
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.success("Tables created")
    except Exception as e:
        logger.critical(f"DB init failed: {e}")
        raise DatabaseError("Database initialization failed") from e


async def close_db():
    """
    安全关闭所有数据库连接并释放连接池资源

    设计原则：
    - 幂等操作：重复调用不会报错
    - 自动回收：强制关闭所有连接（包括未归还的连接）
    - 非阻塞：异步等待所有连接关闭完成

    最佳实践：
    - 应在应用退出前调用（如 FastAPI 的 lifespan 事件）
    - 生产环境建议配合信号处理器使用（如 SIGTERM）

    异常：
        DatabaseError: 当连接池关闭过程中发生不可恢复错误时抛出
    """
    logger.info("Closing DB connections")
    try:
        await async_engine.dispose()
    except Exception as e:
        logger.error(f"DB shutdown error: {e}")
        raise DatabaseError("Connection cleanup failed") from e
    logger.info("DB connections closed")
```

## 定义模型（表结构）





> **`app/models/user.py`**

```python
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.sql import func
from app.core.database import Base


class User(AsyncAttrs, Base):
    """
    用户数据模型
    继承 AsyncAttrs 支持异步属性访问
    继承 Base 作为声明式模型基类
    """

    __table_args__ = {
        "comment": "系统用户表",  # 为数据库表添加注释
        "extend_existing": True,  # 允许表定义扩展
    }

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        comment="用户ID",
    )
    phone = Column(
        String(11),
        unique=True,
        index=True,
        nullable=False,
        comment="用户名(手机号)",
    )
    password = Column(
        String(200),
        nullable=False,
        comment="加密后的密码",
    )
    reated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        comment="创建时间",
    )

```

2）配置 schemas

> **`app/schemas/user.py`**



json 序列化

```shell
pip install sqlalchemy-serializer
```

```shell
# 1. 安装SQLAlchemy
$ pip install SQLAlchemy asyncpg

$ pip install greenlet
pip install greenlet asyncpg sqlalchemy fastapi uvicorn
密码哈西
pip install bcrypt  passlib
```

# 规范

| 查询类型   | 推荐命名模式            | 示例                         |
| ---------- | ----------------------- | ---------------------------- |
| 存在性检查 | `stmt_check_[字段]`     | `stmt_check_email`           |
| 数据获取   | `stmt_get_[业务实体]`   | `stmt_get_order_details`     |
| 关联查询   | `stmt_find_[关联关系]`  | `stmt_find_user_roles`       |
| 插入操作   | `stmt_insert_[实体]`    | `stmt_insert_product`        |
| 更新操作   | `stmt_update_[条件]`    | `stmt_update_user_status`    |
| 删除操作   | `stmt_delete_[条件]`    | `stmt_delete_inactive_users` |
| 复杂查询   | `stmt_build_[业务场景]` | `stmt_build_report_query`    |

# 连接

1）安装依赖

```shell
$ pip install SQLAlchemy asyncpg greenlet
```

2）定义数据库连接池

# RBAC

```mermaid
graph TD
    A[一级菜单] --> B[二级菜单1]
    A --> C[二级菜单2]
    B --> D[按钮1]
    B --> E[按钮2]
    C --> F[按钮3]
    C --> G[按钮4]
```

RBAC（**R**ole-**B**ased **A**ccess **C**ontrol，基于角色的访问控制）是一套用来划分系统功能、资源和数据访问权限的思想（方法论），它通过 **角色** 作为中间层，将 **用户** 和 **权限** 解耦，实现灵活、高效的权限管理。

核心思想：

- 用户不直接拥有权限，而是通过角色间接获得权限。
- 角色是权限的集合，用户是角色的集合。
- 通过分配角色给用户，实现权限控制。

简单来说，就是用户与角色进行绑定，角色与权限进行绑定，这样就解决了每创建一个用户不再是去创建一个新的权限表，而是将用户与角色进行绑定，减少了代码与思维逻辑上的冗余；

简单来说，RBAC就是将系统中的各种元素（如功能模块、数据、资源）进行访问权限设计。具体怎么设计呢？这要根据实际的业务场景和业务流程来定。通常的做法是：

1. 定义几类角色。每类角色有什么样的功能权限和数据权限（增、删、改、查、分享）。比如，超级管理员拥有最大权限。角色1只有功能模块1和功能模块2的全部权限。角色2只有功能模块1的数据查询权限，等等。
2. 将用户绑定到角色上。
3. 通常还支持自定义角色。

角色和权限、用户和角色，都是多对多的关系。

## 核心概念

| 概念                  | 定义描述                  | 典型实例                   |
| --------------------- | ------------------------- | -------------------------- |
| **用户 (User)**       | 系统使用者实体            | 张三(员工)、李四(管理员)   |
| **角色 (Role)**       | 权限的逻辑分组单元        | admin, editor, viewer      |
| **权限 (Permission)** | 对资源的操作许可          | read:article, delete:order |
| **资源 (Resource)**   | 被保护的系统数据/功能对象 | article, order, user       |

## 基本模型

RBAC 通常分为：

1. RBAC0（基础模型）
   - 用户 → 角色 → 权限 的三级结构
   - 用户通过角色获得权限，权限直接绑定到角色
   - 示例：
     - 角色 **admin** 拥有 `create:user`、`delete:user` 权限
     - 用户 **张三** 被分配 **admin** 角色，因此拥有 `create:user` 和 `delete:user` 权限
2. RBAC1（角色继承）
   - 角色可以 **继承** 其他角色的权限（类似面向对象的继承）
   - 示例：
     - 角色 **senior_editor** 继承 `editor` 的所有权限，并额外拥有 `publish:article` 权限
     - 用户 **李四** 被分配 `senior_editor` 角色，因此拥有 `editor` 的所有权限 + `publish:article`
3. RBAC2（约束）
   - 增加 **约束条件**，如：
     - 互斥角色：一个用户不能同时拥有 **审核员** 和 **申请人 角色**（避免利益冲突）
     - 基数约束：一个用户最多只能拥有 3 个角色
     - 先决条件角色：必须先拥有 **初级编辑** 才能升级为 **高级编辑**
4. RBAC3（混合模型）
   - 结合 RBAC1（角色继承） 和 RBAC2（约束），适用于复杂系统

企业级系统一般使用 RBAC0 + RBAC1。

## RBAC 权限管理优势

| 优势             | 说明                                                   |
| ---------------- | ------------------------------------------------------ |
| 解耦用户和权限   | 用户不直接绑定权限，而是通过角色间接获得权限，便于管理 |
| 灵活的角色分配   | 可以动态调整角色权限，无需修改用户权限                 |
| 支持角色继承     | 减少重复配置，提高管理效率                             |
| 便于审计         | 权限变更只需调整角色，便于追踪权限分配情况             |
| 适用于大规模系统 | 可以轻松扩展到成千上万的用户和权限                     |

## RBAC 的实现方式

### 数据库设计

### RBAC 数据库表结构说明

| 表名             | 字段                         | 说明                          |
| ---------------- | ---------------------------- | ----------------------------- |
| users            | id, name                     | 用户表（存储用户基本信息）    |
| roles            | id,name                      | 角色表（定义系统角色）        |
| permissions      | id,parent_id,code,name,level | 权限表（记录具体操作权限）    |
| user_roles       | user_id, role_id             | 用户-角色关联表（多对多关系） |
| role_permissions | role_id, permission_id       | 角色-权限关联表（多对多关系） |

```python
from turtle import back
from typing import List

from sqlalchemy import VARCHAR, CheckConstraint, ForeignKey, Index, Integer, PrimaryKeyConstraint, UniqueConstraint
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

#  RBAC 模型


class Permission(AsyncAttrs, Base):
    """权限模型"""

    __tablename__ = "permissions"
    __mapper_args__ = {"eager_defaults": True}
    __table_args__ = (
        {"comment": "权限表"},
        CheckConstraint("level >= 0", name="check_level_positive"),
        CheckConstraint("NOT (level = 0 AND parent_id IS NOT NULL)", name="check_root_node"),  # 确保根节点的 parent_id 为NULL
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="权限ID")
    parent_id: Mapped[int] = mapped_column(ForeignKey("permissions.id", ondelete="CASCADE"), index=True, nullable=True, comment="父权限ID", server_default=None)
    code: Mapped[str] = mapped_column(VARCHAR(50), unique=True, nullable=False, comment="权限代码")
    name: Mapped[str] = mapped_column(VARCHAR(50), unique=True, nullable=False, comment="权限名称")
    level: Mapped[int] = mapped_column(Integer, nullable=False, comment="权限层级（0为根节点）", server_default="0")

    children: Mapped[List["Permission"]] = relationship(back_populates="parent", lazy="selectin", cascade="all, delete-orphan")
    parent: Mapped["Permission"] = relationship(back_populates="children", remote_side=[id])  # 自关联关键配置
    roles: Mapped[List["Role"]] = relationship(secondary="role_permissions", back_populates="role_permissions")


class Role(AsyncAttrs, Base):
    """角色模型"""

    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(50), unique=True)

    users: Mapped[List["User"]] = relationship(secondary="user_roles", back_populates="roles")
    permissions: Mapped[List["Permission"]] = relationship(secondary="role_permissions", back_populates="roles", cascade="all, delete-orphan")

    role_users: Mapped[List["UserRole"]] = relationship(back_populates="role")
    role_permissions: Mapped[List["RolePermission"]] = relationship(back_populates="role")


class UserRole(AsyncAttrs, Base):
    """中间表：用户角色模型"""

    __tablename__ = "user_roles"
    __table_args__ = {"comment": "用户角色表"}

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), comment="关联用户ID", primary_key=True, index=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), comment="关联角色ID", primary_key=True, index=True)

    user: Mapped["User"] = relationship(back_populates="user_roles")
    role: Mapped["Role"] = relationship(back_populates="role_users")


class RolePermission(AsyncAttrs, Base):
    """中间表：角色权限模型"""

    __tablename__ = "role_permissions"
    __table_args__ = {"comment": "角色权限表"}
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), comment="关联角色ID", primary_key=True, index=True)
    permission_id: Mapped[int] = mapped_column(ForeignKey("permissions.id"), comment="关联权限ID", primary_key=True, index=True)

    role: Mapped["Role"] = relationship(back_populates="role_permissions")
    permission: Mapped["Permission"] = relationship(back_populates="permission_roles")


class User(AsyncAttrs, Base):
    """用户模型"""

    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(50), unique=True)

    roles: Mapped[List["Role"]] = relationship(secondary="user_roles", back_populates="users")
    user_roles: Mapped[List["UserRole"]] = relationship(back_populates="user")

    def has_permission(self, permission_code: str) -> bool:
        return any(perm.code == permission_code for role in self.roles for perm in role.permissions)

```



# 总结

## 插入

```python
from sqlalchemy import insert
stmt = insert(<table_name>).values(...)
```

