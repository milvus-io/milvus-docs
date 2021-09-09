---
id: install_standalone-helm.md
label: 使用 Kubernetes 安装
order: 1
group: standalone
---
# 安装 Milvus 单机版

你可以使用 Docker Compose 或 Kubernetes 安装 Milvus 单机版。


你也可以[从源代码编译 Milvus](https://github.com/milvus-io/milvus#to-start-developing-milvus)。

<div class="alert note">
Docker Compose 部署方式只用作测试使用，不能用于生产环境。
</div>

{{tab}}


## 1.启动本地 Kubernetes 集群
```
$ minikube start
```

## 2. 启动 Milvus
<div class="alert note">
使用 Kubernetes 包管理工具 Helm 能够简化本步骤。
</div>

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
本教程使用 <code> my-release</code> 作为 release name。如需使用不同的 release name, 请在以下命令中修改相应的 release name。
</div>

#### 安装 Milvus 单机版：
```
$ helm install my-release milvus/milvus
```
<div class="alert note">
详见 <a href="https://artifacthub.io/packages/helm/milvus/milvus">Milvus Helm charts</a>。
</div>

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
<div class="alert note">
如需重新启动集群，请运行命令：<code>minikube start</code>
</div>


## 6. 删除集群

如无需重启集群，运行以下命令删除 minikube 虚拟机及包括持久卷（persistent volume）在内的所有已创建资源：
```
minikube delete
```
<div class="alert note">
如需留存日志，在删除集群前从每个 pod 的 <code>stderr</code> 中复制日志及相关资源。运行 <code>kubectl logs (podname)</code> 指令获取 pod 标准错误流。
</div>


</br>

<div class="alert note">
阅读 <a href="upgrade.md">升级指南 2.0</a> 了解如何升级 Milvus 2.0 版本。
</div>
