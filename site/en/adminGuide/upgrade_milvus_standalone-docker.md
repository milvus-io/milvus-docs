---
id: upgrade_milvus_standalone-docker.md
label: Docker Compose
order: 1
group: upgrade_milvus_standalone-operator.md
related_key: upgrade Milvus Standalone
summary: Learn how to upgrade Milvus standalone with Docker Compose.
title: Upgrade Milvus Standalone with Docker Compose
---

{{tab}}

# Upgrade Milvus Standalone with Docker Compose

This guide describes how to upgrade your Milvus standalone deployment from v2.5.x to v{{var.milvus_release_version}} using Docker Compose.

## Before you start

### What's new in v{{var.milvus_release_version}}

Upgrading from Milvus 2.5.x to {{var.milvus_release_version}} involves significant architectural changes:

- **New components**: Introduction of Streaming Node for enhanced data processing
- **Component optimizations**: Enhanced performance and streamlined architecture

<div class="alert note">
This upgrade is <strong>irreversible</strong>. You cannot roll back to a previous version once the upgrade is completed. For more information on architecture changes, refer to <a href="architecture_overview.md">Milvus Architecture Overview</a>.
</div>

### Requirements

**System requirements:**
- Docker and Docker Compose installed
- Milvus standalone deployed via Docker Compose

**Compatibility requirements:**
- Milvus v2.6.0-rc1 is **not compatible** with v{{var.milvus_release_version}}. Direct upgrades from release candidates are not supported.
- If you are currently running v2.6.0-rc1 and need to preserve your data, please refer to [this community guide](https://github.com/milvus-io/milvus/issues/43538#issuecomment-3112808997) for migration assistance.
- You **must** upgrade to v2.5.16 before upgrading to v{{var.milvus_release_version}}.

<div class="alter note">

Due to security concerns, Milvus upgrades its MinIO to RELEASE.2023-03-20T20-16-18Z with the release of v2.2.5. Before any upgrades from previous Milvus Standalone releases installed using Docker Compose, you should create a Single-Node Single-Drive MinIO deployment and migrate existing MinIO settings and content to the new deployment. For details, refer to [this guide](https://min.io/docs/minio/linux/operations/install-deploy-manage/migrate-fs-gateway.html#id2).

</div>

## Upgrade process

### Step 1: Download updated Docker Compose files

Before upgrading, download the latest Docker Compose configuration files:

```bash
# Download the latest docker-compose.yaml
wget https://github.com/milvus-io/milvus/releases/download/v{{var.milvus_release_tag}}/milvus-standalone-docker-compose.yml -O docker-compose.yaml
```

<div class="alert note">
Always download the latest configuration files to ensure compatibility with the new version and access to new features.
</div>

### Step 2: Upgrade to v2.5.16

<div class="alert-note">

Skip this step if your standalone deployment is already running v2.5.16 or higher.

</div>

1. Update the Milvus image tag in your `docker-compose.yaml` to v2.5.16:

    ```yaml
    ...
    standalone:
      container_name: milvus-standalone
      image: milvusdb/milvus:v2.5.16
    ```

2. Apply the upgrade:

    ```bash
    docker compose down
    docker compose up -d
    ```

3. Verify the upgrade:

    ```bash
    docker compose ps
    ```

### Step 3: Upgrade to v{{var.milvus_release_version}}

Once v2.5.16 is running successfully, upgrade to v{{var.milvus_release_version}}:

1. Update the Milvus image tag in your `docker-compose.yaml`:

    ```yaml
    ...
    standalone:
      container_name: milvus-standalone
      image: milvusdb/milvus:v{{var.milvus_release_tag}}
    ```

2. Apply the final upgrade:

    ```bash
    docker compose down
    docker compose up -d
    ```

## Verify the upgrade

Confirm your standalone deployment is running the new version:

```bash
# Check container status
docker compose ps

# Check Milvus version
docker compose logs standalone | grep "version"
```

## What's next
- You might also want to learn how to:
  - [Scale a Milvus cluster](scaleout.md)
- If you are ready to deploy your cluster on clouds:
  - Learn how to [Deploy Milvus on Amazon EKS with Terraform](eks.md)
  - Learn how to [Deploy Milvus Cluster on GCP with Kubernetes](gcp.md)
  - Learn how to [Deploy Milvus on Microsoft Azure With Kubernetes](azure.md)
