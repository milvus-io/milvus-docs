---
id: upgrade_milvus_cluster-docker.md
label: Docker Compose
order: 2
group: upgrade_milvus_cluster-operator.md
related_key: upgrade Milvus Cluster
summary: Learn how to upgrade Milvus cluster with Docker Compose.
---

{{tab}}

# Upgrade Milvus Cluster with Docker Compose

A major change in Milvus 2.2 is the metadata structure of segment indexes. This topic describes how to use Docker Compose upgrade Milvus from v2.1.x to v2.2.x.

In normal cases, you can upgrade Milvus as follows and a certain downtime is introduced:

```shell
// Run the following only after update the milvus image tag in the docker-compose.yaml
docker-compose down
docker-compose up -d
```

However, you need to [migrate the metadata](#Migrate-the-metadata) before any upgrade from Milvus v2.1.x to the latest, or you can [conduct a rolling upgrade](#Conduct-a-rolling-upgrade) to reduce possible downtime to the minimum.

## Migrate the metadata

1. Stop all Milvus components.

```
docker stop <milvus-component-docker-container-name>
```

2. Prepare the configuration file `migrate.yaml` for meta migration.

```
# migration.yaml
cmd:
  # Option: run/backup/rollback
  type: run
  runWithBackup: true
config:
  sourceVersion: 2.1.4   # Specify your milvus version
  targetVersion: {{var.milvus_release_version}}
  backupFilePath: /tmp/migration.bak
metastore:
  type: etcd
etcd:
  endpoints:
    - milvus-etcd:2379  # Use the etcd container name
  rootPath: by-dev # The root path where data is stored in etcd
  metaSubPath: meta
  kvSubPath: kv
```

3. Run the migration container.

```
# Suppose your docker-compose run with the default milvus network,
# and you put migration.yaml in the same directory with docker-compose.yaml.
docker run --rm -it --network milvus -v $(pwd)/migration.yaml:/milvus/configs/migration.yaml milvus/meta-migration:v2.2.0 /milvus/bin/meta-migration -config=/milvus/configs/migration.yaml
```

4. Start Milvus components again with the new Milvus image.

```
Update the milvus image tag in the docker-compose.yaml
docker-compose down
docker-compose up -d
```

## Conduct a rolling upgrade

Since Milvus 2.2.3, you can configure Milvus coordinators to work in active-standby mode and enable the rolling upgrade feature for them, so that Milvus can respond to incoming requests during the coordinator upgrades. In previous releases, coordinators are to be removed and then created during an upgrade, which may introduce certain downtime of the service.

Rolling upgrades requires coordinators to work in active-standby mode. You can use [the script](https://raw.githubusercontent.com/milvus-io/milvus/master/deployments/upgrade/rollingUpdate.sh) we provide to configure the coordinators to work in active-standby mode and start the rolling upgrade.

Based on the rolling update capabilities provided by Kubernetes, the above script enforces an ordered update of the deployments according to their dependencies. In addition, Milvus implements a mechanism to ensure that its components remain compatible with those depending on them during the upgrade, significantly reducing potential service downtime.

The script applies only to the upgrade of Milvus installed with Helm. The following table lists the command flags available in the scripts.

| Parameters   | Description                                               | Default value                    | Required                |
| ------------ | ----------------------------------------------------------| -------------------------------- | ----------------------- |
| `i`          | Milvus instance name                                      | `None`                           | True                    |
| `n`          | Namespace that Milvus is installed in                     | `default`                        | False                   |
| `t`          | Target Milvus version                                     | `None`                           | True                    |
| `w`          | New Milvus image tag                                      | `milvusdb/milvus:v{{var.milvus_release_version}}`         | True                    |
| `o`          | Operation                                                 | `update`                         | False                   |

Once you have ensured that all deployments in your Milvus instance are in their normal status. You can run the following command to upgrade the Milvus instance to {{var.milvus_release_version}}.

```shell
sh rollingUpdate.sh -n default -i my-release -o update -t {{var.milvus_release_version}} -w 'milvusdb/milvus:v{{var.milvus_release_version}}'
```

<div class="alert note">

1. The script hard-codes the upgrade order of the deployments and cannot be changed.
2. The script uses `kubectl patch` to update the deployments and `kubectl rollout status` to watch their status.
3. The script uses `kubectl patch` to update the `app.kubernetes.io/version` label of the deployments to the one specified after the `-t` flag in the command.

</div>

## What's next
- You might also want to learn how to:
  - [Scale a Milvus cluster](scaleout.md)
- If you are ready to deploy your cluster on clouds:
  - Learn how to [Deploy Milvus on AWS with Terraform and Ansible](aws.md)
  - Learn how to [Deploy Milvus on Amazon EKS with Terraform](eks.md)
  - Learn how to [Deploy Milvus Cluster on GCP with Kubernetes](gcp.md)
  - Learn how to [Deploy Milvus on Microsoft Azure With Kubernetes](azure.md)
