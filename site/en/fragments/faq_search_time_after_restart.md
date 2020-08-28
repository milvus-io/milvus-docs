This is because, after restarting, Milvus needs to load data from the disk to the memory for the first vector search. You can set <code>preload_collection</code> in <strong>server_config.yaml</strong> and load as many collections as the memory permits. Milvus loads collections to the memory each time it restarts. 

Otherwise, you can call <code>load_collection()</code> to load collections to the memory.
