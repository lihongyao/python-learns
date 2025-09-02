

# 概述

[Poetry ↪](https://python-poetry.org/) 是一个现代化的 Python 依赖管理和打包工具，它旨在简化 Python 项目的依赖管理和打包发布流程。相比于传统的 pip+virtualenv 组合，Poetry 提供了更直观、更强大的功能：

1. 依赖管理：声明式地管理项目依赖
2. 虚拟环境管理：自动创建和管理虚拟环境
3. 打包发布：轻松打包和发布项目到PyPI
4. 锁定依赖：生成lock文件确保依赖版本一致性
5. 多环境支持：区分开发依赖和生产依赖

# 安装

@See https://python-poetry.org/docs/#installation

官方提供了多种安装方式，我用的是 macOS，所以我直接选择使用 brew 来安装了。

```shell
$ brew install poetry
$ poetry --version # Poetry (version 2.1.3)
```

> **提示**：安装完成之后，可能需要重启终端。

# 配置（可选）

```shell
# 查看配置
$ poetry config --list
# 关闭自动创建虚拟环境（如需全局安装包）
$ poetry config virtualenvs.create true
# 更改虚拟环境存储路径：
$ poetry config virtualenvs.path ~/.cache/pypoetry/virtualenvs
# 配置国内镜像
$ poetry source add tuna https://pypi.tuna.tsinghua.edu.cn/simple
```

# 基本使用

在此之前，我们每次创建新项目，都是基于 conda 为该项目构建一个单独的环境，以实现依赖的隔离，poetry 会自动为我们创建虚拟环境，那么 conda 的作用我们可以把它看成是对 python 版本的管理，就好比使用 nvm 管理 nodejs一样，我们可以在系统安装多个 python 版本，然后每次开发的时候，切换到指定版本即可，那之前我们命名 conda 构建的环境名字的时候，是以项目名来命名的，那么现在，我们可以考虑通过类似 py12，py13这样的命名，如：

```shell
$ conda create -n py12 python=3.12
$ conda create -n py13 python=3.13
```

每次开启项目时，可以通过 `conda activate xxx` 启用对应的版本进行开发。

接下来，我们看看 poetry 如何使用。

**1）创建新项目（库开发）**

```shell
$ poetry new my_project
$ cd my_project 
```

这会创建一个标准的项目结构：

```perl
my_project
├── pyproject.toml # 项目配置和依赖声明文件
├── README.md
├── src
│   └── my_project # 项目源代码目录
│       └── __init__.py
└── tests          # 测试目录
    └── __init__.py
```

**2）初始化已有项目**

在实际开发中，大多数使用 poetry 来管理依赖，作为项目开发中使用，因此建议首先创建项目目录，然后手动初始化，如下所示：

```shell
# 创建项目目录
$ mkdir my_project && cd my_project

# 只初始化pyproject.toml（跳过交互问答）
$ poetry init --no-interaction --python "^3.13"  # 指定你的Python版本

# 或交互式初始化（按需选择）
$ poetry init
```

# 虚拟环境管理

Poetry会自动为项目创建虚拟环境

```shell
# 查看虚拟环境信息
$ poetry env info
# 列出所有虚拟环境
$ poetry env list
# 使用特定Python版本
$ poetry env use /path/to/python
```

# 依赖管理

```shell
# 添加生产依赖
poetry add requests
# 添加开发依赖
poetry add pytest --dev
# 安装所有依赖（含开发依赖）
poetry install
# 仅安装生产依赖
poetry install --no-dev
```

# 镜像

```shell
$ poetry env create xxx
$ poetry env remove 
```



