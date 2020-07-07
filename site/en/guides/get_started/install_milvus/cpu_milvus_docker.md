---
id: cpu_milvus_docker.md
title: Install CPU-only Milvus
sidebar_label: Install CPU-only Milvus
---

# Install CPU-only Milvus

## Prerequisites

#### Operating system requirements

| Operating system | Supported versions                              |
| :--------------- | :----------------------------------------------------------- |
| CentOS           | 7.5 or higher                                                |
| Ubuntu LTS       | 18.04 or higher                                              |

#### Hardware requirements

| Component | Recommended configuration             |
| ---------- | ------------------------------------- |
| CPU        | Intel CPU Sandy Bridge or higher. |
| CPU instruction set | <li>SSE42</li><li>AVX</li><li>AVX2</li><li>AVX512</li> |
| RAM        | 8 GB or more (depends on the data volume) |
| Hard drive | SATA 3.0 SSD or higher                |

#### Software requirements

| Software     | Version                                |
| ------- | -------------------------------------- |
| Docker  | 19.03 or higher                             |

<div class="alert note">
Please ensure that the available memory is greater than the sum of <code>cache.insert_buffer_size</code> and <code>cache.cache_size</code> set in the <b>milvus.yaml</b> file.
</div>

#### Confirm Docker status

Confirm that the Docker daemon is running in the background:

```shell
$ sudo docker info
```

<div class="alert note">
<ul>
<li>If you do not see the server listed, start the Docker daemon.</li>
<li>On Linux, Docker needs <code>sudo</code> privileges. To run Docker commands without <code>sudo</code>, create a <code>docker</code> group and add your users (see <a href="https://docs.docker.com/install/linux/linux-postinstall/">Post-installation steps for Linux</a> for details).</li>
</ul>
</div>

## Pull Docker image

Pull the CPU-only image:

```shell
$ docker pull milvusdb/milvus:{{var.cpu_milvus_docker_image_version}}
```

<div class="alert note">
If the pulling speed is too slow or the pulling process constantly fails, refer to <a href="../../../faq/operational_faq.md">Operational FAQ</a> for possible solutions.
</div>

## Download configuration files

```shell
$ mkdir -p /home/$USER/milvus/conf
$ cd /home/$USER/milvus/conf
$ wget https://raw.githubusercontent.com/milvus-io/milvus/v{{var.release_version}}/core/conf/demo/server_config.yaml
```

<div class="alert note">
If you cannot download configuration files via the <code>wget</code> command, you can create the <b>server_config.yaml</b> file under <b>/home/$USER/milvus/conf</b>, then copy the content from <a href="https://github.com/milvus-io/milvus/blob/v{{var.release_version}}/core/conf/demo/server_config.yaml">server config</a> to your configuration file.
</div>

## Start Docker container

Start the Docker container and map the paths of local files to the container:

```shell
$ docker run -d --name milvus_cpu_{{var.release_version}} \
-p 19530:19530 \
-p 19121:19121 \
-v /home/$USER/milvus/db:/var/lib/milvus/db \
-v /home/$USER/milvus/conf:/var/lib/milvus/conf \
-v /home/$USER/milvus/logs:/var/lib/milvus/logs \
-v /home/$USER/milvus/wal:/var/lib/milvus/wal \
milvusdb/milvus:{{var.cpu_milvus_docker_image_version}}
```

The `docker run` options used in the above command are defined as follows:

- `-d`: Runs container in the background and prints container ID.
- `--name`: Assigns a name to the container.
- `--gpus`: Assigns GPU devices to the container. ('all' represents all GPUs.)
- `-p`: Publishes a container’s port(s) to the host.
- `-v`: Mounts the directory into the container.

Confirm the running state of Milvus:

```shell
$ docker ps
```

If Milvus server cannot successfully start, check the error logs:

```shell
# Get the ID of the container running Milvus.
$ docker ps -a
# Check docker logs.
$ docker logs <milvus container id>
```

## What's next

- If you're just getting started with Milvus:

  - [Try an example program](../example_code.md)
  - [Learn more about Milvus operations](../../milvus_operation.md)
  - [Try Milvus Bootcamp](https://github.com/milvus-io/bootcamp)
  
- If you're ready to run Milvus in production:

  - Build a [monitoring and alerting system](../../monitor.md) to check real-time application performance
  - Tune Milvus performance through [configuration](../../../reference/milvus_config.md)
  
- If you want to use GPU-accelerated Milvus for search in large datasets:
  
  - [Install GPU-enabled Milvus](gpu_milvus_docker.md)
