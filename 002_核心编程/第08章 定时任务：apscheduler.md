# APScheduler

## 简介

APScheduler（Advanced Python Scheduler）是一个用于调度 Python 任务的第三方库，可以按指定时间执行一次任务，也可以按固定间隔或日历规则重复执行任务。

## 版本说明

本章示例使用 APScheduler 3.x 的 API（`BackgroundScheduler`、`add_job()`）。安装时固定在 4.x 之前：

```shell
pip install "APScheduler<4"
```

APScheduler 4.x 对调度器和任务 API 做了较大调整，升级时应参考官方迁移文档，不要直接混用两个版本的写法。

# 基本用法

## 定义任务函数

任务函数就是调度器到达触发时间后执行的普通 Python 函数：

```python
from datetime import datetime


def job():
    print(f"任务执行时间：{datetime.now()}")
```

任务函数应尽量短小，并妥善处理异常。长时间运行的任务会占用执行器中的工作线程。

## 创建和启动调度器

`BackgroundScheduler` 在独立线程中运行，调用 `start()` 后会立即返回，不会阻塞主线程：

```python
from datetime import datetime
import time

from apscheduler.schedulers.background import BackgroundScheduler


def job():
    print(f"任务执行时间：{datetime.now()}")


if __name__ == "__main__":
    scheduler = BackgroundScheduler(timezone="Asia/Shanghai")
    scheduler.add_job(
        job,
        trigger="interval",
        seconds=5,
        id="print-time",
    )
    scheduler.start()
    print("调度器已启动，按 Ctrl+C 退出")

    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown(wait=True)
```

`BackgroundScheduler` 不会替主程序阻止退出；如果主线程很快执行完毕，任务可能还没有机会运行。因此，独立脚本需要保持主线程运行，或改用 `BlockingScheduler`。

## 调度器类型

APScheduler 3.x 常用的调度器有：

| 调度器 | 特点 | 适用场景 |
| --- | --- | --- |
| `BackgroundScheduler` | 在后台线程运行，`start()` 不阻塞 | Web 应用或已有主循环的程序 |
| `BlockingScheduler` | 在当前线程运行，`start()` 会阻塞 | 独立的定时任务脚本 |
| `AsyncIOScheduler` | 与 `asyncio` 事件循环集成 | 异步应用 |

调度器一旦启动，就不应再修改其核心配置。程序结束时应调用 `shutdown()` 释放执行器和作业存储器。

# 任务和触发器

## `add_job()`

使用 `add_job()` 将任务加入调度器：

```python
scheduler.add_job(
    func,                 # 任务函数
    trigger="interval",   # 触发器类型
    seconds=10,
    id="unique-job-id",
    args=(1,),
    kwargs={"enabled": True},
)
```

常用参数：

- `func`：要执行的函数，不能依赖无法导入的局部函数或匿名函数。
- `trigger`：触发器类型，可以是 `date`、`interval` 或 `cron`。
- `id`：任务标识，使用持久化作业存储器时应明确指定。
- `args`、`kwargs`：传给任务函数的位置参数和关键字参数。
- `start_date`、`end_date`：任务开始和结束时间。
- `max_instances`：同一任务允许同时运行的最大实例数。
- `misfire_grace_time`：任务错过计划时间后允许延迟执行的秒数。
- `coalesce`：多次错过执行时间时，是否合并为一次执行。

`add_job()` 返回一个 `Job` 对象，可以保存该对象后进行修改或删除。

## 三种内置触发器

### `date`

只执行一次。如果不指定 `run_date`，通常表示尽快执行：

```python
from datetime import datetime, timedelta


scheduler.add_job(
    job,
    trigger="date",
    run_date=datetime.now() + timedelta(seconds=10),
)
```

### `interval`

按照固定时间间隔重复执行：

```python
scheduler.add_job(job, "interval", minutes=10)
```

也可以使用 `seconds`、`hours`、`days` 等参数。

### `cron`

按照日历规则执行，适合“每天某时刻”或“每周某天”等场景：

```python
scheduler.add_job(
    job,
    trigger="cron",
    day_of_week="mon-fri",
    hour=12,
    minute=0,
)
```

`cron` 的时间字段可以使用数字、范围和通配符，例如 `minute="*/5"` 表示每 5 分钟一次。

# 四大组件

APScheduler 由四类组件协作完成任务调度：

1. 触发器（Trigger）：计算任务下一次执行的时间。
2. 作业存储器（Job store）：保存任务信息。默认的 `MemoryJobStore` 只保存在内存中，进程重启后任务会丢失。
3. 执行器（Executor）：负责执行任务。默认使用线程池，也可以配置进程池。
4. 调度器（Scheduler）：协调上述组件，提供添加、修改、暂停和删除任务的接口。

## 作业存储器

不需要持久化时，使用默认的内存作业存储器即可。需要在程序重启后保留任务时，可以配置 SQLAlchemy、MongoDB 等持久化作业存储器。

持久化作业存储器通常需要注意：

- 任务函数必须可以被正常导入，不能使用局部函数或 `lambda`。
- 任务参数必须可以序列化。
- 初始化时应指定稳定的 `id`，必要时使用 `replace_existing=True`，避免应用重启后重复添加同一个任务。
- 一个作业存储器不应被多个调度器实例共享。

## 执行器

- `ThreadPoolExecutor`：默认执行器，适合大多数 I/O 密集型任务。
- `ProcessPoolExecutor`：使用进程执行，适合 CPU 密集型任务，但任务函数和参数必须可序列化。

执行器中的工作线程或进程数量会限制任务的并发执行数量。任务执行时间过长时，应合理设置 `max_workers` 和 `max_instances`。

# 任务管理

`add_job()` 返回的任务对象可以用于管理任务：

```python
report = scheduler.add_job(report_job, "interval", minutes=10, id="report")

report.pause()    # 暂停任务
report.resume()   # 恢复任务
report.remove()   # 删除任务
```

也可以通过调度器和任务 ID 操作：

```python
scheduler.pause_job("report")
scheduler.resume_job("report")
scheduler.remove_job("report")
```

关闭调度器：

```python
scheduler.shutdown(wait=True)
```

`wait=True` 表示等待正在执行的任务结束；使用 `wait=False` 时不会等待运行中的任务。

# 常见注意事项

- `BackgroundScheduler.start()` 返回后，主程序仍需保持运行，否则调度器线程可能随进程退出。
- 同一个任务可能因执行时间过长而与下一次计划重叠，应合理设置 `max_instances`。
- 程序暂停或调度器关闭期间错过的任务可能触发 misfire，应根据任务性质设置 `misfire_grace_time` 和 `coalesce`。
- 多进程 Web 部署时不要让每个工作进程都启动一份调度器，否则同一任务可能被执行多次；通常应单独运行调度器或确保只有一个实例负责调度。
- 任务内部应记录日志并处理异常，避免单个任务失败后难以排查。

更多内容可参考：

- [APScheduler 3.x 用户指南](https://apscheduler.readthedocs.io/en/3.x/userguide.html)
- [`BackgroundScheduler`](https://apscheduler.readthedocs.io/en/3.x/modules/schedulers/background.html)
- [`date` 触发器](https://apscheduler.readthedocs.io/en/3.x/modules/triggers/date.html)
- [`interval` 触发器](https://apscheduler.readthedocs.io/en/3.x/modules/triggers/interval.html)
- [`cron` 触发器](https://apscheduler.readthedocs.io/en/3.x/modules/triggers/cron.html)
- [APScheduler 迁移到 4.x](https://apscheduler.readthedocs.io/en/master/migration.html)
