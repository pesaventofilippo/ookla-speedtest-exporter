from time import sleep
from threading import Thread
from modules import speedtest
from modules.utils import env
import prometheus_client as prom

METRICS = {
    "ping": prom.Gauge(
        name="ping", documentation="Latest Ping (ms)",
        namespace=env.PROMETHEUS_PREFIX, unit="ms"
    ),
    "jitter": prom.Gauge(
        name="jitter", documentation="Latest Jitter (ms)",
        namespace=env.PROMETHEUS_PREFIX, unit="ms"
    ),
    "download_speed": prom.Gauge(
        name="download_speed", documentation="Latest Download speed (bits per second)",
        namespace=env.PROMETHEUS_PREFIX, unit="bps"
    ),
    "downloaded_bytes": prom.Counter(
        name="downloaded_bytes", documentation="Total downloaded bytes",
        namespace=env.PROMETHEUS_PREFIX, unit="bytes"
    ),
    "upload_speed": prom.Gauge(
        name="upload_speed", documentation="Latest Upload speed (bits per second)",
        namespace=env.PROMETHEUS_PREFIX, unit="bps"
    ),
    "uploaded_bytes": prom.Counter(
        name="uploaded_bytes", documentation="Total uploaded bytes",
        namespace=env.PROMETHEUS_PREFIX, unit="bytes"
    ),
    "packet_loss": prom.Gauge(
        name="packet_loss", documentation="Latest Packet loss (percent)",
        namespace=env.PROMETHEUS_PREFIX, unit="percent"
    ),
    "server_ping": prom.Gauge(
        name="server_ping", documentation="List of server pings (ms)",
        labelnames=["server_id", "host", "name", "location"], namespace=env.PROMETHEUS_PREFIX, unit="ms"
    ),
    "failed_tests": prom.Counter(
        name="failed_tests", documentation="Number of failed tests",
        namespace=env.PROMETHEUS_PREFIX
    )
}


def run_speedtest():
    st = speedtest.run()
    if st is None:
        METRICS["failed_tests"].inc()
        return

    METRICS["ping"].set(st["ping"]["latency"])
    METRICS["jitter"].set(st["ping"]["jitter"])
    METRICS["download_speed"].set(st["download"]["bandwidth"]*8)
    METRICS["downloaded_bytes"].inc(st["download"]["bytes"])
    METRICS["upload_speed"].set(st["upload"]["bandwidth"]*8)
    METRICS["uploaded_bytes"].inc(st["upload"]["bytes"])
    METRICS["packet_loss"].set(st.get("packetLoss", 0))

    for entry in st["serverSelection"]["servers"]:
        if entry.get("latency") is None:
            continue

        server = entry["server"]
        METRICS["server_ping"].labels(
            server_id=server["id"],
            host=server["host"],
            name=server["name"],
            location=server["location"]
        ).set(entry["latency"])


def speedtest_loop():
    while True:
        run_speedtest()
        sleep(env.SPEEDTEST_INTERVAL)


if __name__ == "__main__":
    prom.disable_created_metrics()
    prom.REGISTRY.unregister(prom.GC_COLLECTOR)
    prom.REGISTRY.unregister(prom.PROCESS_COLLECTOR)
    prom.REGISTRY.unregister(prom.PLATFORM_COLLECTOR)

    Thread(target=speedtest_loop, daemon=True).start()
    _, web_thread = prom.start_http_server(addr="0.0.0.0", port=env.PROMETHEUS_PORT)
    web_thread.join()
