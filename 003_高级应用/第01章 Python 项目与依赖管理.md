# 概述

一个 Python 项目通常需要解决以下问题：

1. 记录项目依赖
2. 隔离项目环境
3. 固定依赖版本
4. 运行测试和开发命令
5. 构建和发布 Python 包

[Poetry ↪](https://python-poetry.org/) 和 [uv ↪](https://docs.astral.sh/uv/) 都可以完成依赖管理，但它们的定位不止是“安装 Python 包”。更准确地说，它们都是 Python 项目管理工具。

Poetry 更强调项目依赖、打包和发布；uv 除了项目依赖，还可以安装和管理 Python 版本，以及运行隔离的命令行工具。

两者都使用 `pyproject.toml` 描述项目，都支持虚拟环境和锁文件。一个项目建议选择其中一个作为依赖管理的主要工具，不要交替修改依赖。

> 本章示例基于 [Python 3.14.7 ↪](https://www.python.org/downloads/release/python-3147/)。命令以 macOS 和 zsh 为例，Windows 或 Linux 只需要替换安装方式。

参考：

1. [Poetry 官方文档 ↪](https://python-poetry.org/docs/)
2. [uv 官方文档 ↪](https://docs.astral.sh/uv/)

# 共同概念

## `pyproject.toml`

`pyproject.toml` 是 Python 项目的配置文件，通常用于记录：

- 项目名称和版本
- 支持的 Python 版本
- 运行依赖和开发依赖
- 构建工具配置

Poetry 2.x 推荐使用标准的 `[project]` 区域记录项目元数据和主要依赖；Poetry 专属配置仍然可以放在 `[tool.poetry]` 中。uv 也以标准的 `pyproject.toml` 为项目配置文件。

## 虚拟环境

不同项目可能依赖同一个包的不同版本，因此通常需要为每个项目创建独立的虚拟环境。

- Poetry 默认将虚拟环境放在统一的缓存目录中，也可以配置为项目目录下的 `.venv`。
- uv 默认将项目虚拟环境放在项目目录下的 `.venv`。

使用项目工具执行命令时，优先使用 `poetry run` 或 `uv run`，不必手动激活虚拟环境。

## 锁文件

锁文件会记录依赖树中的具体版本，常用于保证不同机器和不同时间安装出的环境尽量一致。

- Poetry 使用 `poetry.lock`
- uv 使用 `uv.lock`

锁文件通常应该提交到 Git。两个工具的锁文件格式不同，不能互相替代。

## 常用操作

| 操作           | Poetry                          | uv                         |
| :------------- | :------------------------------ | :------------------------- |
| 添加依赖       | `poetry add requests`            | `uv add requests`           |
| 删除依赖       | `poetry remove requests`         | `uv remove requests`        |
| 安装或同步依赖 | `poetry install` / `poetry sync` | `uv sync`                   |
| 运行项目命令   | `poetry run python main.py`      | `uv run python main.py`     |
| 查看依赖       | `poetry show`                    | `uv tree`                   |
| 锁定依赖       | `poetry lock`                    | `uv lock`                   |

# Poetry

Poetry 是一个集依赖管理、虚拟环境、打包和发布于一体的 Python 项目工具。它适合库开发，也适合需要明确项目元数据和发布流程的应用项目。

## 安装

Poetry 官方提供了多种安装方式，详见[安装文档 ↪](https://python-poetry.org/docs/#installation)。macOS 可以使用 Homebrew：

```shell
$ brew install poetry
$ poetry --version
```

升级：

```shell
$ brew upgrade poetry
```

> 不建议把 Poetry 安装到正在管理的项目虚拟环境中。Poetry 应该作为独立的命令行工具安装。

## 配置（可选）

查看当前配置：

```shell
$ poetry config --list
```

Poetry 默认会自动创建虚拟环境。如果希望虚拟环境位于当前项目的 `.venv` 目录，可以配置：

```shell
$ poetry config virtualenvs.create true
$ poetry config virtualenvs.in-project true
```

查看当前项目使用的虚拟环境：

```shell
$ poetry env info
```

> `virtualenvs.create true` 表示启用自动创建虚拟环境，不是关闭创建。

## 创建项目

### 创建新项目

`poetry new` 适合创建库项目，会生成基础的源码目录和测试目录：

```shell
$ poetry new my_project
$ cd my_project
```

生成的目录结构如下：

```text
my_project/
├── pyproject.toml
├── README.md
├── src/
│   └── my_project/
│       └── __init__.py
└── tests/
    └── __init__.py
```

### 初始化已有项目

如果项目目录已经存在，可以使用 `poetry init` 创建 `pyproject.toml`：

```shell
$ mkdir my_project && cd my_project
$ poetry init --no-interaction --python "^3.14"
```

也可以省略参数，按交互提示完成初始化：

```shell
$ poetry init
```

> `--python "^3.14"` 表示项目支持 Python 3.14 及后续兼容版本，并不负责安装 Python。`uv` 可以额外承担 Python 版本安装和管理工作。

## 虚拟环境管理

Poetry 会根据 `pyproject.toml` 中的 Python 版本要求创建虚拟环境。

查看环境信息：

```shell
$ poetry env info
```

列出当前项目关联的环境：

```shell
$ poetry env list
```

指定 Python 解释器：

```shell
$ poetry env use python3.14
```

也可以填写 Python 解释器的完整路径：

```shell
$ poetry env use /path/to/python3.14
```

执行项目命令：

```shell
$ poetry run python --version
$ poetry run pytest
```

## 依赖管理

添加运行依赖：

```shell
$ poetry add requests
```

添加指定版本的依赖：

```shell
$ poetry add "requests>=2.32,<3"
```

删除依赖：

```shell
$ poetry remove requests
```

查看项目依赖：

```shell
$ poetry show
```

## 依赖分组

运行依赖和开发工具通常应该分开记录。Poetry 2.x 使用 `--group` 添加开发依赖：

```shell
$ poetry add pytest --group dev
$ poetry add ruff --group lint
```

安装项目全部依赖（包括默认开发组）：

```shell
$ poetry install
```

只安装运行依赖：

```shell
$ poetry install --only main
```

只安装指定分组：

```shell
$ poetry install --only lint
```

## 安装、锁定和更新

当项目中已经有 `poetry.lock` 时，使用 `poetry install` 按锁文件安装依赖：

```shell
$ poetry install
```

同步环境，使环境中的依赖与锁文件保持一致，并删除多余的包：

```shell
$ poetry sync
```

重新生成锁文件：

```shell
$ poetry lock
```

更新所有依赖：

```shell
$ poetry update
```

只更新某个依赖：

```shell
$ poetry update requests
```

检查项目配置：

```shell
$ poetry check
```

## 构建和发布

Poetry 可以将项目构建为源码包和 wheel 包：

```shell
$ poetry build
```

发布到 PyPI：

```shell
$ poetry publish
```

> 发布前需要配置 PyPI 凭据。学习阶段通常只需要掌握 `poetry build`，不要直接向正式仓库发布测试包。

# uv

uv 是由 Astral 开发的 Python 工具链，覆盖项目依赖、虚拟环境、Python 版本和命令行工具。它的项目命令以 `pyproject.toml` 和 `uv.lock` 为中心。

## 安装（macOS）

macOS 推荐使用 Homebrew 安装：

```shell
$ brew install uv
$ uv --version
```

升级：

```shell
$ brew upgrade uv
```

也可以使用 uv 官方安装脚本：

```shell
$ curl -LsSf https://astral.sh/uv/install.sh | sh
```

更多安装方式参考 [`uv` 官方安装文档 ↪](https://docs.astral.sh/uv/getting-started/installation/)。

## 创建项目

创建并初始化项目：

```shell
$ mkdir -p code/uv_demo
$ cd code/uv_demo
$ uv init --bare
```

安装并固定项目使用的 Python 版本：

```shell
$ uv python install 3.14.7
$ uv python pin 3.14.7
```

查看 uv 管理的 Python 版本：

```shell
$ uv python list
```

> 如果系统中已经安装了符合要求的 Python，可以不执行 `uv python install`。`uv python pin` 只负责记录当前项目的版本要求。

## 依赖管理

添加运行依赖：

```shell
$ uv add requests
```

添加指定版本的依赖：

```shell
$ uv add "requests>=2.32,<3"
```

删除依赖：

```shell
$ uv remove requests
```

添加开发依赖：

```shell
$ uv add --dev pytest
```

添加其他依赖分组：

```shell
$ uv add --group lint ruff
```

查看依赖树：

```shell
$ uv tree
```

## 锁定和同步

`uv add` 会自动更新 `pyproject.toml` 和 `uv.lock`。也可以手动锁定依赖：

```shell
$ uv lock
```

根据项目配置创建或更新 `.venv`：

```shell
$ uv sync
```

在 CI 或部署环境中只使用已有锁文件，不重新解析依赖：

```shell
$ uv sync --locked
```

## 运行项目命令

项目虚拟环境默认位于 `.venv`，但不需要手动激活，直接使用 `uv run`：

```shell
$ uv run python --version
$ uv run pytest
```

`uv run` 会在执行命令前检查项目环境是否需要同步：

```shell
$ uv run python main.py
```

## FastAPI 示例

安装 FastAPI 及其常用开发依赖：

```shell
$ uv add "fastapi[standard]"
```

启动开发服务器：

```shell
$ uv run fastapi dev main.py
```

生产环境可以使用：

```shell
$ uv run fastapi run main.py
```

## 使用命令行工具

`uvx` 可以在临时隔离环境中运行 Python 命令行工具，例如：

```shell
$ uvx ruff check .
```

如果希望长期使用某个工具，可以安装到 uv 的工具环境中：

```shell
$ uv tool install ruff
$ ruff --version
```

升级已安装的工具：

```shell
$ uv tool upgrade ruff
```

## 构建和发布

uv 也支持构建和发布 Python 包：

```shell
$ uv build
$ uv publish
```

## `uv pip` 的适用场景

uv 提供了兼容 pip 的命令：

```shell
$ uv pip install requests
```

这类命令适合直接管理一个虚拟环境。对于已经使用 `pyproject.toml` 的项目，建议优先使用 `uv add`，这样依赖会被记录到项目配置和锁文件中。

# Poetry 与 uv 的区别

| 对比项           | Poetry                         | uv                                  |
| :--------------- | :----------------------------- | :---------------------------------- |
| 主要定位         | 依赖管理、打包和发布             | 项目、依赖、Python 和工具链管理       |
| 项目配置         | `pyproject.toml`                | `pyproject.toml`                    |
| 锁文件           | `poetry.lock`                   | `uv.lock`                           |
| 虚拟环境         | 自动创建，可配置存储位置         | 默认使用项目内 `.venv`               |
| Python 版本      | 选择已有解释器                   | 可以安装、列出和固定 Python 版本       |
| 运行项目命令     | `poetry run`                    | `uv run`                            |
| 开发依赖         | `poetry add --group dev`        | `uv add --dev`                      |
| 命令行工具       | 主要通过项目环境或插件扩展        | `uvx` 和 `uv tool` 提供独立工具环境    |
| 构建和发布       | `poetry build` / `poetry publish` | `uv build` / `uv publish`            |

两者都能完成常见的依赖管理任务，差异主要在于工具侧重点：Poetry 的项目打包和发布体验较集中；uv 更像一个覆盖 Python 开发流程的工具链。

# 如何选择

## 新项目

对于新的 FastAPI 服务、脚本项目或一般应用项目，可以优先选择 uv：

- 安装简单
- 可以管理 Python 版本
- 项目命令统一使用 `uv run`
- 依赖和锁文件管理清晰

## 已有 Poetry 项目

如果项目已经使用 Poetry，并且 `pyproject.toml`、`poetry.lock` 和发布流程都运行正常，没有必要为了追求新工具立即迁移。

工具迁移应该有明确原因，例如统一团队工具链、需要 uv 的 Python 版本管理，或者希望使用 uv 的运行和工具隔离功能。

## 不要混用依赖来源

同一个项目中可以同时安装 Poetry 和 uv，但建议只选一个工具修改项目依赖：

- Poetry 项目使用 `poetry add`、`poetry install` 和 `poetry.lock`
- uv 项目使用 `uv add`、`uv sync` 和 `uv.lock`

不要在同一个项目中一部分依赖由 Poetry 管理，另一部分依赖通过 `uv pip install` 临时安装，否则容易出现配置文件、锁文件和实际环境不一致。

> 本仓库的 FastAPI 章节使用 uv；本章用于集中记录 Poetry 与 uv 的项目管理方式。
