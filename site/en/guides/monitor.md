---
id: monitor.md
title: Monitoring and Alerting
sidebar_label: Monitoring and Alerting
---

# Monitoring and Alerting

## Overview

Although Milvus is highly available, it is critical to actively monitor the overall performance of a system running in production, and to create alerting rules that promptly send notifications when there are events that require investigation or intervention.

### Monitoring solution

Milvus uses Prometheus to store and monitor its metrics and Grafana to flexibly visulize data.

#### Prometheus

  Prometheus is a system monitoring and alerting toolkit with a multi-dimensional data model and a flexible query language.

  The Prometheus ecosystem consists of multiple components, of which the following are used in Milvus:

  - Prometheus server which scrapes and stores time series data.
  - Client libraries for instrumenting application metrics.
  - Alertmanager for alert handling.
  - Pushgateway to allow short-lived, batch metrics, which may not be scraped in time, to be exposed to Prometheus.

Milvus collects monitoring data and pushes it to Pushgateway. At the same time, the Prometheus server will periodically pull data from Pushgateway and save it to its time-series database. The following graph shows how Prometheus works in Milvus:

![prometheus](../../../assets/monitoring/monitoring.png)

#### Grafana

  Grafana is an open source platform for time-series analytics and used in Milvus to visualize various performance metrics:

  ![dashboard](../../../assets/prometheus.png)


### Events to create alert rules

Active monitoring helps you identify problems early, but it is also essential to create alerting rules that promptly send notifications when there are events that require investigation or intervention.

This section includes the most important events for which you must create alerting rules.

**Server is down**

- Rule: Send an alert when the Milvus server is down.
- How to detect: If the Milvus server is down, **No Data** will be displayed on the monitoring dashboard.

**CPU/GPU temperature is too high**

- Rule: Send an alert when the CPU/GPU temperature exceeds 80 degrees Celsius.
- How to detect: Check the metrics `CPU Temperature` and  `GPU Temperature` on the monitoring dashboard.

## Use Prometheus and Alertmanager

Milvus generates detailed time series metrics. This page shows you how to pull these metrics into [Prometheus](https://prometheus.io/), and how to connect [Grafana](https://grafana.com/) and [Alertmanager](https://prometheus.io/docs/alerting/alertmanager/) to Prometheus for flexible data visualizations and notifications.

### Before you begin

- Make sure you have already started a Milvus server and enabled the monitoring function.

### Install Prometheus

1. Download the [Prometheus tarball](https://prometheus.io/download/) for your OS.

2. Go to the Prometheus file directory, and make sure Prometheus is installed successfully:

   ```shell
   $ ./prometheus --version
   ```

   <div class="alert info">
   You can extract the Prometheus binary and add it to your <code>PATH</code>. This makes it easy to start Prometheus from any shell.
   </div>

### Configure and start Prometheus

1. Start Pushgateway:

    ```shell
    ./pushgateway
    ```

    <div class="alert note">
    You must start Pushgateway before starting the Milvus Server.
    </div>
    
2. Start the Prometheus monitor in **server_config.yaml** and set the address and port number of Pushgateway:

    ```yaml
    metric:
      enable: true       # Set the value to true to enable the Prometheus monitor.
      address: 127.0.0.1 # Set the IP address of Pushgateway.
      port: 9091         # Set the port number of Pushgateway.
    ```

3. Go to the Prometheus root directory, and download starter [Prometheus configuration file](https://github.com/milvus-io/docs/blob/v{{var.release_version}}/assets/monitoring/prometheus.yml) for Milvus:

   ```shell
   $ wget https://raw.githubusercontent.com/milvus-io/docs/v{{var.release_version}}/assets/monitoring/prometheus.yml \ -O prometheus.yml
   ```

2. Configure the file to suit your requirements. Refer to [https://prometheus.io/docs/prometheus/latest/configuration/configuration/](https://prometheus.io/docs/prometheus/latest/configuration/configuration/) to learn more about the configuration file for Prometheus.

   > Note: If you use distributed cluster, you must expand the `targets` field to include `localhost: <http-port>` for each additional node in the cluster.

4. Download starter [alerting rules](https://github.com/milvus-io/docs/blob/v{{var.release_version}}/assets/monitoring/alert_rules.yml) for Milvus to the Prometheus root directory:

   ```shell
   wget -P rules https://raw.githubusercontent.com/milvus-io/docs/v{{var.release_version}}/assets/monitoring/alert_rules.yml
   ```

5. Edit the Prometheus configuration file according to your needs:

   - global: Configures parameters such as `scrape_interval` and `evaluation_interval`.

   ```yaml
   global:
     scrape_interval:     2s # Set the crawl time interval to 2s.
     evaluation_interval: 2s # Set the evaluation interval to 2s.
   ```

   - alerting: Sets the address and port of Alertmanager.

   ```yaml
   alerting:
   alertmanagers:
   - static_configs:
      - targets: ['localhost:9093']
   ```

   - rule_files: Specifys the file that defines the alerting rules.

   ```yaml
   rule_files:
      - "alert_rules.yml"
   ```

   - scrape_configs: Sets `job_name` and `targets` for scraping data.

   ```yaml
   scrape_configs:
   - job_name: 'prometheus'
      static_configs:
      - targets: ['localhost:9090']

   - job_name: 'pushgateway'
      honor_labels: true
      static_configs:
      - targets: ['localhost:9091']
   ```

   <div class="alert info">
    See <a href="https://prometheus.io/docs/prometheus/latest/configuration/configuration/">Prometheus Configuration</a> for more information about the configuration file of Prometheus.
   </div>
   
6. Start Prometheus:

    ```shell
    ./prometheus --config.file=prometheus.yml
    ```

### Configure Prometheus in Kubernetes

Start Pushgateway and Prometheus, and then open the monitoring option of the node configuration file **server_config.yaml** in the Kubernetes cluster and set the IP address and port number of Pushgateway.

```yaml
metric:
  enable: true       # Set the value to true to enable the Prometheus monitor.
  address: 127.0.0.1 # Set the IP address of Pushgateway.
  port: 9091         # Set the port number of Pushgateway.
```

### Visualize metrics in Grafana

1. Use the following command to install and start Grafana for your OS:

   ```shell
   $ docker run -i -p 3000:3000 grafana/grafana
   ```

2. Point your browser to `http://<hostname of machine running grafana>:3000` and log into the Grafana UI.

<div class="alert info">
Grafana's default username and password are both "admin". You can also create a new Grafana account.
</div>

3. [Add Prometheus as a data source](https://grafana.com/docs/grafana/latest/features/datasources/prometheus/).
   
4. In Grafana UI, click **Configuration > Data Sources > Prometheus**, and then configure the data source as follows:

   | Field   | Definition                                             |
   | :------ | :----------------------------------------------------- |
   | Name    | Prometheus                                             |
   | Default | True                                                   |
   | URL     | `http://<hostname of machine running prometheus>:9090` |
   | Access  | Browser                                                |

5. Download the starter [Grafana dashboard](https://github.com/milvus-io/docs/blob/v{{var.release_version}}/assets/monitoring/dashboard.json) for Milvus:

   ```shell
   $ wget https://raw.githubusercontent.com/milvus-io/docs/v{{var.release_version}}/assets/monitoring/dashboard.json
   ```

6. [Add the dashboard to Grafana](http://docs.grafana.org/reference/export_import/#importing-a-dashboard).

### Send notifications with Alertmanager

1. Download the [latest Alertmanager tarball](https://prometheus.io/download/#alertmanager) for your OS.

2. Make sure Alertmanager is installed successfully:

   ```shell
   $ alertmanager --version
   ```

   <div class="alert info">
   You can extract the binary and add it to your <code>PATH</code>. This makes it easy to start Alertmanager from any shell.
   </div>

3. Create the [Alertmanager configuration file](https://prometheus.io/docs/alerting/configuration/) to specify the desired receivers for notifications, and add it to Alertmanager root directory.

4. Start the Alertmanager server, with the `--config.file` flag pointing to the configuration file:

   ```shell
   alertmanager --config.file=simple.yml
   ```

5. Point your browser to `http://<hostname of machine running alertmanager>:9093`, where you can use the Alertmanager UI to define rules for [muting alerts](https://prometheus.io/docs/alerting/alertmanager/#silences).

## Related links

[Monitoring Metrics](../reference/monitoring_metrics.md)
