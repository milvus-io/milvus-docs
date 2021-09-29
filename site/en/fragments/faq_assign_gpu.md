In **server_config.yaml** file under /home/$USER/milvus/conf, you can assign GPU devices to index/search. See example:

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
GPU 0,1,2,3 are first 4 GPUs from the list of GPU devices assigned to the docker container.
</div>