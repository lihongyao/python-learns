import os
from dotenv import load_dotenv
from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# 加载.env文件中的环境变量
load_dotenv()


# 创建SQLAlchemy的声明式基类
# 所有数据模型类都将继承这个Base类
class Base(DeclarativeBase):
    pass


# 从环境变量中获取数据库连接配置
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

# 构建PostgreSQL异步连接字符串
# 格式: postgresql+asyncpg://用户名:密码@主机:端口/数据库名
db_url = f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# 引擎配置
engine = create_async_engine(
    db_url,
    pool_size=5,  # 设置连接池大小
    max_overflow=5,  # 设置最大重试次数
    pool_recycle=3600,  # 连接回收时间(秒)
    pool_pre_ping=True,  # 连接健康检查
    pool_use_lifo=True,  # 使用LIFO策略提高连接复用率
    future=True,  # 启用2.0模式
    connect_args={
        "command_timeout": 30,  # 添加命令超时
    },
)

# 会话工厂
AsyncSessionLocal = async_sessionmaker(
    bind=engine,  # 绑定到上面创建的引擎
    autoflush=False,  # 关闭自动刷新提高批量操作性能
    expire_on_commit=False,  # 提交后不使对象过期
    class_=AsyncSession,  # 显式声明会话类
    future=True,  # 启用SQLAlchemy 2.0兼容模式
)


# 依赖注入
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()  # 成功时提交
        except Exception as e:
            logger.error(f"Database error: {str(e)}")
            await session.rollback()  # 异常时回滚
            raise  # 必须重新抛出异常
        finally:
            await session.close()  # 确保连接关闭


# 生命周期管理
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Creating database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield
    logger.info("Disposing database engine...")
    await engine.dispose()
