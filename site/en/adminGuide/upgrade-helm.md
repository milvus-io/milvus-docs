---
id: upgrade-helm.md
label: Helm
order: 1
group: upgrade.md
summary: Learn how to upgrade Milvus v2.1 to v2.2 with Helm.
---

{{tab}}

# Upgrade Milvus with Helm
A major change in Milvus 2.2 is the meta structure of segment indexes. This topic describes how to use Helm to migrate the meta and upgrade Milvus from v2.1.x to v2.2.0. We provide you with a script so that you can safely migrate your meta data.


<div class="alert note">
This script only applies to Milvus installed on a K8s cluster. Rollback to the previous version with the <code>rollback</code> operation first if an error occurs during an upgrade.
</div>

The following table lists the operations you can do for meta migration.

| Parameters   | Description                                                      | Default value                    | Required                |
| ------------ | ---------------------------------------------------------------- | ---------------------------- | ----------------------- |
| `i`          | The Milvus instance name.                                 | `None`                         | True                    |
| `n`          | The namespace that Milvus is installed in.                | `default`                      | False                   |
| `s`          | The source Milvus version.                                | `None`                         | True                    |
| `t`          | The target Milvus version.                               | `None`                         | True                    |
| `r`          | The root path of Milvus meta.                             | `by-dev`                       | False                   |
| `w`          | The new Milvus image tag.                                 | `milvusdb/milvus:v2.2.0`       | False                   |
| `m`          | The meta migration image tag.                             | `harbor.milvus.io/milvus/meta-migration:20221025-e54b6181b`       | False                   |
| `o`          | The meta migration operation.                             | `migrate`                      | False                   |
| `d`          | Whether to delete migration pod after the migration is completed.          | `false`                        | False                   |

## Migrate meta

1. Download the migration script.
2. Stop the Milvus components. Any live session in the Milvus etcd can cause the migration to fail.
3. Create a backup for Milvus meta.
4. Migrate the Milvus meta.
5. Start Milvus components with a new image.

## Upgrade Milvus from v2.1.x to v2.2.0

1. Specify Milvus instance name, source Milvus version, and target Milvus version.

```
./migrate.sh -i my-release -s 2.1.1 -t 2.2.0
```

2. Specify namespace with `-n` if your Milvus is not installed in the default K8s namespace.

```
./migrate.sh -i my-release -n milvus -s 2.1.1 -t 2.2.0
```

3. Specify rootpath with `-r` if your Milvus is installed with the custom `rootpath`.

```
./migrate.sh -i my-release -n milvus -s 2.1.1 -t 2.2.0 -r by-dev
```

4. Specify the image tag with `-w` if your Milvus is installed with custom `image`.

```
./migrate.sh -i my-release -n milvus -s 2.1.1 -t 2.2.0 -r by-dev -w milvusdb/milvus:master-20221016-15878781
```

5. Set `-d true` if you want to automatically remove the migration pod after the migration is completed.

```
./migrate.sh -i my-release -n milvus -s 2.1.1 -t 2.2.0 -w milvusdb/milvus:master-20221016-15878781 -d true
```

6. Rollback and migrate again if the migration fails.

```
./migrate.sh -i my-release -n milvus -s 2.1.1 -t 2.2.0 -r by-dev -o rollback -w <milvus-2-1-1-image>
./migrate.sh -i my-release -n milvus -s 2.1.1 -t 2.2.0 -r by-dev -o migrate -w <milvus-2-2-0-image>
```

## What's next
- You might also want to learn how to:
  - [Scale a Milvus cluster](scaleout.md)
- If you are ready to deploy your cluster on clouds:
  - Learn how to [Deploy Milvus on AWS with Terraform and Ansible](aws.md)
  - Learn how to [Deploy Milvus on Amazon EKS with Terraform](eks.md)
  - Learn how to [Deploy Milvus Cluster on GCP with Kubernetes](gcp.md)
  - Learn how to [Deploy Milvus on Microsoft Azure With Kubernetes](azure.md)
