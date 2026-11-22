# FastAPI 学习项目

在项目根目录 `CODES/fastapi_studio` 下启动：

```bash
.venv/bin/python -m app.main
```

也可以在 IDE 中直接运行 `app/main.py`，或执行：

```bash
.venv/bin/python app/main.py
```

启动后访问接口文档：<http://127.0.0.1:8000/docs>。

直接执行脚本时，入口会将项目根目录加入 Python 模块搜索路径，
以支持 `from app...` 导入；Uvicorn 使用 `app.main:app` 加载应用。
