---
id: roadmap.md
title: Milvus Roadmap
related_key: Milvus roadmap
summary: Milvus is an open-source vector database built to power AI applications. Here is our roadmap to guide our development.
---

# Milvus Roadmap

Welcome to the Milvus Roadmap! Join us on our continuous journey to enhance and evolve Milvus. We are thrilled to share our accomplishments, future plans, and our vision for what lies ahead. Our roadmap is more than a list of upcoming features—it reflects our commitment to innovation and our dedication to working with the community. We invite you to delve into our roadmap, provide your feedback, and help shape the future of Milvus!

## Roadmap

<table>
    <tr>
        <th>Category</th>
        <th>Milvus 2.4.0 (Recently Achieved)</th>
        <th>Milvus 2.5.0 (Upcoming in Mid-CY24)</th>
        <th>Future Roadmap (Milvus 3.0 expected within CY24)</th>
    </tr>
    <tr>
        <td><strong>AI-developer Friendly</strong><br>A developer-friendly technology stack, enhanced with the latest AI innovations</td>
        <td><strong>Multi-Vectors & Hybrid Search</strong><br>Framework for multiplex recall and fusion<br><br><strong>GPU Index Acceleration</strong><br>Support for higher QPS and faster index creation<br><br><strong>Model Libraries in PyMilvus</strong><br>Integrated embedding models for Milvus</td>
        <td><strong>Sparse Vector (GA)</strong><br>Local feature extraction and keyword search<br><br><strong>Milvus Lite (GA)</strong><br>A lightweight, in-memory version of Milvus<br><br><strong>Embedding Models Gallery</strong><br>Support for image and multi-modal embeddings and reranker models in model libraries</td>
        <td><strong>Original Data-In and Data-Out</strong><br>Support for Blob data types<br><br><strong>Data Clustering</strong><br>Data co-locality<br><br><strong>Scenario-oriented Vector Search</strong><br>e.g. Multi-target search & NN filtering<br><br><strong>Support Embedding & Reranker Endpoint</strong></td>
    </tr>
    <tr>
        <td><strong>Rich Functionality</strong><br>Enhanced retrieval and data management features</td>
        <td><strong>Support for FP16, BF16 Datatypes</strong><br>These ML datatypes can help reduce memory usage<br><br><strong>Grouping Search</strong><br>Aggregate split embeddings<br><br><strong>Fuzzy Match and Inverted Index</strong><br>Support for fuzzy matching and inverted indexing for scalar types like varchar and int</td>
        <td><strong>Inverted Index for Array & JSON</strong><br>Indexing for array and partial support JSON<br><br><strong>Bitset Index</strong><br>Improved execution speed and future data aggregation<br><br><strong>Truncate Collection</strong><br>Allows data clearance while preserving metadata<br><br><strong>Support for NULL and Default Values</strong></td>
        <td><strong>Support for More Datatypes</strong><br>e.g. Datetime, GIS<br><br><strong>Advanced Text Filtering</strong><br>e.g. Match Phrase<br><br><strong>Primary Key Deduplication</strong></td>
    </tr>
    <tr>
        <td><strong>Cost Efficiency & Architecture</strong><br>Advanced systems emphasizing stability, cost efficiency, scalability, and performance</td>
        <td><strong>Support for More Collections/Partitions</strong><br>Handles over 10,000 collections in smaller clusters<br><br><strong>Mmap Optimization</strong><br>Balances reduced memory consumption with latency<br><br><strong>Bulk Insert Optimazation</strong><br>Simplifies importing large datasets</td>
        <td><strong>Lazy Load</strong><br>Data is loaded on-demand through read operations<br><br><strong>Major Compaction</strong><br>Re-distributes data based on configuration to enhance read performance<br><br><strong>Mmap for Growing Data</strong><br>Mmap files for expanding data segments</td>
        <td><strong>Memory Control</strong><br>Reduces out-of-memory issues and provides global memory management<br><br><strong>LogNode Introduction</strong><br>Ensures global consistency and addresses the single-point bottleneck in root coordination<br><br><strong>Storage Format V2</strong><br>Universal format design lays the groundwork for disk-based data access</td>
    </tr>
    <tr>
        <td><strong>Enterprise Ready</strong><br>Designed to meet the needs of enterprise production environments</td>
        <td><strong>Milvus CDC</strong><br>Capability for data replication<br><br><strong>Accesslog Enhancement</strong><br>Detailed recording for audit and tracing</td>
        <td><strong>New Resource Group</strong><br>Enhanced resource management<br><br><strong>Storage Hook</strong><br>Support for Bring Your Own Key (BYOK) encryption</td>
        <td><strong>Dynamic Replica Number Adjustment</strong><br>Facilitates dynamic changes to the number of replicas<br><br><strong>Dynamic Schema Modification</strong><br>e.g., Add/delete fields, modify varchar lengths<br><br><strong>Rust and C# SDKs</strong></td>
    </tr>
</table>

- Our roadmap is typically structured into three parts: the most recent release, the next upcoming release, and a mid-to-long term vision within the next year.
- As we progress, we continually learn and occasionally adjust our focus, adding or removing items as needed.
- These plans are indicative and subject to change, and may vary based on subscription services.
- We steadfastly adhere to our roadmap, with our [release notes](release_notes.md) serving as a reference.

## How to contribute

As an open-source project, Milvus thrives on community contributions. Here's how you can be a part of our journey.

### Share feedback

- Issue reporting: Encounter a bug or have a suggestion? Open an issue on our [GitHub page](https://github.com/milvus-io/milvus/issues).

- Feature suggestions: Have ideas for new features or improvements? [We'd love to hear them!](https://github.com/milvus-io/milvus/discussions)

### Code contributions

- Pull requests: Contribute directly to our [codebase](https://github.com/milvus-io/milvus/pulls). Whether it's fixing bugs, adding features, or improving documentation, your contributions are welcome.

- Development guide: Check our [Contributor's Guide](https://github.com/milvus-io/milvus/blob/82915a9630ab0ff40d7891b97c367ede5726ff7c/CONTRIBUTING.md) for guidelines on code contributions.

### Spread the word

- Social sharing: Love Milvus? Share your use cases and experiences on social media and tech blogs.

- Star us on GitHub: Show your support by starring our [GitHub repository](https://github.com/milvus-io/milvus).
