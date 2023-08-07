---
id: birdwatcher_usage.md
summary: Learn how to use Birdwatch to debug Milvus.
---

# Birdwatcher Usage Guide

This page demonstrates how to install and use Birdwatcher.

## Install Birdwatcher

You can download and install the built binary, install it as a common Go module, or build it from the source.

- Install it as a common Go module.

    ```shell
    git clone https://github.com/milvus-io/birdwatcher.git
    cd birdwatcher
    go install github.com/milvus-io/birdwatcher
    ```

    Then you can run Birdwatcher as follows:

    ```shell
    go run main.go
    ```

- Build it from the source.

    ```shell
    git clone https://github.com/milvus-io/birdwatcher.git
    cd birdwatcher
    go build -o birdwatcher main.go
    ```

    Then you can run Birdwatcher as follows:

    ```shell
    ./birdwatcher
    ```

- Download the already-built binary

    First, open the [latest release page](https://github.com/milvus-io/birdwatcher/releases/latest), and find the prepared binaries.

    ```shell
    wget -O birdwatcher.tar.gz \
    https://github.com/milvus-io/birdwatcher/releases/download/latest/birdwatcher_<os>_<arch>.tar.gz
    ```

    Then you can decompress the tarball and use Birdwatcher as follows:

    ```shell
    tar -xvzf birdwatcher.tar.gz
    ./birdwatcher
    ```

## Connect to etcd

Once you start Birdwatcher using either of the preceding way, you will be greeted by a prompt that reads `Offline >`. Type `help` to view the available commands and flags.

```shell
Offline > help
Usage:
   [command]

Available Commands:
  assemble-indexfiles 
  completion          Generate the autocompletion script for the specified shell
  connect             Connect to etcd
  exit                Close this CLI tool
  help                Help about any command
  load-backup         load etcd backup file
  open-workspace      Open workspace
  parse-indexparam    parse index params
  parse-ts            parse hybrid timestamp
  pulsarctl           connect to pulsar admin with pulsarctl
  validate-indexfiles validate index file size
  version             print version

Flags:
  -h, --help   help for this command

Use " [command] --help" for more information about a command.
```

To connect to the etcd of your Milvus instance, run the `connect` command as follows:

```shell
Offline > connect
Using meta path: by-dev/meta/
```

if the above command fails due to an incorrect root path and you know the correct root path, run the following commands to make the connection:

```shell
Offline > connect --rootPath my-release
Using meta path: my-release/meta/
failed to open audit.log file!
Milvus(my-release) > 
```

If the above command fails due to an incorrect root path but you do not know the root path, you can run the following commands to make the connection:

```shell
Offline > connect --dry
using dry mode, ignore rootPath and metaPath
```

```shell
Etcd(127.0.0.1:2379) > find-milvus
1 candidates found:
my-release
```

```shell
Etcd(127.0.0.1:2379) > use my-release
Using meta path: my-release/meta/
failed to open audit.log file!
Milvus(my-release) >
```

## Show information

