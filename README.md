# 概述
从零开始的Python学习之旅——记录代码成长与项目实践

Python 是一门易于学习、功能强大的编程语言。它提供了高效的高级数据结构，还能简单有效地面向对象编程。Python 优雅的语法和动态类型以及解释型语言的本质，使它成为多数平台上写脚本和快速开发应用的理想语言。

[Python 教程 >> ](https://docs.python.org/zh-cn/3/tutorial/index.html)

# 安装 Python

可以基于以下两种方式安装 Python：

1. [官网下载 >>](https://www.python.org/downloads)
2. 使用 [Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/install)，类似于 nvm 管理 nodeJS *（推荐，便于多版本管理和升级）*

因为我的系统是 macOS，所以直接使用 HomeBrew 安装 miniconda，来管理 Python。

```bash
# 安装 miniconda
$ brew install --cask miniconda

# 验证安装， 应显示版本号（如 conda 25.x.x）
$ conda --version

# 初始化 conda（推荐）
$ conda init --all

# 创建虚拟环境（安装 python）
$ conda install python

# 验证安装
$ python3 --version
```

# 安装 IDE

推荐VS Code + Python插件。

# 初体验

```shell
# 创建项目
$ cd Desktop && mkdir -p examples && touch examples/hello_word.py
# 填充代码
$ echo "print('Hello World')" > examples/hello_word.py 
# 在编辑器中打开项目
$ code ./examples
```

运行：

- **方法一**：右键文件 → **“在终端运行 Python 文件”**（需提前安装 Python 解释器）

- **方法二**：打开终端（<kbd>Ctr</kbd> + <kbd>`</kbd>）→ 输入命令：

  ```bash
  $ python hello_word.py 
  ```
