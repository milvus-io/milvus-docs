Milvus 在构建索引和向量查询时依赖于 CPU 对 SIMD (Single Instruction Multiple Data) 扩展指令集的支持。请确认运行 Milvus 的 CPU 至少支持以下 SIMD 指令集中的一种：

- SSE4.2

- AVX

- AVX2

- AVX512

可以使用 lscpu 命令来判断 CPU 是否支持特定 SIMD 指令集


```
$ lscpu | grep -e sse4_2 -e avx -e avx2 -e avx512
```
