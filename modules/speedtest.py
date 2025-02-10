import json
import subprocess


def _run_cmd(args: list[str]) -> dict:
    try:
        result = subprocess.run(
            ["/usr/local/bin/speedtest", "--accept-license", "--accept-gdpr", "--format=json", *args],
            capture_output=True,
            text=True,
            check=True
        )

        speedtest_data = json.loads(result.stdout)
        return speedtest_data

    except Exception:
        return None


def run() -> dict:
    return _run_cmd(["--selection-details"])


def list_servers() -> dict:
    return _run_cmd(["--servers"])
