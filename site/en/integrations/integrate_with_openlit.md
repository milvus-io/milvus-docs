---
id: integrate_with_openlit.md
title: Monitoring Milvus operations using OpenTelmetry and OpenLIT
summary: This page discusses how to monitor Milvus operations using OpenTelemetry and OpenLIT.
---

This guide showcases how [OpenLIT](https://github.com/openlit/openlit) can be used to monitor and track Milvus vector database operations like insert, upsert, managing collections and more.

## Getting started

Before you start, make sure you have deployed OpenLIT locally, Refer to OpenLIT's [Official documentation](https://docs.openlit.io/latest/quickstart) to get started.


First, install the package for Milvus and OpenLIT:

```shell
pip install --upgrade openlit pymilvus
```

## Usage

### Step 1: Initialize OpenLIT in your Application
Integrating OpenLIT into LLM applications is straightforward. Start monitoring for your LLM Application with just **two lines of code**: 

```python
import openlit

openlit.init()
```

Lets take an example application which creates a Milvus collection, inserts some data and then does single-vector search:

```python
from pymilvus import MilvusClient, DataType
import openlit     # Import OpenLIT Library

openlit.init()     # Initialize OpenLIT for OTel auto instrumentation and generating traces and metrics

# 1. Set up a Milvus client
client = MilvusClient(
    uri="http://localhost:19530"
)

# 2. Create a collection in quick setup mode
client.create_collection(
    collection_name="quick_setup",
    dimension=5
)

data=[
    {"id": 0, "vector": [0.3580376395471989, -0.6023495712049978, 0.18414012509913835, -0.26286205330961354, 0.9029438446296592], "color": "pink_8682"},
    {"id": 1, "vector": [0.19886812562848388, 0.06023560599112088, 0.6976963061752597, 0.2614474506242501, 0.838729485096104], "color": "red_7025"},
    {"id": 2, "vector": [0.43742130801983836, -0.5597502546264526, 0.6457887650909682, 0.7894058910881185, 0.20785793220625592], "color": "orange_6781"},
    {"id": 3, "vector": [0.3172005263489739, 0.9719044792798428, -0.36981146090600725, -0.4860894583077995, 0.95791889146345], "color": "pink_9298"},
    {"id": 4, "vector": [0.4452349528804562, -0.8757026943054742, 0.8220779437047674, 0.46406290649483184, 0.30337481143159106], "color": "red_4794"},
    {"id": 5, "vector": [0.985825131989184, -0.8144651566660419, 0.6299267002202009, 0.1206906911183383, -0.1446277761879955], "color": "yellow_4222"},
    {"id": 6, "vector": [0.8371977790571115, -0.015764369584852833, -0.31062937026679327, -0.562666951622192, -0.8984947637863987], "color": "red_9392"},
    {"id": 7, "vector": [-0.33445148015177995, -0.2567135004164067, 0.8987539745369246, 0.9402995886420709, 0.5378064918413052], "color": "grey_8510"},
    {"id": 8, "vector": [0.39524717779832685, 0.4000257286739164, -0.5890507376891594, -0.8650502298996872, -0.6140360785406336], "color": "white_9381"},
    {"id": 9, "vector": [0.5718280481994695, 0.24070317428066512, -0.3737913482606834, -0.06726932177492717, -0.6980531615588608], "color": "purple_4976"}
]

res = client.insert(
    collection_name="quick_setup",
    data=data
)

print(res)

query_vectors = [
    [0.041732933, 0.013779674, -0.027564144, -0.013061441, 0.009748648]
]

res = client.search(
    collection_name="quick_setup",     # target collection
    data=query_vectors,                # query vectors
    limit=3,                           # number of returned entities
)

print(res)
```

To forward telemetry data to an HTTP OTLP endpoint, such as the OpenTelemetry Collector, set the `otlp_endpoint` parameter with the desired endpoint. Alternatively, you can configure the endpoint by setting the `OTEL_EXPORTER_OTLP_ENDPOINT` environment variable as recommended in the OpenTelemetry documentation.

> 💡 Info: If you don't provide `otlp_endpoint` function argument or set the `OTEL_EXPORTER_OTLP_ENDPOINT` environment variable, OpenLIT directs the trace directly to your console, which can be useful during development.
To send telemetry to OpenTelemetry backends requiring authentication, set the `otlp_headers` parameter with its desired value. Alternatively, you can configure the endpoint by setting the `OTEL_EXPORTER_OTLP_HEADERS` environment variable as recommended in the OpenTelemetry documentation.

### Step 3: Visualize and Optimize!

![](https://github.com/openlit/.github/blob/main/profile/assets/openlit-client-1.png?raw=true)

With the LLM Observability data now being collected by OpenLIT, the next step is to visualize and analyze this data to get insights into your LLM application’s performance, behavior, and identify areas of improvement.

To begin exploring your LLM Application's performance data within the OpenLIT UI, please see the [Quickstart Guide](https://docs.openlit.io/latest/quickstart).

If you want to integrate and send metrics and traces to your existing observability tools like Promethues+Jaeger, Grafana or more, refer to the [Official Documentation for OpenLIT Connections](https://docs.openlit.io/latest/connections/intro) for detailed instructions.


## Support

For any question or issue with integration you can reach out to the OpenLIT team on [Slack](https://join.slack.com/t/openlit/shared_invite/zt-2etnfttwg-TjP_7BZXfYg84oAukY8QRQ) or via [email](mailto:contact@openlit.io).