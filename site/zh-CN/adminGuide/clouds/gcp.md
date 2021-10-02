---
id: gcp.md
title: 使用 Kubernetes 在 GCP  上部署 Milvus 的指南
---

#  使用 Kubernetes 在 GCP 上部署 Milvus 的指南

本指南是在 Google Cloud Platform (GCP) 上部署 Milvus 集群的一组说明。 

## 在你开始之前
在开始之前，请确认您将在哪个 GCP 项目下工作。 如果您不确定要使用哪个项目，请联系您的 GCP 管理员并要求他们 [set one up](https://cloud.google.com/resource-manager/docs/creating-managing-projects) 为你. 本指南中使用了一个名为 **"milvus-testing-nonprod"** 的项目。 如果您的项目名称不同，则需要相应地改写命令。

Next, [install the GCP SDK](https://cloud.google.com/sdk/docs/quickstart#installing_the_latest_version) and confirm that you are properly authenticated. Install [kubectl](http://gcloud%20container%20clusters%20get-credentials%20hello-cluster/) and [helm](http://gcloud%20container%20clusters%20get-credentials%20hello-cluster/). Alternatively, you can use the [Google Cloud Shell](https://cloud.google.com/shell) from your browser, which has the GCP SDK, kubectl, and helm pre-installed. 

## Set up the Network
如果您有想要使用的现有虚拟私有云 (VPC) 网络，您可以直接继续 [create a firewall rule for Milvus](gcp.md#Create-a-Firewall-Rule-for-Milvus).

如果您没有现成的VPC网络或想新建一个VPC网络，请先新建一个VPC网络，然后再为Milvus创建防火墙规则。

### 创建新的 VPC 网络

打开您的 CLI 并创建一个新的 VPC。

<div class="alert note">
代替 <b>milvus-testing-nonprod</b> 使用您的项目名称.
</div>

```Apache
gcloud compute networks create milvus-network --project=milvus-testing-nonprod --subnet-mode=auto --mtu=1460 --bgp-routing-mode=regional
```

接下来，创建一组基本的防火墙规则以允许内部通信、ssh 连接、icmp 和 rdp 等流量。
```Apache
gcloud compute firewall-rules create milvus-network-allow-icmp --project=milvus-testing-nonprod --network=projects/milvus-testing-nonprod/global/networks/milvus-network --description=Allows\ ICMP\ connections\ from\ any\ source\ to\ any\ instance\ on\ the\ network. --direction=INGRESS --priority=65534 --source-ranges=0.0.0.0/0 --action=ALLOW --rules=icmp

gcloud compute firewall-rules create milvus-network-allow-internal --project=milvus-testing-nonprod --network=projects/milvus-testing-nonprod/global/networks/milvus-network --description=Allows\ connections\ from\ any\ source\ in\ the\ network\ IP\ range\ to\ any\ instance\ on\ the\ network\ using\ all\ protocols. --direction=INGRESS --priority=65534 --source-ranges=10.128.0.0/9 --action=ALLOW --rules=all

gcloud compute firewall-rules create milvus-network-allow-rdp --project=milvus-testing-nonprod --network=projects/milvus-testing-nonprod/global/networks/milvus-network --description=Allows\ RDP\ connections\ from\ any\ source\ to\ any\ instance\ on\ the\ network\ using\ port\ 3389. --direction=INGRESS --priority=65534 --source-ranges=0.0.0.0/0 --action=ALLOW --rules=tcp:3389

gcloud compute firewall-rules create milvus-network-allow-ssh --project=milvus-testing-nonprod --network=projects/milvus-testing-nonprod/global/networks/milvus-network --description=Allows\ TCP\ connections\ from\ any\ source\ to\ any\ instance\ on\ the\ network\ using\ port\ 22. --direction=INGRESS --priority=65534 --source-ranges=0.0.0.0/0 --action=ALLOW --rules=tcp:22
```

### 为 Milvus 创建防火墙规则 

创建防火墙规则允许外部进入端口 19530，这是 Milvus 使用的端口。
```Apache
gcloud compute --project=milvus-testing-nonprod firewall-rules create allow-milvus-in --description="Allow ingress traffic for Milvus on port 19530" --direction=INGRESS --priority=1000 --network=projects/milvus-testing-nonprod/global/networks/milvus-network --action=ALLOW --rules=tcp:19530 --source-ranges=0.0.0.0/0
```

## 使用 GKE 提供 Kubernetes 集群
我们使用 GKE Standard 来配置 Kubernetes 集群。 在本指南中，我们在区域中创建了一个具有 2 个节点的集群`us-west1-a`, 与机器类型 `e2-standard-4` 运行图像类型 `COS_CONTAINERD`.

<div class="alert note">
您可以更改上述选项以满足您的集群需求。
</div>

### 机器类型选择

在本指南中，我们使用机器类型 `e2-standard-4`, 它有 4 个 vCPU 和 16GB 内存，用于工作节点。 

<div class="alert note">
您可以选择不同的机器类型以更好地适应您的工作情况，但我们强烈建议工作节点都具有至少 16GB 的内存，以确保最低限度的稳定运行。
</div>

```Apache
gcloud beta container --project "milvus-testing-nonprod" clusters create "milvus-cluster-1" --zone "us-west1-a" --no-enable-basic-auth --cluster-version "1.20.8-gke.900" --release-channel "regular" --machine-type "e2-standard-4" --image-type "COS_CONTAINERD" --disk-type "pd-standard" --disk-size "100" --max-pods-per-node "110" --num-nodes "2" --enable-stackdriver-kubernetes --enable-ip-alias --network "projects/milvus-testing-nonprod/global/networks/milvus-network" --subnetwork "projects/milvus-testing-nonprod/regions/us-west1/subnetworks/milvus-network"
```

您的集群可能需要几分钟才能启动。 创建集群后，获取集群的身份验证凭据。
```Apache
gcloud container clusters get-credentials milvus-cluster-1
```

这将 **kubectl** 配置为使用集群。

## 使用 Helm 部署 Milvus

设置好集群后，我们现在可以部署 Milvus。 如果您在上一步中使用了不同的 shell，请再次获取凭据。
```Apache
gcloud container clusters get-credentials milvus-cluster-1
```

1. 添加 Milvus 图表存储库。
```Apache
helm repo add milvus https://milvus-io.github.io/milvus-helm/
```

2. 更新您的 Milvus 图表。
```Apache
helm repo update
```

3. 运行 helm 部署 Milvus。

<div class="alert note">
在本指南中，我们选择名称<code>my-release</code>, 但您可以更改名称。
</div>

```Thrift
helm install my-release milvus/milvus --set cluster.enabled=true --set service.type=LoadBalancer
```

等待几分钟让 Pod 启动，运行 <code>kubectl get services</code> 以检查服务。 如果服务成功启动，您可以看到列出的一组服务。

![GCP](../../../../assets/gcp.png)


<div class="alert note">
请注意负载均衡器的 <code>EXTERNAL-IP</code> 列下列出的 IP。 这是连接 Milvus 的 IP。
</div>

## 使用谷歌云存储

### 概述

Google Cloud Storage (GCS) 是等效于 AWS S3 存储的 Google Cloud Platform。
GCS 网关节点是 MinIO 服务器的替代运行方法，从客户端的角度来看，其行为相同，但使用相应的 GCS 连接 API 将所有连接转换并转发到 GCS。

### 如何使用

使用 GCS 网关节点需要设置许多变量。 一些变量已设置为适当的默认值，但其他变量必须由用户更改。
#### 秘密

MinIO GCS 网关节点需要一组有效的 GCP 服务帐户凭据才能连接到 GCS。 这些凭据必须存储在要分发的 Kubernetes 密钥中。 Kubernetes Secret 必须包含三种类型的数据：
- `accesskey`: MinIO access key; string literal.
- `secretkey`: MinIO secret key; string literal.
- `gcs_key.json`: GCP service account credentials; json file.

示例秘密创建：
```shell
$ kubectl create secret generic mysecret --from-literal=accesskey=minioadmin --from-literal=secretkey=minioadmin --from-file=gcs_key.json=/home/credentials.json
```

<div class="alert note">
如果您选择了默认 <code>minioadmin/minioadmin</code> 以外的 <code>accesskey</code> 和 <code>secretkey</code> 值，则需要更新 <code>minio.accessKey</code> > 和 <code>minio.secretKey</code> 元数据变量。
</div>


#### 元数据 

**必须由用户设置的元数据：**

- `minio.gcsgateway.enabled`: 必须设置为“true”才能启用操作。
  -  默认为假. 
- `minio.gcsgateway.projectId`: 服务帐号和存储分区对应的 GCP 项目 ID。
  - 默认未设置.
- `minio.existingSecret`: 先前定义的秘密的名称. 
  - 默认未设置.
- `externalGcs.bucketName`: 要使用的 GCS 存储桶的名称。 与 S3/MinIO 存储桶不同，GCS 存储桶必须**全局**唯一。 因此默认值是未设置的。
  - 默认未设置.

**应保留为默认值的元数据：**

- `minio.gcsgateway.replicas`: 用于 GCS 网关的副本节点数。 我们强烈建议您只使用一个，因为 MinIO 对更高的数字没有很好的支持。
  - 默认值为 1。
- `minio.gcsgateway.gcsKeyJson`: GCS 服务帐户访问凭据文件的路径。 您不应更改默认值。
  - 默认是 `/etc/credentials/gcs_key.json`.
- 您还应该继承所有普通的 MinIO 元数据变量。

示例头盔安装：
```shell
$ helm install my-release milvus/milvus --set cluster.enabled=true --set minio.existingSecret=mysecret --set minio.gcsgateway.enabled=true --set minio.gcsgateway.projectId=milvus-testing-nonprod --set externalGcs.bucketName=milvus-bucket-example
```


