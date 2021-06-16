---
id: install_standalone-helm.md
label: Install with Helm Chart
order: 1
group: standalone
---

# Install Milvus Standalone

## Before You Begin

Before moving forward to installation, you must check the eligibility of your hardware in line with Milvus' requirement.

<details><summary>Check your Docker and Docker Compose version</summary>

<div class="alert note">
Docker Compose is the recommended way to install Milvus.
</div>
- Docker version 19.03 or higher is required.
- Docker Compose version 1.25.1 or higher is required. 
</details>

<details><summary>Check whether your CPU supports SIMD extension instruction set</summary>

{{fragments/cpu_support.md}}
</details>

<details><summary>Check your GPU’s eligibility</summary>
Milvus Standalone supports GPU acceleration on floating vectors. 
{{fragments/gpu_support.md}}
</details>

## Install Milvus Standalone

{{tab}}

