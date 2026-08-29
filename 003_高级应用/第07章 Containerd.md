# 概述

## Containerd 概述

1. containerd最早是Docker 1.11版本中routerEngine的一部分，现在已从Docker Engine中独立出来，成为一个单独的开源项目独立发展
2. containerd的功能优势是涵盖了容器运行时管理的所有需求
3. containerd以Daemon的形式运行在系统上，通过暴露底层的gRPC API，让上层系统可以通过这些API管理机器上的容器
4. 每个containerd只负责一台机器，包括pull镜像、容器操作(启动/停止等)、网络和存储管理。具体运行容器由runC负责，支持所有符合OCI规范的容器
5. 对于容器编排服务来说，运行时只需要使用containerd+runC，更加轻量且容易管理
6. 独立后的containerd可以与Docker Engine分开演进，专注容器运行时管理，运行更加稳定

## Containerd 主要组件

- containerd daemon

  作用：containerd是一个守护进程，负责管理容器的生命周期。它作为一个长时间运行的进程，提供容器生命周期管理（启动、停止、销毁容器）、镜像管理（拉取、导入导出镜像）、存储管理等功能。

- Container Runtime (如 runc)

  作用：容器运行时负责实际启动和运行容器。containerd本身并不直接运行容器，而是通过与容器运行时（如 runc）的集成来实现容器的创建和管理。包括：容器创建与启动、容器执行、容器停止、容器销毁等。

- Image Service

  作用：镜像服务负责容器镜像的拉取、存储、管理和推送等操作。

- Content Store

  作用：内容存储负责存储容器镜像的内容，如镜像层、元数据等。它是容器镜像管理的底层存储。

- Snapshotter

  作用：Snapshotter负责容器的文件系统操作，特别是在容器文件系统中的快照管理。容器的文件系统通常是通过分层存储实现的。

- Task Service

  作用：Task服务负责管理容器任务，即容器内正在运行的进程。包括：启动容器内的进程、监控容器进程的状态（如健康检查、日志等）。

- Event Service

  作用：事件服务负责发送和接收容器生命周期相关的事件，如容器的启动、停止、运行状态变化等。支持事件的收集和使用，提供一致的事件驱动的行为和审计。事件可以重播到各个模块。

- Networking (CRI plugin)

  作用：containerd通过插件系统与容器网络插件（CNI）集成，管理容器的网络，如：分配IP地址、设置网络策略等。通过CNI插件支持多种网络模式，如桥接模式、主机模式、覆盖网络等。

- Plugin System

  作用：containerd提供了一个插件系统，使得它可以扩展并支持更多的功能，如网络、存储、日志等。

- Metrics

  作用：每个组件都将暴露一些指标，通过Metrics API进行访问

## containerd与其他容器运行时工具性能对比

containerd在各个方面都表现良好，总体性能由于docker和crio，包括容器的运行时间、停止时间、删除时间，用时都很少、很快，效率很高。

# 安装

1）下载官方二进制文件， [点击前往 ↪](https://github.com/containerd/containerd/releases)：containerd-2.1.0-linux-amd64.tar.gz

2）安装一个小工具

```shell
$ apt install lrzsz
```

3）快捷上传文件

```shell
$ rz 
```

4）解压文件至 `/usr/local` 目录

```shell
$ tar Cxzvf /usr/local containerd-2.1.0-linux-amd64.tar.gz
bin/
bin/containerd
bin/containerd-shim-runc-v2
bin/ctr
bin/containerd-stress
```

**systemd**

通过 systemd 管理 containerd 服务的配置说明，具体步骤如下：

1. **下载 systemd 单元文件**

   从 containerd 官方仓库获取服务配置文件：

   ```shell
   $ curl -o /usr/lib/systemd/system/containerd.service \
   https://raw.githubusercontent.com/containerd/containerd/main/containerd.service
   ```

2. **重载 systemd 配置**

   使新添加的服务文件生效：

   ```shell
   $ systemctl daemon-reload
   ```

3. **启用并启动服务**

   设置开机自启并立即运行 containerd：

   ```shell
   $ systemctl enable --now containerd
   ```

4. **验证服务状态**

   ```shell
   $ systemctl status containerd
   ```

   > **预期输出**：`active (running)` 表示服务已正常运行。

## runc

`runc` 是一个符合 OCI（开放容器标准）的轻量级容器运行时，负责根据容器镜像启动、停止和管理容器进程。

Containerd 通过调用 `runc` 来执行底层的容器操作（如 `docker run` 背后的实际执行者）。

1. 下载二进制文件

   从 [opencontainers/runc ↪](https://github.com/opencontainers/runc/releases) 下载对应架构的 `runc` 二进制文件 —  `runc.amd64`。

2. 通过 rz 指令将其上传至 root 根目录

3. **校验文件完整性**

   通过 `sha256sum` 验证下载文件是否完整（防止篡改或损坏

   ```shell
   $ sha256sum runc.amd64 
   028986516ab5646370edce981df2d8e8a8d12188deaf837142a02097000ae2f2  runc.amd64
   ```

4. **安装到系统路径**

   将二进制文件复制到 `/usr/local/sbin/runc` 并赋予可执行权限：

   ```shell
   $ install -m 755 runc.amd64 /usr/local/sbin/runc
   ```

## CNI

这一步是在 **安装 Kubernetes/Containerd 依赖的 CNI（容器网络接口）插件**，用于为容器提供网络功能（如 IP 分配、跨节点通信等）。以下是具体解析：

- 核心功能：CNI 插件负责为容器配置网络（如创建虚拟网卡、分配 IP、设置路由规则等）。
  - 常见插件：`bridge`（默认网桥）、`host-local`（本地 IP 分配）、`loopback`（回环设备）等。
- **必要性**：
  若未安装 CNI 插件，Containerd 或 Kubernetes 创建的容器将无法联网。

1. **创建目录**（存储插件二进制文件）：

   ```shell
   $ mkdir -p /opt/cni/bin
   ```

2. **下载插件包**（示例为 amd64 架构），[点击前往 ↪](https://github.com/containernetworking/plugins/releases) — cni-plugins-linux-amd64-v1.7.1.tgz)

3. 通过 rz 指令将其上传至 root 根目录

4. 校验文件完整性

   ```shell
   $ sha256sum cni-plugins-linux-amd64-v1.7.1.tgz 
   ```

5. **解压到目标目录**

   ```shell
   $ tar Cxzvf /opt/cni/bin cni-plugins-linux-amd64-v1.7.1.tgz 
   ./
   ./dummy
   ./tap
   ./sbr
   ./bandwidth
   ./LICENSE
   ./host-device
   ./dhcp
   ./firewall
   ./loopback
   ./host-local
   ./static
   ./ipvlan
   ./vlan
   ./vrf
   ./bridge
   ./ptp
   ./portmap
   ./macvlan
   ./README.md
   ./tuning
   
   ```

6. 验证插件

   ```shell
   $ ls /opt/cni/bin  # 应显示插件文件列表
   ```

## 配置文件

生成默认配置文件：

```shell
$ mkdir -p /etc/containerd
$ containerd config default | tee /etc/containerd/config.toml
```

**配置加速镜像**

1）编辑/etc/containerd/config.toml文件

在`/etc/containerd/config.toml`文件中找到或添加`[plugins."io.containerd.grpc.v1.cri".registry]`部分，并在其中设置`config_path`指向存放镜像仓库配置的目录。例如：

```
[plugins.'io.containerd.cri.v1.images'.registry]
      config_path = '/etc/containerd/certs.d'
```

2）创建镜像仓库配置目录

如果上述目录不存在，需要手动创建它：

```shell
$ mkdir -p /etc/containerd/certs.d
```

3）为每个镜像仓库创建配置文件

获取阿里云加速器地址

- 登录 [阿里云容器镜像服务控制台 ↪](https://cr.console.aliyun.com/)
- 选择 **镜像工具** — **镜像加速器**

在`/etc/containerd/certs.d`目录下，为每个需要加速的镜像仓库创建一个子目录，并在其中创建`hosts.toml`文件，指定加速地址。例如，为`docker.io`配置加速：

```shell
$ mkdir -p /etc/containerd/certs.d/docker.io
```

配置阿里云镜像源

编辑 `/etc/containerd/certs.d/docker.io/hosts.toml`，内容如下：

```shell
$ vim /etc/containerd/certs.d/docker.io/hosts.toml
```

```shell
server = "https://docker.io"
[host."https://<your-aliyun-mirror>.mirror.aliyuncs.com"]
  capabilities = ["pull", "resolve"]
```

> **提示**：替换 `<your-aliyun-mirror>` 为你的阿里云镜像加速地址

完成上述配置后，需要重启Containerd服务以使配置生效：

```shell
$ systemctl restart containerd
$ systemctl status containerd
$ containerd --version # containerd 命令查看版本
$ ctr version # ctr 命令查看版本
$ ctr images pull --platform linux/arm64 docker.io/library/nginx:latest --hosts-dir=/etc/containerd/certs.d
```

# 镜像管理

# 容器管理





