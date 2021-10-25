---
id: prerequisite-docker.md
label: Install with Docker Compose
order: 0
group: prerequisite
summary: Learn the necessary preparations before installing Milvus.

---

# Before You Begin

Before you install Milvus, check your hardware and software to see if they meet the requirements.

{{tab}}

## Hardware requirements

| Component           | Requirement                                                  | Note                                                         |
| ------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| CPU                 | Intel CPU Sandy Bridge or later                              | Current version of Milvus does not support AMD and Apple M1 CPUs. |
| CPU Instruction Set | <ul><li>SSE4.2</li><li>AVX</li><li>AVX2</li><li>AVX-512</li></ul> | Vector similarity search and index building within Milvus require CPU's support of single instruction, multiple data (SIMD) extension sets. Ensure that the CPU supports at least one of the SIMD extensions listed. See [CPUs with AVX](https://en.wikipedia.org/wiki/Advanced_Vector_Extensions#CPUs_with_AVX) for more information. |
| RAM                 | 8 GB or more (depends on the data volume)                    |                                                              |
| Hard Drive          | SATA 3.0 SSD or later                                        |                                                              |

## Software requirements

| Operating system           | Software                                                     | Note                                                         |
| -------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| macOS 10.14 or later       | Docker Desktop                                               | Set the Docker virtual machine (VM) to use a minimum of 2 virtual CPUs (vCPUs) and 8 GB of initial memory. Otherwise, installation might fail. <br/>See [Install Docker Desktop on Mac](https://docs.docker.com/desktop/mac/install/) for more information. |
| Linux platforms            | <ul><li>Docker 19.03 or later</li><li>Docker Compose 1.25.1 or later</li></ul> | See [Install Docker Engine](https://docs.docker.com/engine/install/) and [Install Docker Compose](https://docs.docker.com/compose/install/) for more information. |
| Windows with WSL 2 enabled | Docker Desktop                                               | We recommend that you store source code and other data bind-mounted into Linux containers in the Linux file system instead of the Windows file system.<br/>See [Install Docker Desktop on Windows with WSL 2 backend](https://docs.docker.com/desktop/windows/install/#wsl-2-backend) for more information. |

