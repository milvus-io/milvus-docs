---
id: install_standalone-helm.md
label: 使用 Kubernetes 安装
order: 0
group: standalone
---
# 安装 Milvus 单机版
你可以使用 Docker Compose 或 Kubernetes 安装 Milvus 单机版。
你也可以[从源代码编译 Milvus](https://github.com/milvus-io/milvus/blob/master/INSTALL.md)。
{{tab}}


## 安装前提
- Kubernetes： 1.14.0 或以上。

- minikube：详见 [minikube 快速开始文档](https://kubernetes.io/docs/tasks/tools/install-minikube/)。

> 安装 minikube 时会自动安装虚拟机监控器（hypervisor）和命令行工具 Kubectl，帮助你从本地工作站管理 Kubernetes。

- Kubernetes 包管理工具 Helm: 3.0.0 或以上。详见 [Helm 官方文档](https://helm.sh/docs/)。

## 1.启动本地 Kubernetes 集群
```
$ minikube start
```

## 2. 启动 Milvus
> 使用 Kubernetes 包管理工具 Helm 能够简化本步骤。

#### 使用 Kubernetes 包管理工具 Helm 添加 Milvus chart 仓库：
```
$ helm repo add milvus https://milvus-io.github.io/milvus-helm/
```

#### 将 Milvus chart 更新至最新版本：
```
$ helm repo update
```

#### 安装 Milvus Helm chart：
设置发布命名（release name）以标记或追踪该 chart 部署。

<div class="alert note">
本教程使用 my-release 作为 release name。如需使用不同的 release name, 请在以下命令中修改相应的 release name。
</div>

#### 安装 Milvus 单机版：
```
$ helm install my-release milvus/milvus
```

> 详见 [Milvus Helm charts](https://artifacthub.io/packages/helm/milvus/milvus)。

*如果启动成功，Milvus pod 将在 `READY` 下显示 `1/1`：*

```
$ kubectl get pods
NAME                                               READY   STATUS      RESTARTS   AGE
my-release-etcd-0                                  1/1     Running     0          30s
my-release-milvus-standalone-54c4f88cb9-f84pf      1/1     Running     0          30s
my-release-minio-5564fbbddc-mz7f5                  1/1     Running     0          30s
```

## 3.连接 Milvus
打开新终端窗口，从你的本地端口转发至 Milvus 服务：
```
$ kubectl port-forward service/my-release-milvus 19530
Forwarding from 127.0.0.1:19530 -> 19530
```

## 4. 卸载 Milvus 实例
```
$ helm uninstall my-release
```

## 5. 停用集群
如需关闭 minikube 虚拟机但保留所有已创建资源，运行以下命令停用集群：
```
$ minikube stop
```
> 如需重新启动集群，请运行命令：

```
minikube start
```

## 6. 删除集群

如无需重启集群，运行以下命令删除 minikube 虚拟机及包括持久卷（persistent volume）在内的所有已创建资源：
```
minikube delete
```

> 如需留存日志，在删除集群前从每个 pod 的 `stderr` 中复制日志及相关资源。运行 `kubectl logs <podname>` 指令获取 pod 标准错误流。


