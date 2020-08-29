<p>把 FLAT 和 IVF_FLAT 做比较，可以这么估算：</p>
<p>
已知 IVF_FLAT 索引是把向量分成 <code>nlist</code> 个单元。假设用默认的 <code>nlist</code> = 16384，搜索的时候是先用目标向量和这 16384 个中心点计算距离，得到最近的 <code>nprobe</code> 个单元，再在单元里计算最近向量。而 FLAT 是每条向量和目标向量计算距离。
</p>
<p>
所以当总的向量条数约等于 <code>nlist</code> 时，两者的计算量相当，性能也差不多。而随着向量条数达到 <code>nlist</code> 的 2 倍、3 倍、n 倍之后，IVF_FLAT 的优势就越来越大。</p>
<p>
详见文档 <a href="vector_db.md">选择向量索引工具</a>。
</p>