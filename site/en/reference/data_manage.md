---
id: data_manage.md
---

# Manage Metadata with MySQL

Milvus uses SQLite as metadata management service in the backend by default. SQLite is embedded in the Milvus process, so there is no need to run additional services. However, in production, it is strongly recommended that you use MySQL as metadata management service because of reliability.

<div class="alert warning">
In CentOS, Milvus does not support MySQL 8.0 or higher.
</div>

Follow the steps below to use MySQL as metadata management service in Linux:

1. Pull the latest image of MySQL:

    ```shell
    $ docker pull mysql:5.7
    ```

2. Launch MySQL service. You can set your own password and port.

    ```shell
    $ docker run -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123456 -d mysql:5.7
    ```

3. Use root account and the IP of the host that runs MySQL service (`<MySQL_server_host IP>`) to log in MySQL. Press \<ENTER\> to enter the password you set in the previous step.

    ```shell
    $ mysql -h<MySQL_server_host IP> -uroot -p
    ```

4. Enter MySQL client command line interface to create a database. Here we use `milvus` as the database name.

    ```sql
    mysql> create database milvus;
    ```

5. Quit MySQL client and update the `meta_uri` parameter in **server_config.yaml**. Use the IP of the host that runs MySQL service (`<MySQL_server_host IP>`). Note that the password, IP address, port, and database name must be consistent with your previous settings.

    ```yaml
    meta_uri: mysql://root:123456@<MySQL_server_host IP>:3306/milvus
    ```

6. Use the updated **server_config.yaml** to launch Milvus.


## FAQ

<details>
<summary><font color="#4fc4f9">Why does Milvus return <code>database is locked</code>?</font></summary>
{{fragments/faq_database_locked.md}}
</details>
<details>
<summary><font color="#4fc4f9">Why can't I find vectors on SQLite or MySQL?</font></summary>
{{fragments/faq_no_embeddings_sqlite_mysql.md}}
</details>
<details>
<summary><font color="#4fc4f9">Can I use SQL Server or PostgreSQL to store metadata in Milvus?</font></summary>
{{fragments/faq_supported_meta_db.md}}
</details>



## Related blogs

From data import, data storage to data querying and scheduling, our blogs on Medium provide detailed insights into the data management mechanism of Milvus.

- [Managing Data in Massive-Scale Vector Database](https://medium.com/@milvusio/managing-data-in-massive-scale-vector-search-engine-db2e8941ce2f)
- [Improvements of the Data File Cleanup Mechanism](https://github.com/milvus-io/community/blob/master/blog/en/2019-12-18-datafile-cleanup.md)
- [Viewing Metadata](https://medium.com/@milvusio/milvus-metadata-management-1-6b9e05c06fb0)
- [Fields in Metadata Tables](https://medium.com/@milvusio/milvus-metadata-management-2-fields-in-the-metadata-table-3bf0d296ca6d)
- [How to Manage Data Files with Metadata](https://medium.com/@milvusio/milvus-metadata-management-3-e65b14137f58)
