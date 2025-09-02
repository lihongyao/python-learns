# 思路分析

https://blog.csdn.net/u011027547/article/details/144037652



## BackgroundScheduler

BackgroundScheduler 是 apscheduler 库中的一个后台调度器，可以在不阻塞主线程的情况下运行定时任务。

datetime 用于获取当前时间和进行时间计算。

time 用于在无限循环中进行休眠

## 定义任务函数

```python
   def job():
       """
       定义要执行的任务函数。
       在这里可以调用其他函数或执行特定的逻辑。
       """
       print(f"任务正在执行！时间: {datetime.now()}")

```

job 函数是实际要执行的任务，这里简单地打印一条消息，显示任务执行的时间。

## 创建调度器实例

```python
scheduler.add_job(
       job,  # 要执行的任务函数
       'cron',  # 触发器类型，表示按照 cron 表达式触发
       hour=12,  # 设置小时，这里设置为 12
       minute=14  # 设置分钟，这里设置为 14
   )

```

## 启动调度器

scheduler.start()

# 四大组件

- triggers：触发器，用于设定触发任务的条件
- job stores：作业存储器，用于存放任务，可以存放在数据库或内存，默认内存
- executors：执行器，用于执行任务，可以设定执行默认为单线程或线程池
- schedulers：调度器，将上述三个组件作为参数，通过创建调度器实例来执行



### 触发器 triggers

每个任务都有自己的触发器，它可以决定任务触发的条件，触发器默认是无状态的。



### 作业存储器 job stores

默认存储在内存中，若存储到[数据库](https://so.csdn.net/so/search?q=数据库&spm=1001.2101.3001.7020)中会有个序列化和反序列化的过程，同时修改和搜索任务的功能也是由它实现。



##### 一个作业存储器不要共享给多个调度器，不然会造成状态混乱

### 执行器 executors

将任务放入线程或线程池中执行，执行完毕通知调度器

### 调度器 schedulers

调度器提供接口，可以将触发器、作业存储器和执行器整合起来，从而实现对任务的操作。

### 调度器组件

- BlockingScheduler 阻塞式调度器：适用于只跑调度器的程序。
- BackgroundScheduler 后台调度器：适用于非阻塞的情况，调度器会在后台独立运行。
- AsyncIOScheduler AsyncIO调度器，适用于应用使用AsnycIO的情况。
- GeventScheduler Gevent调度器，适用于应用通过Gevent的情况。
- TornadoScheduler Tornado调度器，适用于构建Tornado应用。
- TwistedScheduler Twisted调度器，适用于构建Twisted应用。
- QtScheduler Qt调度器，适用于构建Qt应用。

### 选择正确的调度器、作业存储器、触发器和执行器

1、作业存储器

- 作业不需要持久化：默认的 MemoryJobStore
- 作业需要持久化：作业在调度程序重启或应用程序奔溃后继续存在，推荐采用：SQLAlchemyJobStore + PostgreSQL
  2、执行器
- 默认 ThreadPoolExecutor 线程池足以满足大多数场景
- CPU 密集型操作：应考虑 ProcessPoolExecutor 进程池，来充分利用多核算力。也可以将 ProcessPoolExecutor 作为第二执行器，混合使用两种不同的执行器。



### 触发器详解

一个任务可以设定多种触发器，如全部条件满足触发、满足其一触发以及复合触发等：
[apscheduler.triggers.combining](https://apscheduler.readthedocs.io/en/latest/modules/triggers/combining.html#module-apscheduler.triggers.combining)
内置的三种[触发器类型](https://so.csdn.net/so/search?q=触发器类型&spm=1001.2101.3001.7020)

- date：[apscheduler.triggers.date](https://apscheduler.readthedocs.io/en/latest/modules/triggers/date.html#module-apscheduler.triggers.date)
- interval：[apscheduler.triggers.interval](https://apscheduler.readthedocs.io/en/latest/modules/triggers/interval.html#module-apscheduler.triggers.interval)
- cron：[apscheduler.triggers.cron](https://apscheduler.readthedocs.io/en/latest/modules/triggers/cron.html#module-apscheduler.triggers.cron)