# 在百度云上使用 CCE 部署 Milvus 集群

## 一、前提条件

- **百度云环境**：已注册[百度智能云账号](https://console.bce.baidu.com/agent/#/agent/account/bind~token=12966567a9e1280b8e7aed2f4fb6da1301e285d583aca84dbf786ee65d5d5f35&inviteType=agentUser&agentRank=0)，完成实名认证，拥有创建和管理资源的权限。
- **工具准备**：
  - 本地安装 kubectl 和 Helm。
  - 也可使用百度智能云控制台内置的 Cloud Shell，其预装了 kubectl 和 Helm 工具。
- **相关知识**：了解 Kubernetes 基础概念、Helm 包管理工具及 Milvus 向量数据库的基本使用。

## 二、配置百度云容器引擎（CCE）集群

### 步骤 1：通过百度云控制台创建 CCE 集群

1. 登录百度智能云控制台，在产品服务中找到并点击 **容器与微服务 > 容器引擎 CCE**。
2. 点击 **创建集群**，进入创建页面：

   **基础配置**：
   - 所属项目：选择或创建项目（用于资源管理分组）
   - 集群名称：自定义名称，如 `milvus-cce-cluster`
   - 地域：选择就近区域，如 华北-北京，需与后续 BOS 存储桶区域保持一致
   - 可用区：建议选择多个可用区，保障高可用性
   - 集群版本：建议选择最新的稳定版本，如 1.20.x

   **网络配置**：
   - 网络模式：选择 Kubenet，采用集群内虚拟网络，配置相对简单
   - VPC 网络：选择已有 VPC 或创建新的 VPC
   - 服务网段：建议使用 10.0.0.0/16，避免与现有网络冲突
   - Pod 网段：建议使用 172.16.0.0/16，避免与服务网段重叠
   - 安全组：建议创建专用的安全组，仅开放必要端口（如 22、443、19530、19121）

   **节点配置**：
   - 节点池类型：选择 虚拟机节点池
   - 实例规格：选择内存≥16GB 的实例，如 `bcc.gn8.2xlarge`，可根据实际数据量和负载调整
   - 节点数量：至少设置 2 个节点，用于生产环境建议根据流量预估扩容
   - 节点镜像：建议选择 CentOS 7.6 或 Ubuntu 18.04
   - 系统盘：建议配置 100GB 以上
   - 节点标签：建议添加 `milvus=true` 等标签，方便后续管理

   **高级配置**：
   - 集群组件：
     - 开启 CoreDNS
     - 开启 Metrics Server
     - 开启 Node Local DNS
   - 监控告警：
     - 开启集群监控
     - 配置节点监控
     - 设置告警规则
   - 日志配置：
     - 开启集群日志
     - 配置日志采集
   - 自动伸缩：
     - 根据需求配置节点自动伸缩
     - 设置伸缩策略

3. 确认配置无误后，点击 **立即创建**，等待集群创建完成，该过程通常需要 5-10 分钟。

### 步骤 2：连接到 CCE 集群

1. 在 CCE 集群列表中，找到刚创建的集群，点击 **连接信息**：
   - 选择 Kubeconfig 方式，下载 config 文件，或复制相关配置命令。

2. 在本地终端或 Cloud Shell 中执行以下操作（以复制命令为例）：

```bash
# 配置集群信息
kubectl config set-cluster <集群名称> --server=https://<集群Endpoint> --certificate-authority=data:<CA证书内容>

# 配置用户认证信息
kubectl config set-credentials <用户名> --token=<认证Token>

# 设置上下文
kubectl config set-context <上下文名称> --cluster=<集群名称> --user=<用户名>

# 切换到该上下文
kubectl config use-context <上下文名称>
```

3. 验证连接：
```bash
kubectl get nodes
```

若输出节点列表且状态为 Ready，则表示连接成功。

## 三、配置百度云对象存储（BOS）作为外部存储

### 步骤 1：创建 BOS 存储桶

1. 登录百度智能云控制台，进入 **存储 > 对象存储 BOS**。
2. 点击 **创建存储桶**：
   - 存储桶名称：自定义，如 `milvus-data`，名称需全局唯一
   - 所属地域：与 CCE 集群地域一致，如 华北-北京
   - 存储类别：选择 标准存储，适合频繁访问场景
   - 访问权限：选择 私有，保障数据安全
3. 点击 **确定**，完成存储桶创建。

### 步骤 2：获取 BOS 访问密钥

1. 在百度智能云控制台，点击 **用户中心 > 访问密钥**。
2. 若已有密钥，记录 Access Key ID 和 Secret Access Key；若无，则点击 **创建密钥** 生成并妥善保存。

## 四、编写 Milvus 配置文件（values.yaml）

创建 `values.yaml` 文件，内容如下（需替换占位符）：

```yaml
cluster:
  enabled: true

service:
  type: LoadBalancer  # 使用负载均衡器暴露服务

extraConfigFiles:
  user.yaml: |+
    common:
      storageType: remote  # 使用外部存储

minio:
  enabled: false  # 禁用内置MinIO，使用BOS

externalS3:
  enabled: true
  host: bos.<地域>.baidubce.com  # 替换为实际地域，如 bos.bj.baidubce.com
  port: 443  # HTTPS端口
  bucketName: <存储桶名称>  # 如 milvus-data
  cloudProvider: bos  # 指定云服务商为BOS
  useSSL: true  # 启用HTTPS
  accessKey: "<Access Key ID>"  # 步骤3获取的Access Key ID
  secretKey: "<Secret Access Key>"  # 步骤3获取的Secret Access Key
```

## 五、部署 Milvus 集群

### 步骤 1：添加 Milvus Helm 仓库

```bash
helm repo add milvus https://zilliztech.github.io/milvus-helm/
helm repo update
```

### 步骤 2：通过 Helm 安装 Milvus

```bash
helm install -f values.yaml <释放名称> milvus/milvus
```

示例（释放名称设为 milvus-release）：
```bash
helm install -f values.yaml milvus-release milvus/milvus
```

## 六、验证部署

### 步骤 1：检查 Pod 状态

```bash
kubectl get pods -l app.kubernetes.io/instance=milvus-release
```

确保所有 Pod 状态为 Running，若存在 ContainerCreating 或 Error 状态，可通过 `kubectl describe pod <Pod名称>` 查看日志排查问题。

### 步骤 2：获取外部访问 IP

```bash
kubectl get services milvus-release-milvus -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
```

记录输出的外部 IP 地址。

### 步骤 3：测试连接

使用 Milvus SDK 编写测试代码（以 Python 为例）：

```python
from pymilvus import connections

connections.connect(
    alias="default",
    host="<外部IP>",
    port="19530"
)
```

运行代码，若未报错且能成功连接，则 Milvus 部署完成。

## 七、清理资源（可选）

如需删除集群和存储：

```bash
# 删除Milvus部署
helm uninstall milvus-release

# 删除CCE集群
# 在百度智能云控制台CCE页面，找到集群并点击删除

# 删除BOS存储桶
# 在百度智能云控制台BOS页面，找到存储桶并点击删除（删除前请确认数据已备份，操作不可逆）
```

## 注意事项

- **资源规划**：根据数据量和访问负载合理规划 CCE 节点规格和数量，BOS 存储桶可按需选择存储类型和容量。
- **安全配置**：通过百度智能云的安全组（SG）功能，限制对 Milvus 服务端口（19530、19121）的访问，仅开放给可信 IP。
- **监控告警**：开启 CCE 集群监控和 BOS 存储监控，设置告警策略，及时发现和处理异常。
- **版本兼容**：部署前确认 Milvus Helm Chart 版本与 Kubernetes、百度云 CCE 版本的兼容性。