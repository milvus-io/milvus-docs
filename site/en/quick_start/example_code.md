---
id: example_code.md
---

# Hello Milvus 

After the Milvus server is successfully started, you can use this example program to create a table, insert 10 vectors, and then run a vector similarity search.

1. Ensure that you have installed [Python 3.6+](https://www.python.org/downloads/) and a compatible [pip](https://pip.pypa.io/en/stable/installing/).

2. Install Milvus Python SDK.

   ```shell
   # Install Milvus Python SDK
   $ pip3 install pymilvus=={{var.milvus_python_sdk_version}}
   ```

   <div class="alert note">
   To learn more about Milvus Python SDK, go to <a href="https://github.com/milvus-io/pymilvus/blob/{{var.milvus_python_sdk_version}}/README.md">Milvus Python SDK Readme.</a>
   </div>

3. Download Python example code.

   ```shell
   # Download Python example
   $ wget https://raw.githubusercontent.com/milvus-io/pymilvus/{{var.milvus_python_sdk_version}}/examples/example.py
   ```

   <div class="alert note">
   If you cannot use <code>wget</code> to download the example code, you can also create <b>example.py</b> and copy the <a href="https://github.com/milvus-io/pymilvus/blob/{{var.milvus_python_sdk_version}}/examples/example.py">example code.</a>
   </div>
   
4. Run the example code.

   ```shell
   # Run Milvus Python example
   $ python3 example.py
   ```
   <i>All going well, you should have seen the outcome of the CRUD operation results being printed on your screen.</i>

## What's next

- Learn [basic operations](milvus_operation.md) in Milvus
- [Try Milvus bootcamp](https://github.com/milvus-io/bootcamp) to check more solutions
