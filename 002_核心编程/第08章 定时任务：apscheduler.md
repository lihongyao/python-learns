# APScheduler

## 简介

APScheduler（Advanced Python Scheduler）是在进程内按时间规则调度 Python callable 的库，支持一次性、间隔和日历（cron）触发。

它负责计算执行时间并提交任务，不是分布式任务队列，也不会自动保证多进程部署中只执行一次。

## 版本说明

本章采用 APScheduler **3.11.3** 的稳定版 API：

```shell
python -m pip install "APScheduler==3.11.3"
```

APScheduler 4.x 正在进行重大 API 重写，使用 `Scheduler`、`AsyncScheduler`、`add_schedule()` 等新概念；不要把 3.x 和 4.x 示例混用。升级时按官方迁移文档逐项调整。

# 基本用法

## 创建和启动调度器

```python
from datetime import datetime
from time import sleep

from apscheduler.schedulers.background import BackgroundScheduler


def job():
    print(f"任务执行：{datetime.now():%H:%M:%S}")


if __name__ == "__main__":
    scheduler = BackgroundScheduler(timezone="Asia/Shanghai")
    scheduler.add_job(job, "interval", seconds=5, id="print-time")
    scheduler.start()
    try:
        while True:
            sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown(wait=True)
```

- `BackgroundScheduler.start()` 启动后台线程并立即返回；主程序结束时调度器也会停止。
- `BlockingScheduler.start()` 占用当前线程，适合独立脚本。
- `AsyncIOScheduler` 与 `asyncio` 事件循环集成；异步任务需确认库版本和执行器行为。
- 调度器启动后不能再修改其核心配置；程序结束时调用 `shutdown()`。

时区优先使用标准库 `zoneinfo` 支持的名称。时间规则涉及夏令时，应明确时区并测试重复或不存在的本地时间。

# 任务和触发器

## `add_job()`

```python
scheduler.add_job(
    func,
    trigger="interval",
    seconds=10,
    id="unique-job-id",
    args=(1,),
    kwargs={"enabled": True},
    max_instances=1,
    coalesce=True,
    misfire_grace_time=30,
)
```

常用参数：

- `func`：任务 callable；持久化作业或进程池执行时应可被导入和序列化。
- `trigger`：`date`、`interval`、`cron`，也可以传入触发器对象。
- `id`：任务标识；初始化持久化作业时应显式指定。
- `args`、`kwargs`：传给任务函数的参数。
- `start_date`、`end_date`：开始、结束时间。
- `max_instances`：同一任务允许同时执行的最大实例数，默认通常为 1。
- `misfire_grace_time`：错过计划时间后仍允许执行的最大延迟。
- `coalesce`：多次错过时是否合并为一次执行。
- `next_run_time=None`：先以暂停状态创建任务。

默认添加到内存作业存储器；任务不会跨进程共享，也不会在进程重启后保留。

## 一次性触发 `date`

```python
from datetime import datetime, timedelta

scheduler.add_job(
    job,
    trigger="date",
    run_date=datetime.now() + timedelta(seconds=10),
)
```

省略 `run_date` 通常表示尽快执行。一次性任务完成后会从调度器中移除。

## 间隔触发 `interval`

```python
scheduler.add_job(job, "interval", minutes=10)
```

可使用 `seconds`、`minutes`、`hours`、`days`、`weeks` 等参数。间隔任务不会因为设置了 10 分钟就保证每次精确在整点执行，实际时间还会受调度器唤醒、执行器容量和系统负载影响。

## 日历触发 `cron`

```python
scheduler.add_job(
    job,
    "cron",
    day_of_week="mon-fri",
    hour=12,
    minute=0,
)
```

适合“工作日 12:00”“每月某日”等规则。建议使用 `mon`、`fri` 等名称表达星期，避免不同版本或系统对数字星期的误解。

# 四类组件

1. **触发器（Trigger）**：计算下一次运行时间。
2. **作业存储器（Job store）**：保存任务定义；内存存储器重启后丢失。
3. **执行器（Executor）**：将任务提交到线程池或进程池。
4. **调度器（Scheduler）**：协调触发器、作业存储器和执行器。

## 作业存储器

常用内置存储器：

- `MemoryJobStore`：默认，适合临时任务。
- `SQLAlchemyJobStore` 等持久化存储器：适合重启后恢复任务。

持久化任务需要注意：

- 任务函数通常必须是模块级、可导入的 callable。
- 参数和相关对象必须可序列化。
- 应指定稳定的 `id`，并在初始化时使用 `replace_existing=True`，避免每次重启重复添加。
- 一个作业存储器不应被多个独立调度器实例共享。

## 执行器

- `ThreadPoolExecutor`：默认选择，适合 I/O 密集型任务。
- `ProcessPoolExecutor`：适合 CPU 密集型任务，但函数和参数需可序列化。

执行器容量会影响任务延迟。任务运行时间超过触发间隔时，应结合 `max_instances`、`coalesce` 和任务幂等性设计。

# 任务管理

`add_job()` 返回 `Job` 对象：

```python
job = scheduler.add_job(report_job, "interval", minutes=10, id="report")

job.pause()
job.resume()
job.modify(name="daily report")
job.reschedule("cron", hour=9, minute=0)
job.remove()
```

也可以按 ID 操作：

```python
scheduler.pause_job("report")
scheduler.resume_job("report")
scheduler.modify_job("report", name="daily report")
scheduler.reschedule_job("report", "cron", hour=9, minute=0)
scheduler.remove_job("report")
```

调度器级别操作：

```python
scheduler.pause()
scheduler.resume()
scheduler.print_jobs()
scheduler.shutdown(wait=True)
```

`scheduler.pause()` 暂停处理所有任务；`job.pause()` 只暂停单个任务。`shutdown(wait=False)` 不等待正在运行的任务结束，但不会强制终止它们。

# 执行结果和异常

任务函数的返回值不会自动被 `add_job()` 调用方取得。执行结果和异常可通过监听器观察：

```python
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED


def listener(event):
    if event.exception:
        print(f"任务失败：{event.job_id}")
    else:
        print(f"任务完成：{event.job_id}")


scheduler.add_listener(listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
```

监听器只适合记录、指标和通知，不应把耗时业务逻辑直接放在其中。任务内部也应记录异常上下文；单个任务失败不会自动停止调度器。

# 错过执行与任务重叠

## misfire

调度器关闭、机器暂停或执行器繁忙时，任务可能错过计划时间。`misfire_grace_time` 决定超时任务是否还允许补执行。

## coalesce

当同一任务错过多个执行点时：

- `coalesce=True`：合并为一次执行。
- `coalesce=False`：可能连续补执行多个实例。

选择取决于任务语义：发送通知等通常不应重复，账务补偿等可能需要逐次处理。

## 任务重叠

`max_instances` 限制同一任务并发实例数。限制不是分布式锁；多个进程中的多个调度器仍可能各自执行一份任务。

任务应尽量幂等，并在业务层设计唯一键、租约或分布式锁。多进程 Web 部署时通常单独运行一个调度器，或使用支持多节点协调的任务系统。

# 配置示例

```python
from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler(
    jobstores={
        "default": SQLAlchemyJobStore(url="sqlite:///jobs.sqlite"),
    },
    executors={
        "default": ThreadPoolExecutor(10),
        "processpool": ProcessPoolExecutor(2),
    },
    job_defaults={
        "coalesce": True,
        "max_instances": 1,
        "misfire_grace_time": 30,
    },
    timezone="Asia/Shanghai",
)
```

配置持久化存储器时，应在调度器启动前完成，并保证数据库连接、任务序列化和部署拓扑符合要求。SQLite 适合简单单进程场景，不等于多节点调度协调方案。

# 常见注意事项

- 先确认 APScheduler 主版本，再选择对应文档；不要混用 3.x 与 4.x API。
- `BackgroundScheduler` 需要主程序保持运行；Web 应用的重载器和多工作进程可能启动多份调度器。
- `max_instances`、`misfire_grace_time`、`coalesce` 解决不同问题，不能互相替代。
- cron 任务要明确时区，并测试夏令时切换。
- 持久化任务函数必须可导入、参数可序列化；不要直接使用局部函数、lambda 或打开的文件对象。
- 调度器只负责调度，不能替代可靠消息队列、分布式锁或工作流系统。
- 关闭程序时调用 `shutdown()`，并根据业务选择是否等待正在运行的任务。

# 推荐阅读

- [APScheduler 3.11 用户指南](https://apscheduler.readthedocs.io/en/3.x/userguide.html)
- [`BackgroundScheduler`](https://apscheduler.readthedocs.io/en/3.x/modules/schedulers/background.html)
- [`add_job()`](https://apscheduler.readthedocs.io/en/3.x/modules/schedulers/base.html#apscheduler.schedulers.base.BaseScheduler.add_job)
- [APScheduler 3.x 到 4.x 迁移](https://apscheduler.readthedocs.io/en/master/migration.html)
