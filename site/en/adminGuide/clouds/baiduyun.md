# Deploying Milvus Cluster on Baidu Cloud CCE

## Prerequisites

- **Baidu Cloud Environment**: Registered Baidu Cloud account with real-name verification and resource management permissions.
- **Tools Required**:
  - Local installation of kubectl and Helm.
  - Alternatively, use Baidu Cloud Console's built-in Cloud Shell, which comes pre-installed with kubectl and Helm tools.
- **Knowledge Required**: Basic understanding of Kubernetes concepts, Helm package management, and Milvus vector database usage.

## Configure Baidu Cloud Container Engine (CCE) Cluster

### Step 1: Create CCE Cluster via Baidu Cloud Console

1. Log in to Baidu Cloud Console, navigate to **Container & Microservices > Container Engine CCE**.
2. Click **Create Cluster** to enter the creation page:

   **Basic Configuration**:
   - Project: Select or create a project (for resource management grouping)
   - Cluster Name: Custom name, e.g., `milvus-cce-cluster`
   - Region: Choose a nearby region, e.g., North China-Beijing, must match the BOS bucket region
   - Availability Zones: Recommend selecting multiple zones for high availability
   - Cluster Version: Recommend selecting the latest stable version, e.g., 1.20.x

   **Network Configuration**:
   - Network Mode: Select Kubenet for simple cluster virtual network configuration
   - VPC Network: Select existing VPC or create a new one
   - Service CIDR: Recommend using 10.0.0.0/16, avoid conflicts with existing networks
   - Pod CIDR: Recommend using 172.16.0.0/16, avoid overlapping with service CIDR
   - Security Group: Recommend creating a dedicated security group, only open necessary ports (e.g., 22, 443, 19530, 19121)

   **Node Configuration**:
   - Node Pool Type: Select Virtual Machine Node Pool
   - Instance Type: Select instances with ≥16GB memory, e.g., `bcc.gn8.2xlarge`, adjust based on actual data volume and load
   - Node Count: Minimum 2 nodes, for production environment recommend scaling based on traffic estimation
   - Node Image: Recommend CentOS 7.6 or Ubuntu 18.04
   - System Disk: Recommend configuring 100GB or more
   - Node Labels: Recommend adding labels like `milvus=true` for easier management

   **Advanced Configuration**:
   - Cluster Components:
     - Enable CoreDNS
     - Enable Metrics Server
     - Enable Node Local DNS
   - Monitoring & Alerting:
     - Enable cluster monitoring
     - Configure node monitoring
     - Set up alert rules
   - Logging Configuration:
     - Enable cluster logging
     - Configure log collection
   - Auto Scaling:
     - Configure node auto-scaling based on needs
     - Set scaling policies

3. After confirming the configuration, click **Create Now** and wait for cluster creation to complete, which typically takes 5-10 minutes.

### Step 2: Connect to CCE Cluster

1. In the CCE cluster list, find the newly created cluster and click **Connection Information**:
   - Choose Kubeconfig method, download config file, or copy configuration commands.

2. Execute the following operations in local terminal or Cloud Shell (using copied commands as example):

```bash
# Configure cluster information
kubectl config set-cluster <cluster-name> --server=https://<cluster-endpoint> --certificate-authority=data:<CA-certificate-content>

# Configure user authentication
kubectl config set-credentials <username> --token=<authentication-token>

# Set context
kubectl config set-context <context-name> --cluster=<cluster-name> --user=<username>

# Switch to the context
kubectl config use-context <context-name>
```

3. Verify connection:
```bash
kubectl get nodes
```

If the node list is displayed and status is Ready, the connection is successful.

## Configure Baidu Cloud Object Storage (BOS) as External Storage

### Step 1: Create BOS Bucket

1. Log in to Baidu Cloud Console, navigate to **Storage > Object Storage BOS**.
2. Click **Create Bucket**:
   - Bucket Name: Custom name, e.g., `milvus-data`, must be globally unique
   - Region: Must match CCE cluster region, e.g., North China-Beijing
   - Storage Class: Select Standard Storage, suitable for frequent access scenarios
   - Access Permission: Select Private for data security
3. Click **Confirm** to complete bucket creation.

### Step 2: Get BOS Access Keys

1. In Baidu Cloud Console, click **User Center > Access Keys**.
2. If you have existing keys, record the Access Key ID and Secret Access Key; if not, click **Create Key** to generate and securely save them.

## Create Milvus Configuration File (values.yaml)

Create a `values.yaml` file with the following content (replace placeholders):

```yaml
cluster:
  enabled: true

service:
  type: LoadBalancer  # Use load balancer to expose service

extraConfigFiles:
  user.yaml: |+
    common:
      storageType: remote  # Use external storage

minio:
  enabled: false  # Disable built-in MinIO, use BOS

externalS3:
  enabled: true
  host: bos.<region>.baidubce.com  # Replace with actual region, e.g., bos.bj.baidubce.com
  port: 443  # HTTPS port
  bucketName: <bucket-name>  # e.g., milvus-data
  cloudProvider: bos  # Specify cloud provider as BOS
  useSSL: true  # Enable HTTPS
  accessKey: "<Access Key ID>"  # Access Key ID from Step 3
  secretKey: "<Secret Access Key>"  # Secret Access Key from Step 3
```

## Deploy Milvus Cluster

### Step 1: Add Milvus Helm Repository

```bash
helm repo add milvus https://zilliztech.github.io/milvus-helm/
helm repo update
```

### Step 2: Install Milvus via Helm

```bash
helm install -f values.yaml <release-name> milvus/milvus
```

Example (release name set as milvus-release):
```bash
helm install -f values.yaml milvus-release milvus/milvus
```

## Verify Deployment

### Step 1: Check Pod Status

```bash
kubectl get pods -l app.kubernetes.io/instance=milvus-release
```

Ensure all pods are in Running state. If any pods are in ContainerCreating or Error state, check logs using `kubectl describe pod <pod-name>`.

### Step 2: Get External Access IP

```bash
kubectl get services milvus-release-milvus -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
```

Record the output external IP address.

### Step 3: Test Connection

Write test code using Milvus SDK (Python example):

```python
from pymilvus import connections

connections.connect(
    alias="default",
    host="<external-ip>",
    port="19530"
)
```

Run the code. If no errors occur and connection is successful, Milvus deployment is complete.

## Clean Up Resources (Optional)

To delete cluster and storage:

```bash
# Delete Milvus deployment
helm uninstall milvus-release

# Delete CCE cluster
# In Baidu Cloud Console CCE page, find the cluster and click delete

# Delete BOS bucket
# In Baidu Cloud Console BOS page, find the bucket and click delete (ensure data is backed up before deletion, operation is irreversible)
```

## Notes

- **Resource Planning**: Plan CCE node specifications and count based on data volume and access load, BOS bucket can be configured with storage type and capacity as needed.
- **Security Configuration**: Use Baidu Cloud Security Group (SG) to restrict access to Milvus service ports (19530, 19121), only open to trusted IPs.
- **Monitoring & Alerting**: Enable CCE cluster monitoring and BOS storage monitoring, set up alert policies to detect and handle anomalies promptly.
- **Version Compatibility**: Verify compatibility between Milvus Helm Chart version and Kubernetes, Baidu Cloud CCE versions before deployment. 