---
id: install_standalone-docker.md
label: Install with Docker Compose
order: 0
group: standalone
summary: Installation instructions for the standalone version of Milvus.

---

# Install Milvus Standalone

{{fragments/installation_guide.md}}

{{tab}}

## Download installation files

[Download **milvus-standalone-docker-compose.yml**](https://github.com/milvus-io/milvus/releases/download/v{{var.cpu_milvus_docker_image_version}}/milvus-standalone-docker-compose.yml) directly or with the following command, and save it as **docker-compose.yml**.

```
wget https://github.com/milvus-io/milvus/releases/download/v{{var.cpu_milvus_docker_image_version}}/milvus-standalone-docker-compose.yml -O docker-compose.yml
```

## Configure Milvus (optional)

[Download **milvus.yaml**](https://raw.githubusercontent.com/milvus-io/milvus/v{{var.cpu_milvus_docker_image_version}}/configs/milvus.yaml) directly or with the following command, and modify the configurations to suit your needs. See [Milvus Standalone System Configurations](configuration_standalone-basic.md) for more information.

```
wget https://raw.githubusercontent.com/milvus-io/milvus/v{{var.cpu_milvus_docker_image_version}}/configs/milvus.yaml
```

In **docker-compose.yml**, map the local path to your **milvus.yaml** file onto the corresponding docker container path to the configuration file **/milvus/configs/milvus.yaml** under the `volumes` section.

```yaml
    volumes:
      - ${DOCKER_VOLUME_DIRECTORY:-.}/volumes/milvus:/var/lib/milvus
      - /local/path/to/your/file:/milvus/configs/milvus.yaml
```

<div class="alert note">
Data is stored in the <b>volumes</b> folder according to the default configuration in <b>docker-compose.yml</b>. To change the folder to store data, edit <b>docker-compose.yml</b> or run <code>$ export DOCKER_VOLUME_DIRECTORY=</code>.
</div>

## Start Milvus

```shell
$ docker-compose up -d
```

```text
Docker Compose is now in the Docker CLI, try `docker compose up`
Creating milvus-etcd  ... done
Creating milvus-minio ... done
Creating milvus-standalone ... done
```

*After Milvus standalone starts, three running docker containers appear including two infrastructure services and one Milvus service.* 

```
$ sudo docker-compose ps
      Name                     Command                  State                          Ports
----------------------------------------------------------------------------------------------------------------
milvus-etcd         etcd -listen-peer-urls=htt ...   Up (healthy)   2379/tcp, 2380/tcp
milvus-minio        /usr/bin/docker-entrypoint ...   Up (healthy)   9000/tcp
milvus-standalone   /tini -- milvus run standalone   Up             0.0.0.0:19530->19530/tcp,:::19530->19530/tcp
```

## Stop Milvus

To stop Milvus standalone, run <code> $ sudo docker-compose down</code>.

To delete data after stopping Milvus, run <code> $ sudo rm -rf  volumes</code>.

## What's next

Having installed Milvus, You can:

- Check [Hello Milvus](example_code.md) to run an example code with different SDKs to see what Milvus can do.
- See [Upgrade Milvus Using Helm Chart](upgrade.md) for instructions to upgrade your Milvus server.
- Explore [MilvusDM](migrate_overview.md), an open-source tool designed for importing and exporting data in Milvus.

