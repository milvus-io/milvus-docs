---
id: configure-helm.md
label: Helm
related_key: configure
summary: Configure Milvus with Helm Charts.
title: Configure Milvus with Helm Charts
---

# Configure Milvus with Helm Charts

This topic describes how to configure Milvus components and its third-party dependencies with Helm Charts.

<div class="alert note">
In current release, all parameters take effect only after Milvus restarts.
</div>

## Configure Milvus via configuration file

You can configure Milvus with a configuration file `values.yaml`.

### Download a configuration file

[Download](https://raw.githubusercontent.com/zilliztech/milvus-helm/master/charts/milvus/values.yaml) `values.yaml` directly or with the following command.

```
$ wget https://raw.githubusercontent.com/milvus-io/milvus-helm/master/charts/milvus/values.yaml
```

### Modify the configuration file

Configure your Milvus instance to suit your application scenarios by adjusting corresponding parameters in `values.yaml`.

Specifically, search for `extraConfigFiles` in `values.yaml` and put your configurations in this section as follows:

```yaml
# Extra configs for milvus.yaml
# If set, this config will merge into milvus.yaml
# Please follow the config structure in the milvus.yaml
# at https://github.com/milvus-io/milvus/blob/master/configs/milvus.yaml
# Note: this config will be the top priority which will override the config
# in the image and helm chart.
extraConfigFiles:
  user.yaml: |+
    #    For example to set the graceful time for query nodes
    #    queryNodes:
    #      gracefulTime: 10
```

Check the following links for more information about each parameter.

Sorted by:

<div class="filter">
<a href="#component">Components or dependencies</a> <a href="#purpose">Configuration purposes</a> 

</div>

<div class="filter-component table-wrapper">

<table id="component">
<thead>
  <tr>
    <th>Dependencies</th>
    <th>Components</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>
        <ul>
            <li><a href="configure_etcd.md">etcd</a></li>
            <li><a href="configure_minio.md">MinIO or S3</a></li>
            <li><a href="configure_pulsar.md">Pulsar</a></li>
            <li><a href="configure_rocksmq.md">RocksMQ</a></li>
        </ul>
    </td>
    <td>
        <ul>
            <li><a href="configure_rootcoord.md">Root coord</a></li>
            <li><a href="configure_proxy.md">Proxy</a></li>
            <li><a href="configure_querycoord.md">Query coord</a></li>
            <li><a href="configure_querynode.md">Query node</a></li>
            <li><a href="configure_indexnode.md">Index node</a></li>
            <li><a href="configure_datacoord.md">Data coord</a></li>
            <li><a href="configure_datanode.md">Data node</a></li>
            <li><a href="configure_localstorage.md">Local storage</a></li>
            <li><a href="configure_log.md">Log</a></li>
            <li><a href="configure_msgchannel.md">Message channel</a></li>
            <li><a href="configure_common.md">Common</a></li>
            <li><a href="configure_gpu.md">GPU</a></li>
            <li><a href="configure_grpc.md">GRPC</a></li>
            <li><a href="configure_indexcoord.md">Index coord</a></li>
            <li><a href="configure_metastore.md">Metastore</a></li>
            <li><a href="configure_mq.md">Message Queue</a></li>
            <li><a href="configure_tikv.md">Tikv</a></li>
            <li><a href="configure_trace.md">Trace</a></li>
            <li><a href="configure_quotaandlimits.md">Quota and Limits</a></li>
        </ul>
    </td>
  </tr>
</tbody>
</table>

</div>

<div class="filter-purpose table-wrapper">

<table id="purpose">
<thead>
  <tr>
    <th>Purpose</th>
    <th>Parameters</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>Performance tuning</td>
    <td>
        <ul>
            <li><a href="configure_querynode.md#queryNodegracefulTime"><code>queryNode.gracefulTime</code></a></li>
            <li><a href="configure_rootcoord.md#rootCoordminSegmentSizeToEnableIndex"><code>rootCoord.minSegmentSizeToEnableIndex</code></a></li>
            <li><a href="configure_datacoord.md#dataCoordsegmentmaxSize"><code>dataCoord.segment.maxSize</code></a></li>
            <li><a href="configure_datacoord.md#dataCoordsegmentsealProportion"><code>dataCoord.segment.sealProportion</code></a></li>
            <li><a href="configure_datanode.md#dataNodeflushinsertBufSize"><code>dataNode.flush.insertBufSize</code></a></li>
            <li><a href="configure_querycoord.md#queryCoordautoHandoff"><code>queryCoord.autoHandoff</code></a></li>
            <li><a href="configure_querycoord.md#queryCoordautoBalance"><code>queryCoord.autoBalance</code></a></li>
            <li><a href="configure_localstorage.md#localStorageenabled"><code>localStorage.enabled</code></a></li>
        </ul>
    </td>
  </tr>
  <tr>
    <td>Data and meta</td>
    <td>
        <ul>
            <li><a href="configure_common.md#commonretentionDuration"><code>common.retentionDuration</code></a></li>
            <li><a href="configure_rocksmq.md#rocksmqretentionTimeInMinutes"><code>rocksmq.retentionTimeInMinutes</code></a></li>
            <li><a href="configure_datacoord.md#dataCoordenableCompaction"><code>dataCoord.enableCompaction</code></a></li>
            <li><a href="configure_datacoord.md#dataCoordenableGarbageCollection"><code>dataCoord.enableGarbageCollection</code></a></li>
            <li><a href="configure_datacoord.md#dataCoordgcdropTolerance"><code>dataCoord.gc.dropTolerance</code></a></li>
        </ul>
    </td>
  </tr>
  <tr>
    <td>Administration</td>
    <td>
        <ul>
            <li><a href="configure_log.md#loglevel"><code>log.level</code></a></li>
            <li><a href="configure_log.md#logfilerootPath"><code>log.file.rootPath</code></a></li>
            <li><a href="configure_log.md#logfilemaxAge"><code>log.file.maxAge</code></a></li>
            <li><a href="configure_minio.md#minioaccessKeyID"><code>minio.accessKeyID</code></a></li>
            <li><a href="configure_minio.md#miniosecretAccessKey"><code>minio.secretAccessKey</code></a></li>
        </ul>
    </td>
  </tr>
  <tr>
    <td>Quota and Limits</td>
    <td>
        <ul>
            <li><a href="configure_quotaandlimits.md#quotaAndLimitsddlenabled"><code>quotaAndLimits.ddl.enabled</code></a></li>
            <li><a href="configure_quotaandlimits.md#quotaAndLimitsddlcollectionRate"><code>quotaAndLimits.ddl.collectionRate</code></a></li>
            <li><a href="configure_quotaandlimits.md#quotaAndLimitsddlpartitionRate"><code>quotaAndLimits.ddl.partitionRate</code></a></li>
            <li><a href="configure_quotaandlimits.md#quotaAndLimitsindexRateenabled"><code>quotaAndLimits.indexRate.enabled</code></a></li>
            <li><a href="configure_quotaandlimits.md#quotaAndLimitsindexRatemax"><code>quotaAndLimits.indexRate.max</code></a></li>
            <li><a href="configure_quotaandlimits.md#quotaAndLimitsflushRateenabled"><code>quotaAndLimits.flushRate.enabled</code></a></li>
            <li><a href="configure_quotaandlimits.md#quotaAndLimitsflushmax"><code>quotaAndLimits.flush.max</code></a></li>
            <li><a href="configure_quotaandlimits.md#quotaAndLimitscompationenabled"><code>quotaAndLimits.compation.enabled</code></a></li>
            <li><a href="configure_quotaandlimits.md#quotaAndLimitscompactionmax"><code>quotaAndLimits.compaction.max</code></a></li>
            <li><a href="configure_quotaandlimits.md#quotaAndLimitsdmlenabled"><code>quotaAndLimits.dml.enabled</code></a></li>
            <li><a href="configure_quotaandlimits.md#quotaAndLimitsdmlinsertRatemax"><code>quotaAndLimits.dml.insertRate.max</code></a></li>
            <li><a href="configure_quotaandlimits.md#quotaAndLimitsdmldeleteRatemax"><code>quotaAndLimits.dml.deleteRate.max</code></a></li>
            <li><a href="configure_quotaandlimits.md#quotaAndLimitsdqlenabled"><code>quotaAndLimits.dql.enabled</code></a></li>
            <li><a href="configure_quotaandlimits.md#quotaAndLimitsdqlsearchRatemax"><code>quotaAndLimits.dql.searchRate.max</code></a></li>
            <li><a href="configure_quotaandlimits.md#quotaAndLimitsdqlqueryRatemax"><code>quotaAndLimits.dql.queryRate.max</code></a></li>
            <li><a href="configure_quotaandlimits.md#quotaAndLimitslimitWritingttProtectionenabled"><code>quotaAndLimits.limitWriting.ttProtection.enabled</code></a></li>
            <li><a href="configure_quotaandlimits.md#quotaAndLimitslimitWritingttProtectionmaxTimeTickDelay"><code>quotaAndLimits.limitWriting.ttProtection.maxTimeTickDelay</code></a></li>
            <li><a href="configure_quotaandlimits.md#quotaAndLimitslimitWritingmemProtectionenabled"><code>quotaAndLimits.limitWriting.memProtection.enabled</code></a></li>
            <li><a href="configure_quotaandlimits.md#quotaAndLimitslimitWritingmemProtectiondataNodeMemoryLowWaterLevel"><code>quotaAndLimits.limitWriting.memProtection.dataNodeMemoryLowWaterLevel</code></a></li>
            <li><a href="configure_quotaandlimits.md#quotaAndLimitslimitWritingmemProtectionqueryNodeMemoryLowWaterLevel"><code>quotaAndLimits.limitWriting.memProtection.queryNodeMemoryLowWaterLevel</code></a></li>
            <li><a href="configure_quotaandlimits.md#quotaAndLimitslimitWritingmemProtectiondataNodeMemoryHighWaterLevel"><code>quotaAndLimits.limitWriting.memProtection.dataNodeMemoryHighWaterLevel</code></a></li>
            <li><a href="configure_quotaandlimits.md#quotaAndLimitslimitWritingmemProtectionqueryNodeMemoryHighWaterLevel"><code>quotaAndLimits.limitWriting.memProtection.queryNodeMemoryHighWaterLevel</code></a></li>
            <li><a href="configure_quotaandlimits.md#quotaAndLimitslimitWritingdiskProtectionenabled"><code>quotaAndLimits.limitWriting.diskProtection.enabled</code></a></li>
            <li><a href="configure_quotaandlimits.md#quotaAndLimitslimitWritingdiskProtectiondiskQuota"><code>quotaAndLimits.limitWriting.diskProtection.diskQuota</code></a></li>
            <li><a href="configure_quotaandlimits.md#quotaAndLimitslimitWritingforceDeny"><code>quotaAndLimits.limitWriting.forceDeny</code></a></li>
            <li><a href="configure_quotaandlimits.md#quotaAndLimitslimitReadingqueueProtectionenabled"><code>quotaAndLimits.limitReading.queueProtection.enabled</code></a></li>
            <li><a href="configure_quotaandlimits.md#quotaAndLimitslimitReadingqueueProtectionnqInQueueThreshold"><code>quotaAndLimits.limitReading.queueProtection.nqInQueueThreshold</code></a></li>
            <li><a href="configure_quotaandlimits.md#quotaAndLimitslimitReadingqueueProtectionqueueLatencyThreshold"><code>quotaAndLimits.limitReading.queueProtection.queueLatencyThreshold</code></a></li>
            <li><a href="configure_quotaandlimits.md#quotaAndLimitslimitReadingresultProtectionenabled"><code>quotaAndLimits.limitReading.resultProtection.enabled</code></a></li>
            <li><a href="configure_quotaandlimits.md#quotaAndLimitslimitReadingresultProtectionmaxReadResultRate"><code>quotaAndLimits.limitReading.resultProtection.maxReadResultRate</code></a></li>
            <li><a href="configure_quotaandlimits.md#quotaAndLimitslimitReadingforceDeny"><code>quotaAndLimits.limitReading.forceDeny</code></a></li>
        </ul>
    </td>
  </tr>
</tbody>
</table>

</div>

For other parameters specifically to Kubernetes installation, See [Milvus Helm Chart Configuration](https://github.com/milvus-io/milvus-helm/tree/master/charts/milvus#configuration).

### Start Milvus

Having finished modifying the configuration file, you can then start Milvus with the file.

```
$ helm upgrade my-release milvus/milvus -f values.yaml
```

## Configure multiple Deployments and strict resource group isolation

Milvus Helm charts can split selected Milvus components into multiple Kubernetes Deployments. This is useful when you want to place different pods in different availability zones (AZs), attach different Kubernetes labels to each Deployment, or assign QueryNode and StreamingNode pods to static Milvus resource groups.

The following components support multiple deployment groups:

- `proxy.groups`
- `dataNode.groups`
- `queryNode.groups`
- `streamingNode.groups`

Each item in a `groups` list renders one Deployment. `mixCoordinator` always renders a single Deployment, but you can still configure `mixCoordinator.labels`, `mixCoordinator.extraEnv`, `mixCoordinator.nodeSelector`, `mixCoordinator.affinity`, `mixCoordinator.tolerations`, and `mixCoordinator.topologySpreadConstraints` for that Deployment.

If a component's `groups` list is empty, Helm keeps the original behavior and renders one Deployment for that component. The legacy `replicaResourceGroups` setting is still supported for compatibility, but do not mix it with `queryNode.groups` or `streamingNode.groups` in the same release. `replicaResourceGroups` renders resource-group-specific QueryNode and StreamingNode Deployments and also writes cluster-level load settings into the generated Milvus config, while `groups` leaves the Milvus load plan under your control.

The commonly used fields in a deployment group are:

```yaml
name: az1
replicas: 2
labels: {}
annotations: {}
extraEnv: []
nodeSelector: {}
affinity: {}
tolerations: []
topologySpreadConstraints: []
```

`labels` are Kubernetes Deployment and pod-template labels. They do not assign a Milvus resource group by themselves. To assign a QueryNode or StreamingNode to a Milvus resource group, set the `MILVUS_SERVER_LABEL_RESOURCE_GROUP` environment variable through `extraEnv`.

### Split Deployments by AZ

The following example splits Proxy and DataNode across two AZs. The group-level `replicas` field lets each AZ have a different number of pods.

```yaml
proxy:
  groups:
    - name: az1
      replicas: 2
      labels:
        topology.milvus.io/az: az1
      nodeSelector:
        topology.kubernetes.io/zone: us-east-1a
    - name: az2
      replicas: 1
      labels:
        topology.milvus.io/az: az2
      nodeSelector:
        topology.kubernetes.io/zone: us-east-1b

dataNode:
  groups:
    - name: az1
      replicas: 2
      labels:
        topology.milvus.io/az: az1
      nodeSelector:
        topology.kubernetes.io/zone: us-east-1a
    - name: az2
      replicas: 1
      labels:
        topology.milvus.io/az: az2
      nodeSelector:
        topology.kubernetes.io/zone: us-east-1b
```

### Split QueryNode and StreamingNode by resource group

For QueryNode and StreamingNode, use Helm deployment groups for the Kubernetes layout and use `MILVUS_SERVER_LABEL_RESOURCE_GROUP` for the Milvus resource group membership. This keeps the Kubernetes Deployment split independent from the Milvus resource group mechanism.

```yaml
queryNode:
  groups:
    - name: rg-blue-az1
      replicas: 2
      labels:
        topology.milvus.io/az: az1
        milvus.io/resource-group: rg-blue-a
      nodeSelector:
        topology.kubernetes.io/zone: us-east-1a
      extraEnv:
        - name: MILVUS_SERVER_LABEL_RESOURCE_GROUP
          value: rg-blue-a
    - name: rg-blue-az2
      replicas: 2
      labels:
        topology.milvus.io/az: az2
        milvus.io/resource-group: rg-blue-b
      nodeSelector:
        topology.kubernetes.io/zone: us-east-1b
      extraEnv:
        - name: MILVUS_SERVER_LABEL_RESOURCE_GROUP
          value: rg-blue-b

streamingNode:
  groups:
    - name: rg-blue-az1
      replicas: 1
      labels:
        topology.milvus.io/az: az1
        milvus.io/resource-group: rg-blue-a
      nodeSelector:
        topology.kubernetes.io/zone: us-east-1a
      extraEnv:
        - name: MILVUS_SERVER_LABEL_RESOURCE_GROUP
          value: rg-blue-a
    - name: rg-blue-az2
      replicas: 1
      labels:
        topology.milvus.io/az: az2
        milvus.io/resource-group: rg-blue-b
      nodeSelector:
        topology.kubernetes.io/zone: us-east-1b
      extraEnv:
        - name: MILVUS_SERVER_LABEL_RESOURCE_GROUP
          value: rg-blue-b
```

For strict resource group isolation, configure the Milvus load plan through dynamic configuration in etcd instead of `user.yaml`. The following commands assume that the Milvus root path is `by-dev`, which is the default for Helm installations. If your release uses a different root path, replace `by-dev` with your configured root path.

```bash
ETCDCTL_API=3 etcdctl --endpoints=http://<etcd-endpoint>:2379 put \
  by-dev/config/queryCoord.clusterLevelLoadReplicaNumber 2
ETCDCTL_API=3 etcdctl --endpoints=http://<etcd-endpoint>:2379 put \
  by-dev/config/queryCoord.clusterLevelLoadResourceGroups rg-blue-a,rg-blue-b
ETCDCTL_API=3 etcdctl --endpoints=http://<etcd-endpoint>:2379 put \
  by-dev/config/queryCoord.clusterLevelLoadForceOverrideUserReplicaMode true
ETCDCTL_API=3 etcdctl --endpoints=http://<etcd-endpoint>:2379 put \
  by-dev/config/streaming.primaryResourceGroup rg-blue-a
ETCDCTL_API=3 etcdctl --endpoints=http://<etcd-endpoint>:2379 put \
  by-dev/config/streaming.strictResourceGroupIsolation.enabled true
```

In this model, `queryCoord.clusterLevelLoadReplicaNumber` controls the number of collection load replicas, and `queryCoord.clusterLevelLoadResourceGroups` controls where those replicas are placed. The Helm group `replicas` field only controls the number of Kubernetes pods in that Deployment.

### Run a blue-green resource group switch

To switch from one set of resource groups to another, first deploy both the blue and green QueryNode and StreamingNode groups with Helm, then update the dynamic configuration in etcd.

```yaml
queryNode:
  groups:
    - name: blue-a
      replicas: 2
      extraEnv:
        - name: MILVUS_SERVER_LABEL_RESOURCE_GROUP
          value: rg-blue-a
    - name: blue-b
      replicas: 2
      extraEnv:
        - name: MILVUS_SERVER_LABEL_RESOURCE_GROUP
          value: rg-blue-b
    - name: green-a
      replicas: 2
      extraEnv:
        - name: MILVUS_SERVER_LABEL_RESOURCE_GROUP
          value: rg-green-a
    - name: green-b
      replicas: 2
      extraEnv:
        - name: MILVUS_SERVER_LABEL_RESOURCE_GROUP
          value: rg-green-b

streamingNode:
  groups:
    - name: blue-a
      replicas: 1
      extraEnv:
        - name: MILVUS_SERVER_LABEL_RESOURCE_GROUP
          value: rg-blue-a
    - name: blue-b
      replicas: 1
      extraEnv:
        - name: MILVUS_SERVER_LABEL_RESOURCE_GROUP
          value: rg-blue-b
    - name: green-a
      replicas: 1
      extraEnv:
        - name: MILVUS_SERVER_LABEL_RESOURCE_GROUP
          value: rg-green-a
    - name: green-b
      replicas: 1
      extraEnv:
        - name: MILVUS_SERVER_LABEL_RESOURCE_GROUP
          value: rg-green-b
```

Then move the Milvus load plan in phases:

```bash
# Blue: two loaded replicas on the current resource groups.
ETCDCTL_API=3 etcdctl --endpoints=http://<etcd-endpoint>:2379 put \
  by-dev/config/queryCoord.clusterLevelLoadReplicaNumber 2
ETCDCTL_API=3 etcdctl --endpoints=http://<etcd-endpoint>:2379 put \
  by-dev/config/queryCoord.clusterLevelLoadResourceGroups rg-blue-a,rg-blue-b
ETCDCTL_API=3 etcdctl --endpoints=http://<etcd-endpoint>:2379 put \
  by-dev/config/queryCoord.clusterLevelLoadForceOverrideUserReplicaMode true
ETCDCTL_API=3 etcdctl --endpoints=http://<etcd-endpoint>:2379 put \
  by-dev/config/streaming.primaryResourceGroup rg-blue-a

# Overlap: load replicas on both blue and green resource groups.
ETCDCTL_API=3 etcdctl --endpoints=http://<etcd-endpoint>:2379 put \
  by-dev/config/queryCoord.clusterLevelLoadReplicaNumber 4
ETCDCTL_API=3 etcdctl --endpoints=http://<etcd-endpoint>:2379 put \
  by-dev/config/queryCoord.clusterLevelLoadResourceGroups rg-blue-a,rg-blue-b,rg-green-a,rg-green-b

# Green: serve from the new resource groups.
ETCDCTL_API=3 etcdctl --endpoints=http://<etcd-endpoint>:2379 put \
  by-dev/config/streaming.primaryResourceGroup rg-green-a
ETCDCTL_API=3 etcdctl --endpoints=http://<etcd-endpoint>:2379 put \
  by-dev/config/queryCoord.clusterLevelLoadReplicaNumber 2
ETCDCTL_API=3 etcdctl --endpoints=http://<etcd-endpoint>:2379 put \
  by-dev/config/queryCoord.clusterLevelLoadResourceGroups rg-green-a,rg-green-b
```

After the new load plan becomes compliant, remove the blue QueryNode and StreamingNode deployment groups with another Helm upgrade.

```bash
curl http://<mixcoord-management-endpoint>/management/replica/loadconfig/compliance
```

## Configure Milvus via command line

Alternatively, you can upgrade Milvus configurations directly with the Helm command.

### Check the configurable parameters

Before upgrade, you can check the configurable parameters with Helm charts.

```
$ helm show values milvus/milvus
```

### Start Milvus

Configure and start Milvus by adding `--values` or `--set` in the command for upgrade.

```
# For instance, upgrade the Milvus cluster with compaction disabled
$ helm upgrade my-release milvus/milvus --set dataCoord.enableCompaction=false
```

## What's next

- If you want to learn how to monitor the Milvus services and create alerts:
  - Learn [Monitor Milvus with Prometheus Operator on Kubernetes](monitor.md)
  - Learn [Visualize Milvus Metrics in Grafana](visualize.md).

- If you are looking for instructions on how to allocate resources:
  - [Allocate Resources on Kubernetes](allocate.md#standalone)
