import json
import subprocess


def run() -> dict:
    try:
        result = subprocess.run(
            ["/usr/local/bin/speedtest", "--accept-license", "--accept-gdpr", "--format=json", "--selection-details"],
            capture_output=True, text=True, check=True
        )

        speedtest_data = json.loads(result.stdout)
        return speedtest_data

    except Exception:
        return None


def ping(target: str, timeout_ms: int=300) -> float:
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-W", str(timeout_ms), target],
            capture_output=True, text=True, check=True
        )

        latency = result.stdout.split("time=", 1)[1].split(" ", 1)[0]
        return float(latency)

    except Exception:
        return None
