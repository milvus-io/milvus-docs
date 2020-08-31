<p>You need to set <code>index_file_size</code> when creating a collection from a client. This parameter specifies the size of each segment, and its default value is 1024 in MB. When the size of newly inserted vectors reaches the specified volume, Milvus packs these vectors into a new segment. In other words, newly inserted vectors do not go into a segment until they grow to the specified volume. When it comes to creating indexes, Milvus creates one index file for each segment. When conducting a vector search, Milvus searches all index files one by one.
</p>
<p>
As a rule of thumb, we would see a 30% ~ 50% increase in the search performance after changing the value of <code>index_file_size</code> from 1024 to 2048. Note that an overly large <code>index_file_size</code> value may cause failure to load a segment into the memory or graphics memory. Suppose the graphics memory is 2 GB and <code>index_file_size</code> 3 GB, each segment is obviously too large.
</p>
<p>
In situations where vectors are not frequently inserted, we recommend setting the value of <code>index_file_size</code> to 1024 MB or 2048 MB. Otherwise, we recommend setting the value to 256 MB or 512 MB to keep unindexed files from getting too large.
</p>