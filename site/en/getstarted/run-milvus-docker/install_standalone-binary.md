---
id: install_standalone-binary.md
label: "RPM/DEB Package"
related_key: "RPM/DEB Package"
summary: Learn how to install Milvus standalone with a pre-built RPM/DEB package and run it as a systemd service.
title: Install Milvus Standalone with RPM/DEB Package
---

# Install Milvus Standalone with RPM/DEB Package

This page illustrates how to install Milvus standalone with a pre-built RPM/DEB package and run it as a systemd service.

## Prerequisites

- [Check the requirements for hardware and software](prerequisite-docker.md) prior to your installation.
- The host uses systemd. The package installs Milvus as a systemd service.
- The host has glibc 2.34 or a later version. The DEB package also requires libstdc++ from GCC 11 or a later version. The package manager checks these dependencies during the installation.

## Download the RPM/DEB Package

Not every Milvus release publishes RPM/DEB packages. The [Milvus v{{var.milvus_deb_release}} release page](https://github.com/milvus-io/milvus/releases/tag/v{{var.milvus_deb_release}}) lists the following packages:

- For x86_64/amd64, download the **{{var.milvus_deb_amd64}}** or **{{var.milvus_rpm_amd64}}** package.
- For ARM64, download the **{{var.milvus_deb_arm64}}** or **{{var.milvus_rpm_arm64}}** package.

To install a different release, check the **Assets** section of its [release page](https://github.com/milvus-io/milvus/releases) first, and use only a package that is listed there for your system architecture.

The following commands assume that you are going to run Milvus Standalone on an x86_64/amd64 machine.

For RPM-based systems:

```bash
wget https://github.com/milvus-io/milvus/releases/download/v{{var.milvus_deb_release}}/{{var.milvus_rpm_amd64}}
```

For DEB-based systems:

```bash
wget https://github.com/milvus-io/milvus/releases/download/v{{var.milvus_deb_release}}/{{var.milvus_deb_amd64}}
```

## Install the RPM/DEB Package

For RPM-based systems (such as Rocky Linux, RHEL, and Fedora), use `dnf` to install the package:

```bash
sudo dnf install -y ./{{var.milvus_rpm_amd64}}
```

For DEB-based systems (such as Ubuntu and Debian), use `apt-get` to install the package:

```bash
sudo apt-get install -y ./{{var.milvus_deb_amd64}}
```

The package creates a `milvus` system user and group, the data directory `/var/lib/milvus`, and the log directory `/var/log/milvus`. It installs the `milvus` systemd service but does not enable or start it.

## Start Milvus Standalone

Enable the `milvus` service so that it starts at boot, and start it now:

```bash
sudo systemctl enable --now milvus
```

You can check the status of the Milvus service using the following command:

```bash
systemctl status milvus
```

If Milvus is running successfully, you should see output similar to the following:

```text
● milvus.service - Milvus 3.0 Standalone Server
     Loaded: loaded (/usr/lib/systemd/system/milvus.service; enabled; preset: disabled)
     Active: active (running) since Wed 2026-11-18 14:16:05 UTC; 2s ago
   Main PID: 326 (milvus)
```

Milvus is ready to serve requests when its health endpoint returns `OK`. This can take a few seconds after the service starts:

```bash
curl http://127.0.0.1:9091/healthz
```

The service runs as the `milvus` user and listens on port `19530` for client connections and on port `9091` for the health check and metrics, on all network interfaces. The embedded etcd listens on `127.0.0.1:2379`. Restrict access to these ports with your firewall as needed.

The package installs the following files:

| Path | Content |
|---|---|
| `/usr/bin/milvus` | Launcher script that the service runs |
| `/usr/lib/milvus/` | Milvus binary and its bundled libraries |
| `/etc/milvus/configs/` | Configuration files, including `milvus.yaml` |
| `/var/lib/milvus/` | Data, embedded etcd metadata, and message queue files |
| `/var/log/milvus/` | Milvus log files |

You can also read the service logs with `journalctl -u milvus`.

<div class="alert warning">

> The package ships example TLS certificates and private keys in `/etc/milvus/configs/cert/`. Anyone who downloads the package has the same keys, so do not use them to enable TLS. To enable TLS, create your own certificates as described in [Encryption in Transit](tls.md).

</div>

## (Optional) Update Milvus configurations

You can modify the Milvus configurations in the `/etc/milvus/configs/milvus.yaml` file. For example, to change the `proxy.healthCheckTimeout` to `1000` ms, you can search for the target parameter and modify accordingly. For applicable configuration items, refer to [System Configuration](system_configuration.md).

Restart the service so that the change takes effect:

```bash
sudo systemctl restart milvus
```

## Stop Milvus Standalone

To stop Milvus Standalone, you can use the following command:

```bash
sudo systemctl stop milvus
```

## Uninstall Milvus Standalone

Stop the service and disable it first. The DEB package does not stop or disable the service when it is removed:

```bash
sudo systemctl disable --now milvus
```

Then remove the package. For RPM-based systems:

```bash
sudo dnf remove -y milvus
```

For DEB-based systems:

```bash
sudo apt-get remove -y milvus
```

Removing the package does not delete the `milvus` user and group, the data in `/var/lib/milvus`, or the logs in `/var/log/milvus`, and it can leave the configuration in `/etc/milvus` behind. Delete them yourself if you no longer need them.

## What's next

Having installed Milvus Standalone, follow the **Use an existing Milvus server** path in [Quickstart](quickstart.md), connecting to `http://localhost:19530`, to insert data and run a search.
