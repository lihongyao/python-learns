# 概述

从零开始学习 Python，记录基础语法、核心编程、Web 开发、数据库和项目实践。

本仓库以 Markdown 笔记为主，并配有可运行的 Python 示例。建议按“语法基础 → 核心编程 → 高级应用 → PostgreSQL”的顺序学习；遇到不熟悉的主题时，可以先阅读对应章节，再运行 `CODES/` 中的示例进行验证。

参考资料：

1. [Python 官方教程 ↪](https://docs.python.org/zh-cn/3/tutorial/index.html)
2. [菜鸟教程：Python 3 教程 ↪](https://www.runoob.com/python3/python3-tutorial.html)
3. [Python Playground ↪](https://python-playground.com/)

# 学习路线

- [语法基础](<001_语法基础/>)：数据类型、字符串、列表、字典、集合、函数、异常和模块。
- [核心编程](<002_核心编程/>)：面向对象、文件操作、正则表达式、线程、进程、协程、插件和定时任务。
- [高级应用](<003_高级应用/>)：Python 项目管理（Poetry、uv）、FastAPI、SQLAlchemy、项目实战、Docker 和 Containerd。
- [PostgreSQL](<004_PostgreSQL/>)：数据库基础、数据类型、用户、表、模式、数据操作和高级用法。
- [代码示例](<CODES/>)：基础语法、FastAPI 教程和学生管理系统等示例代码。

# 仓库结构

```text
001_语法基础/       Python 基础语法笔记
002_核心编程/       Python 核心编程笔记
003_高级应用/       Web 开发、ORM、容器和项目实践
004_PostgreSQL/    PostgreSQL 学习笔记
CODES/             配套 Python 示例代码
xminds/            思维导图文件
imgs/              文档配图
```

# 快速开始

1. 克隆仓库并进入目录：

   ```shell
   git clone https://github.com/lihongyao/python-learns.git
   cd python-learns
   ```

2. 选择一种环境管理方式，创建并激活独立环境。Conda 和 `venv + pip` 的示例见下文。

3. 从 [学习路线](#学习路线) 选择章节，或直接运行基础示例：

   ```shell
   python -c "print('Python 环境已就绪')"
   python CODES/basic/01_基础语法.py
   ```

   第一条命令用于确认解释器可用。基础示例主要演示语法表达式，脚本没有额外的输出。如果使用了虚拟环境，请先激活环境。Windows 如果 `python` 命令不可用，可以尝试 `py`；macOS/Linux 如果未配置 `python`，可以将命令中的 `python` 替换为 `python3`。

# 虚拟环境

虚拟环境用于隔离项目的 Python 解释器和依赖包，避免不同项目之间发生版本冲突。

虚拟环境本身不负责“打包”依赖；跨机器复现环境时，应提交 `environment.yml` 或 `requirements.txt` 等依赖清单。

常见选择如下：

- **Conda**：适合需要管理多个 Python 版本、科学计算库或非 Python 系统依赖的项目。
- **venv + pip**：Python 内置方案，适合大多数轻量项目。
- **Poetry 或 uv**：适合希望统一管理项目元数据、锁定依赖版本的项目。本仓库的指南见 [第 01 章：Python 项目与依赖管理（Poetry 与 uv）](<003_高级应用/第01章 Python 项目与依赖管理.md>)。

## venv + pip

`venv` 随 Python 一起提供，不需要额外安装环境管理器。在仓库根目录执行：

```shell
python -m venv .venv
```

建议将 `.venv/` 加入项目的 `.gitignore`，不要把本地虚拟环境提交到版本库。

激活环境：

```shell
# macOS/Linux
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1

# Windows CMD
.venv\Scripts\activate.bat
```

激活后使用 `python -m pip` 安装依赖；如果当前项目提供 `requirements.txt`，可以执行：

```shell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
deactivate
```

如果项目没有 `requirements.txt`，可以只安装当前示例需要的包，例如：

```shell
python -m pip install fastapi uvicorn
```

# Conda

[Conda](https://docs.conda.io/) 是跨平台的环境和包管理工具，可以管理 Python 以及部分非 Python 依赖。推荐使用 [Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/install)，它比完整 Anaconda 更轻量。

## 安装

macOS 使用 Homebrew 时，可以执行：

```shell
brew install --cask miniconda
conda init zsh
exec zsh
conda --version
```

Windows 和 Linux 请按照 [Miniconda 安装文档](https://www.anaconda.com/docs/getting-started/miniconda/install) 选择对应安装包。`conda init` 只需要初始化正在使用的 Shell；例如 Bash 使用 `conda init bash`，PowerShell 使用 `conda init powershell`。

国内网络环境下可以按需配置镜像。镜像地址可能会变化，使用前请以镜像站说明为准：

```shell
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --set show_channel_urls yes
```

如果不希望打开终端时自动进入 `base` 环境，可以执行：

```shell
conda config --set auto_activate_base false
```

## 创建项目环境

示例使用 Python 3.14.7；实际项目可以根据依赖兼容性选择其他版本：

```shell
conda create -n learns python=3.14.7
conda activate learns
python --version
```

在已激活的环境中安装依赖时，优先使用 Conda 能提供的包；需要从 PyPI 安装时，使用当前环境对应的解释器：

```shell
conda install numpy
python -m pip install 包名
```

退出环境：

```shell
conda deactivate
```

## 导出和恢复环境

跨平台分享时，建议只导出明确安装过的依赖：

```shell
conda export --from-history --format=environment-yaml --file environment.yml
```

在另一台机器上创建环境：

```shell
conda env create --file environment.yml
conda activate learns
```

如果需要精确复现当前平台的完整解析结果，也可以使用传统命令：

```shell
conda env export --file environment.yml
```

## 常用命令

```shell
# 查看所有环境
conda env list

# 删除环境
conda remove --name 环境名 --all --yes

# 更新指定环境中的全部包
conda update --name 环境名 --all
```

不建议把项目依赖安装到 `base` 环境。进入项目目录后，再按项目需要激活对应环境即可，不必每次打开终端都激活同一个环境。

# pip

`pip` 是 Python 的包安装器，通常从 [Python Package Index（PyPI）](https://pypi.org/) 获取和安装第三方包。

建议始终使用 `python -m pip`，这样可以确保 pip 与当前 Python 解释器对应。

## 基础命令

```shell
# 查看 pip 版本及路径
python -m pip --version

# 安装包
python -m pip install 包名

# 安装指定版本
python -m pip install 包名==版本号

# 升级包
python -m pip install --upgrade 包名

# 卸载包
python -m pip uninstall 包名

# 列出已安装的包
python -m pip list

# 查看包详细信息
python -m pip show 包名
```

## 依赖文件

导出当前环境中的包，并在另一台机器上安装：

```shell
python -m pip freeze > requirements.txt
python -m pip install -r requirements.txt
```

`pip freeze` 会记录当前环境中的所有已安装包，适合复现已有环境。新项目也可以手动维护只包含直接依赖的 `requirements.txt`，并在需要时使用锁定工具生成完整依赖集合。

## 配置与维护

```shell
# 升级 pip 自身
python -m pip install --upgrade pip

# 临时使用镜像源
python -m pip install 包名 --index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 永久配置镜像源（会影响当前用户的所有 pip 命令）
python -m pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/

# 检查依赖是否存在冲突
python -m pip check

# 清理缓存
python -m pip cache purge
```

# IDE

## VS Code

推荐安装 [VS Code](https://code.visualstudio.com/download) 以及以下扩展：

- [Python](https://marketplace.visualstudio.com/items/?itemName=ms-python.python)：运行、调试和管理 Python 项目。
- [Pylance](https://marketplace.visualstudio.com/items/?itemName=ms-python.vscode-pylance)：代码补全、类型分析和跳转。
- [Black Formatter](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter)：代码格式化。

按需选择一个代码质量工具即可，例如 [Ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff) 或 [Flake8](https://marketplace.visualstudio.com/items?itemName=ms-python.flake8)。需要类型检查时再安装 [mypy](https://marketplace.visualstudio.com/items?itemName=ms-python.mypy-type-checker)；`isort`、Path Intellisense 和 SQL Beautify 等扩展可按个人工作流安装。

### 选择 Python 解释器

1. 使用 <kbd>Command</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd>（Windows/Linux 使用 <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd>）打开命令面板。
2. 执行 `Python: Select Interpreter`。
3. 选择当前项目的 Conda 环境或 `.venv` 环境。

### 配置格式化

安装 Black Formatter 后，在 Python 文件中执行“Format Document With...” → “Configure Default Formatter...”并选择 Black Formatter。也可以在 VS Code 的 `settings.json` 中配置：

```json
{
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.formatOnSave": true
  }
}
```

Black Formatter 扩展通常自带格式化程序；只有在项目明确要求使用特定版本时，才需要在当前环境中单独安装 `black`。

## PyCharm

可以参考 [PyCharm 安装指南](https://www.jetbrains.com/zh-cn/help/pycharm/installation-guide.html) 和 [键盘快捷键指南](https://www.jetbrains.com/zh-cn/help/pycharm/mastering-keyboard-shortcuts.html)。创建项目时选择已有的 Conda 环境或项目内 `.venv`，并按需安装代码检查、格式化等插件。

# 初体验

以下命令在仓库根目录执行，创建一个最小示例并运行它：

```shell
mkdir -p examples
printf "print('Hello, World!')\n" > examples/main.py
python examples/main.py
```

如果希望使用 VS Code 打开示例目录：

```shell
code examples
```

也可以在编辑器中打开 `examples/main.py`，使用右上角的运行按钮或运行和调试面板执行文件。

使用集成终端时，可通过 <kbd>Ctrl</kbd> + <kbd>\`</kbd> 打开终端。

macOS 也可以使用 <kbd>Control</kbd> + <kbd>`</kbd>。
