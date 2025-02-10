from modules import speedtest
from modules.utils import env
import prometheus_client as prom
from http.server import HTTPServer, BaseHTTPRequestHandler

METRICS = {
    "ping": prom.Gauge("ping", "Ping (ms)",
                       namespace=env.PROMETHEUS_PREFIX, unit="ms"),
    "jitter": prom.Gauge("jitter", "Jitter (ms)",
                         namespace=env.PROMETHEUS_PREFIX, unit="ms"),
    "download_speed": prom.Gauge("download_speed", "Download speed (bits per second)",
                                    namespace=env.PROMETHEUS_PREFIX, unit="bps"),
    "downloaded_bytes": prom.Counter("downloaded_bytes", "Total downloaded bytes",
                                        namespace=env.PROMETHEUS_PREFIX, unit="bytes"),
    "upload_speed": prom.Gauge("upload_speed", "Upload speed (bits per second)",
                                namespace=env.PROMETHEUS_PREFIX, unit="bps"),
    "uploaded_bytes": prom.Counter("uploaded_bytes", "Total uploaded bytes",
                                    namespace=env.PROMETHEUS_PREFIX, unit="bytes"),
    "packet_loss": prom.Gauge("packet_loss", "Packet loss percent",
                                namespace=env.PROMETHEUS_PREFIX, unit="percent"),
    "server_pings": prom.Gauge("server_pings", "List of server pings (ms)",
                               labelnames=["server_id", "host", "name", "location"],
                               namespace=env.PROMETHEUS_PREFIX, unit="ms"),
    "failed_tests": prom.Counter("failed_tests", "Number of failed tests",
                                    namespace=env.PROMETHEUS_PREFIX)
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
    METRICS["packet_loss"].set(st["packetLoss"])

    for entry in st["serverSelection"]["servers"]:
        server = entry["server"]
        METRICS["server_pings"].labels(
            server_id=server["id"],
            host=server["host"],
            name=server["name"],
            location=server["location"]
        ).set(entry["latency"])


class MetricsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/metrics":
            run_speedtest()

            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(prom.generate_latest())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")

    # Disable logging
    def log_message(self, format, *args):
        return


if __name__ == "__main__":
    prom.disable_created_metrics()
    prom.REGISTRY.unregister(prom.PROCESS_COLLECTOR)
    prom.REGISTRY.unregister(prom.PLATFORM_COLLECTOR)
    prom.REGISTRY.unregister(prom.GC_COLLECTOR)

    server = HTTPServer(("0.0.0.0", env.PROMETHEUS_PORT), MetricsHandler)
    server.serve_forever()
