---
id: configure_operator.md
title: Configure Milvus with Milvus Operator
related_key: Milvus Operator
summary: Learn how to configure Milvus with Milvus Operator.
---

# Configure Milvus with Milvus Operator

In production environment, you need to allocate resources to the Milvus cluster based on machine type and workload. You can configure during deployment or update the configurations while the cluster is running.

This topic introduces how to configure a Milvus cluster when you install it with Milvus Operator.

This topic assumes that you have deployed Milvus Operator. See [Deploy Milvus Operator](install_cluster-milvusoperator.md) for more information.

Configuring a Milvus cluster with Milvus Operator includes:
- Global resource configurations
- Private resource configurations

<div class="alert note">
Private resource configurations will overwrite global resource configurations. If you configure the resources globally and specify the private resource of a certain component at the same time, the component will prioritize and respond to the private configurations first.
</div>

## Configure global resources

When using Milvus Operator to start a Milvus cluster, you need to specify a configuration file. The example here uses the default configuration file.

```yaml
kubectl apply -f https://raw.githubusercontent.com/milvus-io/milvus-operator/main/config/samples/milvus_cluster_default.yaml
```

The details of the configuration file is as follows:

```yaml
apiVersion: milvus.io/v1beta1
kind: Milvus
metadata:
  name: my-release
  labels:
    app: milvus
spec:
  mode: cluster
  dependencies: {}
  components: {}
  config: {}
```

The field `spec.components` includes both the global and private resource configuration of all Milvus components. The following are four commonly used fields to configure global resource. 
- `image`: The Milvus docker image used.
- `resources`: The compute resources allocated to each component.
- `tolerations` and `nodeSelector`: The scheduling rules of each Milvus component in the K8s cluster. See [tolerations](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/) and [nodeSelector](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/) for more information.
- `env`: The environment variables. 

If you want to configure more fields, see documentation [here](https://pkg.go.dev/github.com/milvus-io/milvus-operator/apis/milvus.io/v1beta1#ComponentSpec).

To configure global resource for Milvus cluster, create a `milvuscluster_resource.yaml` file. 

### Example

The following example configures global resource for a Milvus cluster.

```
apiVersion: milvus.io/v1beta1
kind: Milvus
metadata:
  name: my-release
  labels:
    app: milvus
spec:
  mode: cluster
  components:
    image: milvusdb/milvus:v2.1.0
    nodeSelector: {}
    tolerations: {}
    env: {}
    resources:
      limits:
        cpu: '4'
        memory: 8Gi
      requests:
        cpu: 200m
        memory: 512Mi
```

Run the following command to apply new configurations:

```
kubectl apply -f milvuscluster_resource.yaml
```

<div class="alert note">
Cluster resources will be updated according to the configuration file if there is a Milvus cluster named <code>my-release</code> in the K8s cluster. Otherwise, a new Milvus cluster will be created.
</div>

## Configure private resources

Originally in Milvus 2.0, a Milvus cluster includes eight components: proxy, root coord, index coord, data coord, query coord, index node, data node, and query node. However, a new component, mix coord, is released along with Milvus 2.1.0. Mix coord includes all coordinator components. Therefore, starting a mix coord means that you do not need to install and start other coordinators including root coord, index coord, data coord, and query coord.

Common fields used to configure each component include:
- `replica`: The number of replicas of each component.
- `port`: The listen port number of each component.
- The four commonly used fields in global resource configuration: `image`, `env`, `nodeSelector`, `tolerations`, `resources` (see above). For more configurable fields, click on each component in [this documentation](https://pkg.go.dev/github.com/milvus-io/milvus-operator/apis/milvus.io/v1beta1#MilvusComponents).

<div class="alert note">
In addition, when configuring proxy, there is an extra field called `serviceType`. This field defines the type of service Milvus provides in the K8s cluster.
</div>

To configure resources for a specific component, add the component name in the field under `spec.componets` first and then configure its private resources.

### Example

The example below configures the replicas and compute resources of proxy and datanode in the `milvuscluster.yaml` file.

```
apiVersion: milvus.io/v1beta1
kind: Milvus
metadata:
  name: my-release
  labels:
    app: milvus
spec:
  mode: cluster
  components:
    image: milvusdb/milvus:v2.1.0
    resources:
      limits:
        cpu: '4'
        memory: 8Gi
      requests:
        cpu: 200m
        memory: 512Mi
    rootCoord: 
      replicas: 1
      port: 8080
      resources:
        limits:
          cpu: '6'
          memory: '10Gi'
    dataCoord: {}
    queryCoord: {}
    indexCoord: {}
    dataNode: {}
    indexNode: {}
    queryNode: {}
    proxy:
      replicas: 1
      serviceType: ClusterIP
      resources:
        limits:
          cpu: '2'
          memory: 4Gi
        requests:
          cpu: 100m
          memory: 128Mi
  config: {}
  dependencies: {}
```

<div class="alert note">
This example configures not only global resources but also private compute resources for root coord and proxy. When using this configuration file to start a Milvus cluster, the private resources configurations will be applied to root coord and proxy, while the rest of the components will follow the global resource configuration.
</div>

Run the following command to apply new configurations:

```
kubectl apply -f milvuscluster.yaml
```


## What's next

- Learn how to manage the following Milvus dependencies with Milvus Operator:
  - [Configure Object Storage with Milvus Operator](object_storage_operator.md)
  - [Configure Meta Storage with Milvus Operator](meta_storage_operator.md)
  - [Configure Message Storage with Milvus Operator](message_storage_operator.md)




