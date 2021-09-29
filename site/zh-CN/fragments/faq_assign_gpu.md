在 /home/$USER/milvus/conf 路径下的 <b>server_config.yaml</b> 文件中，你可以为建立索引以及检索分配 GPU。如下代码所示：

```
gpu:
  enable: true
  cache_size: 10GB
  gpu_search_threshold: 0
  search_devices:
    - gpu0
    - gpu1
  build_index_devices:
    - gpu2
    - gpu3
```
<div class="alert note">
gpu 0, 1, 2, 3是分配给 Docker 容器的 GPU 中的前四个。
</div>
