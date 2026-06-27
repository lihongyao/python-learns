# 概述
从零开始的Python学习之旅——记录代码成长与项目实践

Python 是一门易于学习、功能强大的编程语言。它提供了高效的高级数据结构，还能简单有效地面向对象编程。Python 优雅的语法和动态类型以及解释型语言的本质，使它成为多数平台上写脚本和快速开发应用的理想语言。

1. [官方教程 ↪](https://docs.python.org/zh-cn/3/tutorial/index.html)
2. [菜鸟教程 ↪](https://www.runoob.com/python3/python3-tutorial.html)

# 虚拟环境

在 Python 开发中，我们常常会面临这样的问题：不同项目可能依赖于同一库的不同版本，或者某些项目需要特定的 Python 解释器版本。如果将所有的包都安装在全局环境中，可能会导致版本冲突，影响项目的正常运行。为了解决这些问题，Python 引入了虚拟环境的概念，而 Conda 则是一个功能强大的包和环境管理工具，能帮助我们更方便地创建和管理虚拟环境。

虚拟环境是 Python 提供的一种将项目的依赖项隔离开来的机制。它可以创建一个独立的 Python 环境，每个环境都有自己独立的 Python 解释器 和安装的包，互不干扰。这样，我们就可以在不同的虚拟环境中为不同的项目安装所需的特定版本的库，避免了全局环境中版本冲突的问题。

为什么需要虚拟环境？

- 避免版本冲突：不同项目可能依赖于同一库的不同版本，使用虚拟环境可以为每个项目提供独立的库版本。
- 方便项目迁移：虚拟环境可以将项目的依赖项打包，方便在不同的机器上部署项目。
- 保持全局环境整洁：只在全局环境中安装必要的工具，将项目的依赖项安装在虚拟环境中，使全局环境更加简洁。

# Conda

Conda 是一个开源的包和环境管理系统，可在 Windows、macOS 和 Linux 上运行。它不仅可以管理 Python 包，还可以管理其他语言的包，如 R、Java 等。Conda 可以创建、保存、加载和切换不同的虚拟环境，并且可以快速安装、更新和卸载包。

推荐使用 [Miniconda ↪](https://www.anaconda.com/docs/getting-started/miniconda/install) 搭建 Python 环境和依赖隔离。

> **提示**：conda 类似于 nvm 管理 nodeJS *（推荐，便于多版本管理和升级）*

## 安装

因为我的系统是 macOS，所以直接使用 HomeBrew 安装 miniconda，来管理 Python。

```bash
# 安装 miniconda
$ brew install --cask miniconda

# 初始化 conda，将 Conda 添加到终端环境变量（建议重启终端）
$ conda init --all

# 验证安装， 检查 Conda 版本
$ conda --version

# 配置镜像
$ conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
$ conda config --set show_channel_urls yes

# 禁用自动激活
$ conda config --set auto_activate_base false
```

## 依赖隔离：创建项目环境

**步骤 1：创建虚拟环境**

为每个项目创建独立环境（例如项目名为 `my_project`，Python 3.14.4）：

```shell
$ conda create -n my_project python=3.14.4
```

**步骤 2：激活环境**

```shell
$ conda activate my_project
```

激活后，终端提示符会显示环境名，如 `(my_project)`。

**步骤 3：安装项目依赖**

在激活的环境中安装包（例如 `numpy`）：

```python
$ conda install numpy  # 或使用 pip install numpy
```

**步骤 4：退出环境**

```shell
$ conda deactivate
```

## 新项目标准流程

在每次创建项目之前，我们都应该为项目创建一个独立的环境，如果在全局环境下，会导致依赖冲突等问题，就好比前端通过 npm 全局安装依赖，然而各个项目对依赖版本有所差异，前端可以在项目本地安装，可以很方便的解决依赖隔离的问题，在 Python 中，我们可以通过 conda 来创建环境。比

1. **创建环境**：`conda create -n 项目名 python=版本号`

2. **激活环境**：`conda activate 项目名`

3. **安装依赖**：`conda install 包名` 或 `pip install 包名`

4. **导出依赖**（可选）：

   ```shell
   $ conda env export > environment.yml  # Conda 方式
   $ pip freeze > requirements.txt      # Pip 方式
   ```

5. **退出环境**：`conda deactivate`

示例：比如我们现在需要创建一个环境用于我们后续的学习，所以我可以创建一个 `learns` 的环境，操作如下：

```shell
$ conda create -n learns python=3.14.4
$ conda activate learns
```

## 其他实用指令

- **查看所有环境**：`conda env list`

- **删除环境**：`conda remove -n 环境名 --all -y`

- **批量删除**

  ```shell
  $ for env in <env1> <env2> <env3> ...; do conda remove -n $env --all -y; done
  ```

## 注意事项

1. **优先使用 Conda 安装包**：减少依赖冲突（尤其是科学计算库如 `numpy`）。
2. **避免在 `base` 环境安装包**：保持干净的系统环境。
3. 每次打开终端时，记得先激活环境。

# pip

`pip` 是 Python 的官方包管理工具，全称为 **"Pip Installs Packages"**，用于安装、升级、卸载和管理 Python 第三方库。它直接与 Python Package Index (PyPI) 集成，PyPI 是 Python 社区的公共包仓库，包含数十万个开源库。

**（1）基础指令**

```shell
# 查看 pip 版本及路径
$ pip --version
# 安装包（默认最新版）
$ pip install 包名
# 安装指定版本
$ pip install 包名==版本号
# 升级包
$ pip install --upgrade 包名
# 卸载包
$ pip uninstall 包名
# 列出已安装的包
$ pip list
# 查看包详细信息
$ pip show 包名
```

**（2）批量管理**

```shell
# 导出依赖列表到文件
$ pip freeze > requirements.txt
# 从文件安装依赖
$ pip install -r requirements.txt
```

**（3）配置与维护**

```shell
# 升级 pip 自身
$ python -m pip install --upgrade pip
# 临时使用国内镜像源（如清华源）
$ pip install 包名 -i https://pypi.tuna.tsinghua.edu.cn/simple
# 永久配置镜像源
$ pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
```

**（4）其他实用指令**

```shell
# 检查依赖冲突
$ pip check
# 清理缓存
$ pip cache purge
# 获取帮助
$ pip help
```

# IDE

## VSCode

1. 推荐使用 [VS Code](https://code.visualstudio.com/download)
2. 插件安装，打开 VS Code，快捷键 <kbd>Command</kbd> + <kbd>Shift</kbd> + <kbd>X</kbd> 打开扩展商店，搜索框搜索插件并安装，推荐插件如下：
   - [**Python (Microsoft)**](https://marketplace.visualstudio.com/items/?itemName=ms-python.python)：官方扩展
   - **[Pylance](https://marketplace.visualstudio.com/items/?itemName=ms-python.vscode-pylance)**：Python 语言服务器
   - [**Flake8**](https://marketplace.visualstudio.com/items?itemName=ms-python.flake8)：Python代码静态检查工具，用于检测代码风格错误（PEP 8规范）、语法错误和逻辑问题。
   - [**Black Formatter**](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter)：Python代码格式化工具，自动将代码转换为符合PEP 8风格的统一格式（如缩进、引号、行长度等），支持自定义配置。
   - [**isort**](https://marketplace.visualstudio.com/items?itemName=ms-python.isort)：自动对Python的`import`语句按标准库/第三方库/本地模块分组并排序，提升代码可读性。
   - [**mypy**](https://marketplace.visualstudio.com/items?itemName=ms-python.mypy-type-checker)：Python静态类型检查器，通过类型注解在编码阶段发现潜在类型错误，支持泛型、联合类型等高级特性。
   - [**Path Intellisense**](https://marketplace.visualstudio.com/items?itemName=christian-kohler.path-intellisense)：文件路径自动补全插件，输入路径时智能提示目录和文件名，支持别名映射和忽略规则配置
   - [**Python Environment Manager**](https://marketplace.visualstudio.com/items?itemName=donjayamanne.python-environment-manager)：管理Python虚拟环境和解释器，快速切换不同项目的依赖环境
   - [**SQL Beautify**](https://marketplace.visualstudio.com/items?itemName=clarkyu.vscode-sql-beautify)：SQL/HQL代码格式化工具，一键整理杂乱SQL语句（如对齐关键字、标准化缩进），支持DDL和INSERT语句优化。

### 配置 Python 解释器

1. 在 VSCode 中使用快捷键 <kbd>Command</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd> 打开命令面板
2. 输入 Python: Select Interpreter
3. 选择当前项目所需的环境即可，比如刚刚创建的 `learns`

> **再次强调**：你应该为你的项目单独创建环境进行依赖隔离。

### 配置代码格式化

1. VSCode 安装扩展：[**Black Formatter**](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter)

2. 安装 black

   ```shell
   $ pip install black
   ```

   > 提示：`pip` 是 Python 的官方包管理工具

3. 配置 VSCode settings

   - 快捷键：<kbd>Command</kbd> + <kbd>,</kbd>
   - 搜索：python formatting provider
   - 选择 Black Formatter 作为 Python 作为格式化工具

## PyCharm

参考 [入门指南 ↪](https://www.jetbrains.com/zh-cn/help/pycharm/installation-guide.html)

- [学习键盘快捷键 ↪](https://www.jetbrains.com/zh-cn/help/pycharm/mastering-keyboard-shortcuts.html)

- 插件
  - **Fitten Code**

# 初体验

```shell
# 创建项目
$ cd Desktop && mkdir -p examples && touch examples/main.py
# 填充代码
$ echo "print('Hello World')" > examples/main.py 
# 在编辑器中打开项目
$ code ./examples
```

运行：

- **方法一**：右键文件 → **“在终端运行 Python 文件”**（需提前安装 Python 解释器）

- **方法二**：打开终端（<kbd>Ctr</kbd> + <kbd>`</kbd>）→ 输入命令：

  ```bash
  $ python hello_word.py 
  ```

- **方法三**：在编辑器右上角，有一个  ▶ 按钮，有两种选择：
  - 运行 Python 文件
  - Python 调试程序：调试 Python 文件



