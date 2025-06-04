import os

class EnvironmentConfig:
    def __init__(self):
        self.PROMETHEUS_PORT = int(os.getenv("PROMETHEUS_PORT", "8000"))
        self.PROMETHEUS_PREFIX = os.getenv("PROMETHEUS_PREFIX", "speedtest")
        self.SPEEDTEST_INTERVAL = int(os.getenv("SPEEDTEST_INTERVAL", "3600"))
        self.PING_INTERVAL = int(os.getenv("PING_INTERVAL", "60"))
        self.PING_TARGETS = os.getenv("PING_TARGETS", "").split(",")


env = EnvironmentConfig()
