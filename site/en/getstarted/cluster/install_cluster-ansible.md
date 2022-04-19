---
id: install_cluster-ansible.md
label: Ansible Controller
related_key: Docker
order: 4
group: install_cluster-docker.md
summary: Learn how to install Milvus cluster with Ansible Controller.
---

# Install Milvus Cluster

{{fragments/installation_guide_cluster.md}}

{{tab}}


## Prerequisites

- Hardware: Three virtual machines each with four cores of CPU and 8 GB of RAM or more
- Operating system: Ubuntu 20.04 LTS
- Software: Ansible Controller

## Download Ansible Milvus node deployment Playbook

Download the `ansible-milvus-node-deployment` Playbook.

```
$ git clone https://github.com/john-h-luo/ansible-milvus-node-deployment.git
```

## Configure installation files

Enter the local path to the playbook and configure the installation files.

```shell
$ cd your/local/path/to/ansible-milvus-node-deployment
```

### Configure `inventory.ini`

Configure Ansible `inventory.ini` to divide hosts in groups in accordance with their roles in the Milvus system.

Add host names, and define `docker` group and `vars`.



```
[dockernodes] # Define group name in square brackets
dockernode01 # Replace the default value with hostnames
dockernode02
dockernode03

[admin]
ansible-controller

[coords]
dockernode01

[nodes]
dockernode02

[dependencies]
dockernode03

[docker:children] # Define `docker` group
dockernodes
coords
nodes
dependencies

[docker:vars] # Define `vars`
ansible_python_interpreter=/usr/bin/python3
StrictHostKeyChecking=no
```

### Configure `ansible.cfg`

`ansible.cfg` controls the action of the playbook, for example, SSH key, etc.

```
[defaults]
host_key_checking = False
inventory = inventory.ini # Specify the Inventory file
private_key_file=~/.my_ssh_keys/gpc_sshkey # Specify the SSH key that Ansible uses to access Docker host
```

### Configure `deploy-docker.yml`

`deploy-docker.yml` defines the tasks during the installation of Docker. See the code comments in the file for details.

```
- name: setup pre-requisites # Installation prerequisites
  hosts: all 
  become: yes
  become_user: root
  roles:
    - install-modules
    - configure-hosts-file

- name: install docker
  become: yes
  become_user: root
  hosts: dockernodes
  roles:
    - docker-installation
```

## Test Ansible connectivity

Test the connectivity to Ansible.

```shell
$ ansible all -m ping
```

Add `-i` in the command to specify the path to the inventory file if you did not specify it in `ansible.cfg`, otherwise Ansible uses `/etc/ansible/hosts`.

## Check the Playbook Syntax

Check the syntax of the Playbook.

```shell
$ ansible-playbook deploy-docker.yml --syntax-check
```

Normally, the terminal returns as follow:

```
playbook: deploy-docker.yml
```

## Install Docker

Install Docker with the Playbook.

```shell
$ ansible-playbook deploy-docker.yml
```

If Docker is successfully installed on the three hosts, the terminal returns as follow:

```
TASK [docker-installation : Install Docker-CE] *******************************************************************
ok: [dockernode01]
ok: [dockernode03]
ok: [dockernode02]

TASK [docker-installation : Install python3-docker] **************************************************************
ok: [dockernode01]
ok: [dockernode02]
ok: [dockernode03]

TASK [docker-installation : Install docker-compose python3 library] **********************************************
changed: [dockernode01]
changed: [dockernode03]
changed: [dockernode02]

PLAY RECAP *******************************************************************************************************
ansible-controller         : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
dockernode01               : ok=10   changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
dockernode02               : ok=10   changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
dockernode03               : ok=10   changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

## Verify the installation

Log in to the three hosts with the SSH key, and verify the installation on the hosts.

- For root host:

```shell
$ docker -v
```

- For non-root hosts:

```shell
$ sudo docker -v
```

Normally, the terminal returns as follow:

```
Docker version 20.10.14, build a224086
```

Check the running status of the containers.

```shell
$ docker ps
```

## Check the Syntax of `deploy-milvus.yml`

Check the Syntax of `deploy-milvus.yml`.

```shell
$ ansible-playbook deploy-milvus.yml --syntax-check
```

Normally, the terminal returns as follow:

```
playbook: deploy-milvus.yml
```

## Create Milvus container

The tasks to create Milvus container are defined in `deploy-milvus.yml`.

```shell
$ ansible-playbook deploy-milvus.yml
```

The terminal returns:

```
PLAY [Create milvus-etcd, minio, pulsar] *****************************************************************

TASK [Gathering Facts] ********************************************************************************************
ok: [dockernode03]

TASK [etcd] *******************************************************************************************************
changed: [dockernode03]

TASK [pulsar] *****************************************************************************************************
changed: [dockernode03]

TASK [minio] ******************************************************************************************************
changed: [dockernode03]

PLAY [Create milvus nodes] ****************************************************************************************

TASK [Gathering Facts] ********************************************************************************************
ok: [dockernode02]

TASK [querynode] **************************************************************************************************
changed: [dockernode02]

TASK [datanode] ***************************************************************************************************
changed: [dockernode02]

TASK [indexnode] **************************************************************************************************
changed: [dockernode02]

PLAY [Create milvus coords] ***************************************************************************************

TASK [Gathering Facts] ********************************************************************************************
ok: [dockernode01]

TASK [rootcoord] **************************************************************************************************
changed: [dockernode01]

TASK [datacoord] **************************************************************************************************
changed: [dockernode01]

TASK [querycoord] *************************************************************************************************
changed: [dockernode01]

TASK [indexcoord] *************************************************************************************************
changed: [dockernode01]

TASK [proxy] ******************************************************************************************************
changed: [dockernode01]

PLAY RECAP ********************************************************************************************************
dockernode01               : ok=6    changed=5    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
dockernode02               : ok=4    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
dockernode03               : ok=4    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

Now you have Milvus deployed on the three hosts.

## What's next

Having installed Milvus, you can:

- Check [Hello Milvus](example_code.md) to run an example code with different SDKs to see what Milvus can do.

- Learn the basic operations of Milvus:
  - [Connect to Milvus server](manage_connection.md)
  - [Conduct a vector search](search.md)
  - [Conduct a hybrid search](hybridsearch.md)

- Explore [MilvusDM](migrate_overview.md), an open-source tool designed for importing and exporting data in Milvus.
- [Monitor Milvus with Prometheus](monitor.md).
