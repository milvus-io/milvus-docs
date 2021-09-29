在/home/$USER/milvus/conf路径下的**server_config.yaml**文件中，你可以为建立索引以及检索分配GPU。如下代码所示：

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
gpu0, 1, 2, 3是分配给Docker容器的GPU中的前四个。
</div>
