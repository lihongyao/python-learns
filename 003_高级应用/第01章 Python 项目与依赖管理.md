# 概述

项目管理的核心是：**声明依赖、隔离环境、锁定版本、统一运行方式**。需要分发项目时，再增加构建和发布流程。

> 本章按 **2026 年 11 月**的工具能力整理，示例使用 **Python 3.15.2**。命令以 macOS 为例；除安装和环境激活方式外，项目命令通常跨平台通用。

## 如何选择

| 场景 | 本章建议 |
| --- | --- |
| 新的一般应用、Web 服务、命令行项目 | 优先考虑 **uv**，统一管理 Python、依赖、环境和工具 |
| 已有 Poetry 项目 | 继续使用 **Poetry**，根据团队需求决定是否迁移 |
| 学习底层机制、维护简单或已有 pip 流程 | 掌握 **`venv + pip`**，按项目需要增加锁定工具 |
| 单文件脚本 | 可用 uv 的脚本依赖元数据，无须创建完整项目 |
| 涉及大量非 Python 依赖的科学计算环境 | 评估 **Conda / Pixi**，例如需要一起管理原生库和外部程序 |

这是按场景给出的实践建议。团队已有稳定流程时，优先保持一致；同一项目选择一个主要依赖管理工具和对应锁文件。

# 共同概念

## 项目文件各自负责什么

| 文件或目录 | 作用 | 是否提交 Git |
| --- | --- | --- |
| `pyproject.toml` | 项目元数据、依赖声明、构建和工具配置 | 是 |
| `.python-version` | uv 等工具选择本地 Python 解释器时使用的版本请求 | 通常提交 |
| `uv.lock` / `poetry.lock` | 解析后的直接依赖与传递依赖版本、来源等信息 | 是 |
| `.venv/` | 当前机器上的项目虚拟环境 | 否 |
| `requirements.txt` | pip 等工具读取的安装需求列表 | 按项目流程决定 |

**声明、锁定和安装是三件事**：`pyproject.toml` 描述允许安装什么，锁文件记录解析结果，`.venv` 保存当前实际安装的内容。

- 直接依赖：项目主动使用的包，应显式声明。
- 传递依赖：直接依赖所依赖的包，由解析器一起处理。
- 锁文件应由工具生成，不要手工维护。
- 跨平台锁文件可以包含多个条件分支；不同系统不一定安装完全相同的包。

## `pyproject.toml`

新项目优先使用标准的 `[project]` 和 `[dependency-groups]`；工具专属配置放在 `[tool.xxx]`。

下面是配置片段，构建配置由项目模板生成：

```toml
[project]
name = "demo"
version = "0.1.0"
requires-python = ">=3.15"
dependencies = ["requests>=2.32,<3"]

[dependency-groups]
dev = ["pytest"]
lint = ["ruff"]

[project.optional-dependencies]
cli = ["rich"]
```

| 配置 | 含义 |
| --- | --- |
| `[project].dependencies` | 运行依赖，发布包时写入包元数据 |
| `[dependency-groups]` | 测试、检查等本地开发依赖，不随包发布为运行依赖 |
| `[project.optional-dependencies]` | 用户可选功能，即 extras，例如 `demo[cli]` |
| `[build-system]` | 构建后端及构建所需依赖，例如 `uv_build`、Hatchling、`poetry-core` |

依赖组用于开发任务，extras 用于可选功能，两者不要混淆。

## Python 版本与依赖版本

- `requires-python = ">=3.15"`：声明项目兼容 Python 3.15 及以上版本，不负责安装解释器。
- `.python-version` 中的 `3.15.2`：选择本地使用的解释器版本，不会把项目兼容范围改成仅支持 3.15.2。
- `requests>=2.32,<3`：依赖的允许范围；具体安装版本由锁文件确定。
- `==` 精确指定版本，`>=`、`<` 指定边界；`~=1.4.2` 表示 `>=1.4.2,<1.5`。
- 标准依赖字符串不支持 Poetry 的 `^` 语法；在 `[project]` 中使用标准版本约束。

固定解释器、提交锁文件，并在相同平台上验证，才能提高环境的可复现程度。库项目还应测试其声明支持的 Python 版本范围。

## 虚拟环境与 `pip`

虚拟环境隔离 Python 包，不隔离操作系统，也不是容器。通常每个项目使用独立的 `.venv`。

基础流程如下：

```shell
$ python3.15 -m venv .venv
$ source .venv/bin/activate
$ python -m pip install requests
$ python -m pip --version
$ deactivate
```

Windows PowerShell 激活命令为 `.venv\Scripts\Activate.ps1`。使用 `python -m pip` 可以明确 pip 对应的解释器。

`pip freeze` 记录当前环境中的已安装版本，可能包含无关包，**不等于完整的跨平台依赖锁定流程**。已有 `requirements.txt` 的项目可以使用 `python -m pip install -r requirements.txt`。

使用 uv 或 Poetry 时，优先通过 `uv run` / `poetry run` 执行命令，无须手动激活环境；编辑器也应选择该项目的解释器。

# uv

uv 覆盖 Python 版本、项目依赖、虚拟环境、命令行工具，以及构建发布。本章将它作为新项目的主要示例。

## 安装

macOS 可使用 Homebrew：

```shell
$ brew install uv
$ uv --version
```

通过 Homebrew 安装后，用 `brew upgrade uv` 升级。其他系统参考 [uv 官方安装文档 ↪](https://docs.astral.sh/uv/getting-started/installation/)。

## 创建项目与管理 Python

```shell
$ uv python install 3.15.2
$ uv init --app --package --python 3.15.2 demo
$ cd demo
$ uv python pin 3.15.2
$ uv run demo
```

- `uv python install` 安装解释器；已有合适解释器时可以跳过。
- `uv init --python` 选择初始化所用解释器，并据此生成最低 Python 版本要求，创建后应检查 `requires-python`。
- `uv python pin` 将版本请求写入 `.python-version`，不会立即安装解释器或重建环境。
- `uv run` 会按需创建环境、锁定和同步依赖，再运行命令。
- `uv python list` 查看解释器；`uv run python --version` 查看项目实际使用的版本。

常用模板：

| 命令 | 用途 |
| --- | --- |
| `uv init --app --package demo` | 带构建配置、`src` 布局和命令入口的应用 |
| `uv init --lib demo` | 准备供其他项目使用的库 |
| `uv init --no-package demo` | 不安装项目自身的简单应用，直接运行 `main.py` |
| `uv init --bare` | 在已有目录中只生成最小 `pyproject.toml` |

> uv **0.12 起**，默认应用模板也包含构建配置和 `src` 布局；旧教程中直接生成 `main.py` 的行为可通过 `--no-package` 明确指定。

带包结构的应用通常如下，`.venv` 和 `uv.lock` 在后续同步时生成：

```text
demo/
├── pyproject.toml
├── uv.lock
├── .python-version
├── .venv/
├── README.md
├── src/
│   └── demo/
│       └── __init__.py
└── tests/                 # 自行添加测试
```

`[project.scripts]` 中的 `demo = "demo:main"` 表示命令 `demo` 调用 `demo` 模块中的 `main()`，不是执行同名文件。

## 添加、删除和查看依赖

| 操作 | 命令 |
| --- | --- |
| 添加运行依赖 | `uv add requests` |
| 添加版本约束 | `uv add "requests>=2.32,<3"` |
| 删除运行依赖 | `uv remove requests` |
| 添加默认开发组依赖 | `uv add --dev pytest` |
| 添加命名依赖组 | `uv add --group lint ruff` |
| 删除分组依赖 | `uv remove --group lint ruff` |
| 添加可选功能依赖 | `uv add --optional cli rich` |
| 查看依赖树 | `uv tree` |

`uv add` / `uv remove` 默认同时修改项目声明、更新锁文件并同步环境。不要用 `uv pip install` 代替依赖声明。

## 分组与 extras 的安装

| 命令 | 默认配置下的安装范围 |
| --- | --- |
| `uv sync` | 运行依赖和 `dev` 组 |
| `uv sync --group lint` | 在默认范围上增加 `lint` 组 |
| `uv sync --all-groups` | 运行依赖和所有依赖组 |
| `uv sync --only-group lint` | 仅 `lint` 组，不安装项目及其运行依赖 |
| `uv sync --no-default-groups` | 运行依赖，不安装默认依赖组 |
| `uv sync --extra cli` | 在默认范围上启用 `cli` extra |

- 默认只启用 `dev` 开发组；可通过 `[tool.uv].default-groups` 调整。
- extras 默认不安装；`--all-groups` 不等于 `--all-extras`。
- `--no-dev` 只排除 `dev` 组；部署时若要排除所有默认开发组，使用 `--no-default-groups`。
- 各依赖组默认一起解析、锁定，不能把分组当成彼此独立的冲突环境。

## 锁定、同步和更新

| 命令 | 作用 |
| --- | --- |
| `uv lock` | 创建或更新锁文件，不安装依赖 |
| `uv sync` | 按需更新锁文件，再同步环境；默认删除未选中的包 |
| `uv sync --locked` | 要求锁文件存在且与项目声明一致，否则报错；不修改锁文件 |
| `uv sync --frozen` | 直接使用现有锁文件，跳过与项目声明的一致性检查 |
| `uv lock --check` | 检查锁文件是否存在且与项目声明一致 |

CI 通常使用 **`--locked`**，以发现遗漏提交的依赖变更。`--frozen` 不保证锁文件与当前声明一致，也不表示离线安装。

锁文件不会仅因为上游发布新版本就自动过期。主动升级依赖：

```shell
$ uv lock --upgrade-package requests
$ uv sync
```

升级全部依赖可用 `uv lock --upgrade`，仍然受 `pyproject.toml` 中的约束限制。需要跨越上界时，应先调整依赖声明，再锁定、同步并验证。

## 运行命令

```shell
$ uv run python --version
$ uv run pytest
$ uv run --group lint ruff check .
```

对于 `--no-package` 创建的应用，使用 `uv run python main.py`。

- `uv run` 默认按需更新锁文件和补齐环境，但通常不会删除额外安装的包；`uv sync` 默认执行精确同步。
- `uv run --locked ...` 要求锁文件有效；`uv run --no-sync ...` 跳过环境同步，适合已经完成同步的后续步骤。
- FastAPI 等应用依赖同样使用 `uv add` 声明，启动命令详见后续 FastAPI 章节。

## 独立工具与单文件脚本

偶尔使用的命令行工具可放在独立环境中：

```shell
$ uvx ruff check .
$ uv tool install ruff
$ uv tool upgrade ruff
```

`uvx` 是 `uv tool run` 的别名，使用独立、可缓存的工具环境。项目需要固定工具版本时，将工具加入开发组并用 `uv run`；pytest 等需要导入项目的工具也优先使用项目环境。

单文件脚本可以使用 **PEP 723** 内联元数据记录依赖：

```shell
$ uv init --script report.py --python 3.15
$ uv add --script report.py rich
$ uv run report.py
```

uv 为脚本准备独立环境。需要锁定具体版本时，执行 `uv lock --script report.py`，生成 `report.py.lock`，并与脚本一起提交。

## 对接已有 pip 流程

`uv pip` 用于直接操作虚拟环境，不会自动维护项目的依赖声明和 `uv.lock`：

```shell
$ uv venv
$ uv pip install -r requirements.txt
```

需要将已有需求列表导入项目时，使用 `uv add -r requirements.txt`；如果文件来自 `pip freeze`，先整理出项目真正使用的直接依赖。

需要向只接受 `requirements.txt` 的环境交付时，从锁文件导出：

```shell
$ uv export --locked --no-default-groups --no-emit-project --format requirements.txt -o requirements.txt
```

这里导出运行依赖，不包含项目自身；带包结构的项目需要另行安装自身。导出文件应由工具生成，避免和 `pyproject.toml` 分别手工维护。

**PEP 751** 已标准化 `pylock.toml`。uv 支持导出该格式，但项目流程仍使用 `uv.lock`，两者不能直接改名替换。

# Poetry

Poetry 提供依赖管理、虚拟环境、构建和发布。已有 Poetry 项目继续使用原有流程即可。

## 安装与初始化

Poetry 应作为独立工具安装，避免装进它管理的项目环境：

```shell
$ brew install poetry
$ poetry --version
$ poetry new demo
$ cd demo
$ poetry env use python3.15
```

- Homebrew 安装用 `brew upgrade poetry` 升级。
- `poetry new` 默认创建带 `src` 布局的包项目；创建后检查 `pyproject.toml` 中的 Python 兼容范围。
- 已有目录使用 `poetry init`；也可使用 `poetry init --no-interaction --python ">=3.15"`。
- `poetry env use` 选择已有解释器，`poetry env info` 查看环境。
- Poetry 提供实验性的 `poetry python install` 等解释器管理命令。

希望环境放在项目内，可在创建环境前配置 `poetry config virtualenvs.in-project true`。已有缓存环境不会因为修改配置自动迁移。

## 常用命令

| 操作 | 命令 |
| --- | --- |
| 添加运行依赖 | `poetry add requests` |
| 添加版本约束 | `poetry add "requests>=2.32,<3"` |
| 删除依赖 | `poetry remove requests` |
| 添加开发依赖 | `poetry add --group dev pytest` |
| 添加命名依赖组 | `poetry add --group lint ruff` |
| 查看依赖树 | `poetry show --tree` |
| 按锁文件安装，保留额外包 | `poetry install` |
| 按锁文件同步，移除多余包 | `poetry sync` |
| 仅同步运行依赖 | `poetry sync --only main` |
| 更新锁文件，默认保留已锁版本 | `poetry lock` |
| 更新某个依赖并安装 | `poetry update requests` |
| 更新所有依赖并安装 | `poetry update` |
| 校验配置和锁文件，并要求锁文件存在 | `poetry check --lock` |
| 运行项目命令 | `poetry run pytest` |

- `poetry lock --regenerate` 忽略旧锁文件重新解析；普通 `poetry lock` 不等于升级全部依赖。
- 当前 Poetry 支持标准 `[dependency-groups]`；旧项目中的 `[tool.poetry.group.<组名>.dependencies]` 也可继续使用。
- Poetry 默认安装运行依赖和所有**非可选组**，与 uv 默认只启用 `dev` 开发组不同。
- `--with docs` 启用可选组，`--without lint` 排除分组，`--only lint` 仅选择指定组；extras 用 `--extras`。

## 只管理依赖的应用

Poetry 默认还会安装项目自身。对于不需要打包的应用，可以配置：

```toml
[tool.poetry]
package-mode = false
```

此时只安装依赖，不能构建或发布项目。`poetry install --no-root` 则只是在本次安装时跳过项目自身。

# 构建与发布

## 构建前端与后端

`uv build` / `poetry build` 是构建入口；`[build-system]` 指定实际执行构建的后端及其构建依赖。

- 需要构建包时，配置构建后端，并确认源码、README、许可证等文件齐全。
- uv 的 `--package` / `--lib` 模板、Poetry 的 `new` 模板会生成相应配置。
- `src` 布局将源码与项目根目录分开，开发时通常应先安装项目自身。uv 默认以可编辑方式安装带构建配置的项目。
- 依赖锁文件用于开发和部署；发布库时，使用者根据包元数据解析依赖，不会自动沿用仓库中的锁文件。

## 常用命令

| 操作 | uv | Poetry |
| --- | --- | --- |
| 构建 wheel 和源码分发包 | `uv build` | `poetry build` |
| 上传已有构建产物 | `uv publish` | `poetry publish` |

构建产物通常位于 `dist/`。发布需要配置目标仓库和凭据；团队发布可在支持时采用 PyPI Trusted Publishing，学习时可使用 TestPyPI 验证。

# Poetry 与 uv 的区别

| 对比项 | uv | Poetry |
| --- | --- | --- |
| 项目配置与锁文件 | `pyproject.toml` + `uv.lock` | `pyproject.toml` + `poetry.lock` |
| Python 管理 | 安装、发现、固定解释器版本 | 选择解释器，也提供实验性安装管理命令 |
| 默认环境位置 | 项目内 `.venv` | 默认缓存目录，可配置项目内 `.venv` |
| 默认开发组 | `dev`，可配置 | 所有非可选组 |
| 精确同步环境 | `uv sync` | `poetry sync` |
| 独立工具运行 | `uvx` / `uv tool` | 通常另外使用工具安装器 |
| 构建发布 | 支持，可配合不同构建后端 | 支持，通常配合 `poetry-core` |

迁移工具时，重点检查版本约束、依赖源、分组、extras、构建配置和 CI 命令。锁文件格式不同，不要在同一项目交替使用两个工具修改依赖。

# 团队协作与持续集成

## Git 管理

提交源码、测试、`pyproject.toml`、主要工具的锁文件，以及团队约定的 `.python-version`。忽略可重建的环境和产物：

```gitignore
.venv/
__pycache__/
*.py[cod]
.pytest_cache/
.ruff_cache/
build/
dist/
*.egg-info/
```

不要复制另一台机器的 `.venv`；克隆项目后，按锁文件重新同步。

## CI 基本流程

CI 先安装团队约定版本的工具和 Python，再校验锁文件、同步、执行检查。以下假设项目已配置 `dev` / `lint` 组并编写测试。

uv 项目：

```shell
$ uv sync --locked --group lint
$ uv run --locked --no-sync ruff check .
$ uv run --locked --no-sync pytest
```

Poetry 项目：

```shell
$ poetry check --lock
$ poetry sync
$ poetry run ruff check .
$ poetry run pytest
```

应用部署时可用 `uv sync --locked --no-default-groups` 或 `poetry sync --only main` 排除开发组；项目需要的 extras 应显式启用。后续启动命令也应保持相同分组策略，避免再次引入开发依赖。

依赖升级应同时提交声明和锁文件的变更，并运行测试。同步依赖本身不代表完成测试，也不代表验证了所有平台和 Python 版本。

# 参考

1. [Python 中文教程：虚拟环境和包 ↪](https://docs.python.org/zh-cn/3.15/tutorial/venv.html)
2. [Python 3.15.2 发布页 ↪](https://www.python.org/downloads/release/python-3152/)
3. [Python Packaging：编写 pyproject.toml ↪](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)
4. [uv：创建项目 ↪](https://docs.astral.sh/uv/concepts/projects/init/)、[项目布局与锁文件 ↪](https://docs.astral.sh/uv/concepts/projects/layout/)
5. [uv：依赖管理 ↪](https://docs.astral.sh/uv/concepts/projects/dependencies/)、[锁定和同步 ↪](https://docs.astral.sh/uv/concepts/projects/sync/)
6. [uv：工具 ↪](https://docs.astral.sh/uv/guides/tools/)、[脚本 ↪](https://docs.astral.sh/uv/guides/scripts/)、[构建发布 ↪](https://docs.astral.sh/uv/guides/package/)
7. [Poetry：基本用法 ↪](https://python-poetry.org/docs/basic-usage/)、[依赖组 ↪](https://python-poetry.org/docs/managing-dependencies/)、[命令行参考 ↪](https://python-poetry.org/docs/cli/)
8. [Pixi 官方文档 ↪](https://pixi.sh/latest/)
