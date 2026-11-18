---
id: install_standalone-binary.md
label: "RPM/DEB Package"
related_key: "RPM/DEB Package"
summary: Learn how to install Milvus standalone with a pre-built RPM/DEB package.
title: Install Milvus Standalone with RPM/DEB Package
---

# Install Milvus Standalone with RPM/DEB Package

This page illustrates how to install Milvus standalone with a pre-built RPM/DEB package.

## Prerequisites

- You have already installed libstdc++ 8.5.0 or a later version.
- [Check the requirements for hardware and software](prerequisite-docker.md) prior to your installation.
- The host uses systemd. The package installs Milvus as a systemd service.
- On Rocky Linux 9 and 10, and on other distributions compatible with RHEL 9 or 10, install `libxcrypt-compat`. Milvus needs `libcrypt.so.1`, but the RPM package does not declare it as a dependency, so the package manager does not install it for you:

    ```bash
    sudo dnf install -y libxcrypt-compat
    ```

## Download the RPM/DEB Package

You can download the RPM/DEB package according to your system architecture from the [Milvus v{{var.milvus_deb_release}} release page](https://github.com/milvus-io/milvus/releases/tag/v{{var.milvus_deb_release}}).

- For x86_64/amd64, download the **{{var.milvus_deb_amd64}}** or **{{var.milvus_rpm_amd64}}** package.
- For ARM64, download the **{{var.milvus_deb_arm64}}** or **{{var.milvus_rpm_arm64}}** package.

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

<div class="alert warning">

> The 2.6.x packages add `/usr/lib/milvus` to the system linker cache through `/etc/ld.so.conf.d/milvus.conf`. That directory holds the OpenSSL libraries bundled with Milvus (`libssl.so.3` and `libcrypto.so.3`), so after the installation every program on the host loads them instead of the OpenSSL library of the distribution. On distributions that ship a newer OpenSSL, such as Rocky Linux 9 and 10 and Debian 13, programs such as `systemctl`, `journalctl`, `dnf`, `rpm`, `openssl`, `curl`, and the Python `ssl` module stop working, and on Rocky Linux 10 `sshd` rejects its own configuration. Keep your terminal session open, run the steps in [Keep the bundled libraries private to Milvus](#Keep-the-bundled-libraries-private-to-Milvus) right after the installation, and do not reboot the host before you have done so.

</div>

For RPM-based systems (such as Rocky Linux, RHEL, and Fedora), use `dnf` to install the package:

```bash
sudo dnf install -y ./{{var.milvus_rpm_amd64}}
```

For DEB-based systems (such as Ubuntu and Debian), use `apt-get` to install the package:

```bash
sudo apt-get install -y ./{{var.milvus_deb_amd64}}
```

The DEB package enables the `milvus` service and tries to start it during the installation. Where the linker cache problem above breaks `systemctl`, that start fails, but `apt-get` does not report an error.

## Keep the bundled libraries private to Milvus

Remove the linker cache entry, so that the rest of the system uses its own OpenSSL library again. Then make the bundled libraries visible to the Milvus service only:

```bash
sudo rm /etc/ld.so.conf.d/milvus.conf
sudo ldconfig
sudo mkdir -p /etc/systemd/system/milvus.service.d
printf '[Service]\nEnvironment=LD_LIBRARY_PATH=/usr/lib/milvus\n' | sudo tee /etc/systemd/system/milvus.service.d/libpath.conf
sudo systemctl daemon-reload
```

To confirm the change, check that the linker cache no longer lists `/usr/lib/milvus` and that the system OpenSSL works again:

```bash
ldconfig -p | grep /usr/lib/milvus
openssl version
```

The first command prints nothing, and the second one prints the OpenSSL version of your distribution.

Upgrading or reinstalling the package can bring `/etc/ld.so.conf.d/milvus.conf` back. After each upgrade, check whether the file exists, and if it does, run the first two commands above again.

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
● milvus.service - Milvus Standalone Server
     Loaded: loaded (/usr/lib/systemd/system/milvus.service; enabled; preset: enabled)
    Drop-In: /etc/systemd/system/milvus.service.d
             └─libpath.conf
     Active: active (running) since Wed 2026-11-18 14:12:07 UTC; 2s ago
   Main PID: 4743 (milvus)
```

Milvus is ready to serve requests when its health endpoint returns `OK`. This can take a few seconds after the service starts:

```bash
curl http://127.0.0.1:9091/healthz
```

You can find the Milvus binary at `/usr/bin/milvus`, the bundled libraries in `/usr/lib/milvus/`, and the configuration files in `/etc/milvus/configs/`. The path of the systemd unit file differs between distributions; run `systemctl cat milvus` to see it. The service runs as `root`. By default, `localStorage.path` and `rocksmq.path` in `milvus.yaml` point to directories under `/var/lib/milvus`.

## (Optional) Update Milvus configurations

You can modify the Milvus configurations in the `/etc/milvus/configs/milvus.yaml` file. For example, to change the `proxy.healthCheckTimeout` to `1000` ms, you can search for the target parameter and modify accordingly. For applicable configuration items, refer to [System Configuration](system_configuration.md).

Restart the service so that the change takes effect:

```bash
sudo systemctl restart milvus
```

On RPM-based systems, removing or upgrading the package deletes the whole `/etc/milvus` directory, including your changes. Keep a copy of your `milvus.yaml` outside `/etc/milvus`.

## Stop Milvus Standalone

To stop Milvus Standalone, you can use the following command:

```bash
sudo systemctl stop milvus
```

## Upgrade Milvus Standalone on RPM-based systems

Do not upgrade the 2.6.x RPM package in place with `dnf upgrade` or `rpm -U`. During an in-place upgrade, the removal script of the old package runs after the new files are installed and deletes `/etc/milvus` and `/usr/lib/milvus`, which leaves Milvus without its configuration and libraries.

Instead, upgrade in the following order:

1. Copy `/etc/milvus/configs/milvus.yaml` to a location outside `/etc/milvus`.
2. Uninstall the old package as described in [Uninstall Milvus Standalone](#Uninstall-Milvus-Standalone).
3. Install the new package and run the steps in [Keep the bundled libraries private to Milvus](#Keep-the-bundled-libraries-private-to-Milvus) again.
4. Restore your changes in `/etc/milvus/configs/milvus.yaml` and start the service.

## Uninstall Milvus Standalone

If `dnf` or `rpm` fails with an `OPENSSL_3.4.0` not found error, run the steps in [Keep the bundled libraries private to Milvus](#Keep-the-bundled-libraries-private-to-Milvus) first.

For RPM-based systems, the following command removes the package together with `/etc/milvus`:

```bash
sudo dnf remove -y milvus
```

For DEB-based systems, `apt-get remove` keeps the configuration files in `/etc/milvus`, and `apt-get purge` deletes them:

```bash
sudo apt-get purge -y milvus
```

Then remove the systemd drop-in directory that you created:

```bash
sudo rm -r /etc/systemd/system/milvus.service.d
sudo systemctl daemon-reload
```

To delete the stored data as well, remove `/var/lib/milvus` if you kept the default paths.

## What's next

Having installed Milvus Standalone, you can:

- Check [Quickstart](quickstart.md) to see what Milvus can do.

- Learn the basic operations of Milvus:
  - [Manage Databases](manage_databases.md)
  - [Manage Collections](manage-collections.md)
  - [Manage Partitions](manage-partitions.md)
  - [Insert, Upsert & Delete](insert-update-delete.md)
  - [Single-Vector Search](single-vector-search.md)
  - [Hybrid Search](multi-vector-search.md)

- [Upgrade Milvus Using Helm Chart](upgrade_milvus_cluster-helm.md).
- [Scale your Milvus cluster](scaleout.md).
- Deploy your Milvus cluster on clouds:
  - [Amazon EKS](eks.md)
  - [Google Cloud](gcp.md)
  - [Microsoft Azure](azure.md)
- Explore [Milvus WebUI](milvus-webui.md), an intuitive web interface for Milvus observability and management.
- Explore [Milvus Backup](milvus_backup_overview.md), an open-source tool for Milvus data backups.
- Explore [Birdwatcher](birdwatcher_overview.md), an open-source tool for debugging Milvus and dynamic configuration updates.
- Explore [Attu](https://github.com/zilliztech/attu), an open-source GUI tool for intuitive Milvus management.
- [Monitor Milvus with Prometheus](monitor.md).
