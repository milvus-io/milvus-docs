---
id: release_notes.md
summary: Milvus Release Notes
---
# Release Notes

Find out what’s new in Milvus! This page summarizes information about new features, improvements, known issues, and bug fixes in each release. You can find the release notes for each released version after v2.1.0 in this section. We suggest that you regularly visit this page to learn about updates.

## v2.1.0

Release date: 2022-07-22

<h3 id="v2.1.0">Compatibility</h3>

<table class="version">
	<thead>
	<tr>
		<th>Milvus version</th>
		<th>Python SDK version</th>
		<th>Java SDK version</th>
		<th>Go SDK version</th>
		<th>Node.js SDK version</th>
	</tr>
	</thead>
	<tbody>
	<tr>
		<td>2.1.0</td>
		<td>2.1.0</td>
		<td>2.1.0</td>
		<td>2.1.0</td>
		<td>2.1.2</td>
	</tr>
	</tbody>
</table>


Milvus 2.1.0 not only introduces many new features including support for VARCHAR data type, memory replicas, embedded Milvus, Kafka support, and RESTful API but also greatly improves the functionality, performance, and stability of Milvus. 

<h3 id="v2.1.0">Features</h3>

- Support for VARCHAR data type

Milvus now supports variable-length string as a scalar data type. Like previous scalar types, VARCHAR can be specified as an output field or be used for attribute filtering. A MARISA-trie-based inverted index is also supported to accelerate prefix query and exact match.

- Memory Replicas

Memory replicas enable you to load data on multiple query nodes. Like read replicas in traditional databases, memory replicas can help increase throughput if you have a relatively small dataset but want to scale read throughput with more hardware resources. We will support hedged read in future releases to increase availability when applying memory replicas.

- Embedded Milvus

Embedded Milvus enables you to [pip install Milvus](install_embedded_milvus.md
) in one command, try quick demos and run short scripts in Python on your Macbook, including on the ones with M1 processor. 

- Kafka Support (Beta)

Apache Kafka is the most widely used open-source distributed message store. In Milvus 2.1, you can simply use Kafka for message storage by modifying configurations. 

- RESTful API (Beta)

Milvus 2.1 now provides RESTful API for applications written in PHP or Ruby. GIN, one of the most popular Golang web frameworks, is adopted as the web server.

<h3 id="v2.1.0">Performance</h3>

The Milvus core team conducted a full performance benchmarking and profiling, and fixed a few bottlenecks on load/search paths. Under some test cases, Milvus search performance is boosted about 3.2 times thanks to the search combination logic.
- [#16014](https://github.com/milvus-io/milvus/pull/16014) Enables ZSTD compression for pulsar.
- [#16514](https://github.com/milvus-io/milvus/pull/16514) [#17273](https://github.com/milvus-io/milvus/pull/17273) Improves load performance.
- [#17005](https://github.com/milvus-io/milvus/pull/17005) Loads binlog for different fields in parallel. 
- [#17022](https://github.com/milvus-io/milvus/pull/17022) Adds logic for search merging and a simple task scheduler for read tasks.
- [#17194](https://github.com/milvus-io/milvus/pull/17194) Simplifies the merge logic of searchTask.
- [#17287](https://github.com/milvus-io/milvus/pull/17287) Reduces default seal proportion. 

<h3 id="v2.1.0">Stability</h3>

To improve stability, especially during streaming data insertion, we fixed a few critical issues including: 
- Fixed out of memory issues.
- Fixed message queue backlog full caused by message queue subscription leakge.
- Fixed the issue of deleted entities can still be readable.
- Fixed data being erroneously cleaned by compaction during load or index.


<h3 id="v2.1.0">Other improvements</h3>

- Security 

Starting from Milvus 2.1.0, we support username, password, and TLS connection. We also enabled safe connections to our dependencies such as S3, Kafka and etcd.

- ANTLR parser

Milvus now adopts Go ANTLR as the plan parser to make adding new grammar such as arithmetic operations on numerical fields more flexible. The adoption of ANTLR also prepares for Milvus query language support in future releases.

- Observability

We refined monitoring metrics by adding important metrics including search QPS and latency to the new dashboard. Please notify us if any metrics critical to your production environment are not listed.

- Deployment

For users who don't have a K8s environment but still want to deploy a cluster, Milvus now supports Ansible deployment. See [Install Milvus Cluster](install_cluster-ansible.md) for more information.

<h3 id="v2.1.0">Known issues</h3>

1. Partition is not a fully released feature so we recommend user not to rely on it. [#17648 When a partition is dropped, the data and index cannot be cleaned.](https://github.com/milvus-io/milvus/issues/17648)
2. When building index after load, the collection need to released and reloaded. [#17809 When an index is created on a loaded collection, the segment already loaded will not be notified to load the index.](https://github.com/milvus-io/milvus/issues/17809)

