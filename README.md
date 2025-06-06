# ookla-speedtest-exporter
A simple Prometheus exporter for Ookla Speedtest CLI

### Description
This is a very basic Prometheus exporter for [Ookla Speedtest](https://www.speedtest.net/apps/cli) that runs periodic speedtests and returns results.  

## Usage
The exporter is configured using environment variables.  
Every variable has a default value, so you can just run the exporter without setting any of them, if you want.

| Variable             | Description                             | Default       |
|----------------------|-----------------------------------------|---------------|
| `PROMETHEUS_PORT`    | Port the exporter listens on            | `8000`        |
| `PROMETHEUS_PREFIX`  | Prefix for the Prometheus metrics       | `"speedtest"` |
| `SPEEDTEST_INTERVAL` | Interval between speedtests in seconds  | `3600`        |
| `PING_INTERVAL`      | Interval between pings in seconds       | `60`          |
| `PING_TARGETS`       | Comma-separated list of targets to ping | `""`          |

## Docker
The exporter is available as a Docker image on the [GitHub Container Registry](https://ghcr.io/pesaventofilippo/ookla-speedtest-exporter).

To run the exporter using Docker, you can use the following command:
```bash
docker run -d -p 8000:8000 \
    ghcr.io/pesaventofilippo/ookla-speedtest-exporter
```

### docker compose
You can also use `docker compose` to run the exporter.
Here is an example `compose.yml` file:
```yaml
services:
  ookla-speedtest-exporter:
    image: ghcr.io/pesaventofilippo/ookla-speedtest-exporter
    ports:
      - 8000:8000
```
