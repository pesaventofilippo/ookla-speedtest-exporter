FROM python:3.12-alpine

WORKDIR /app
ARG TARGETARCH

# Install Ookla Speedtest CLI
RUN apk add --no-cache curl tar
RUN case "$TARGETARCH" in \
        "amd64") BINARY_URL="https://install.speedtest.net/app/cli/ookla-speedtest-1.2.0-linux-x86_64.tgz" ;; \
        "386")   BINARY_URL="https://install.speedtest.net/app/cli/ookla-speedtest-1.2.0-linux-i386.tgz" ;; \
        "arm64") BINARY_URL="https://install.speedtest.net/app/cli/ookla-speedtest-1.2.0-linux-aarch64.tgz" ;; \
        "arm")   BINARY_URL="https://install.speedtest.net/app/cli/ookla-speedtest-1.2.0-linux-armhf.tgz" ;; \
        *) echo "Unsupported architecture: $TARGETARCH" && exit 1 ;; \
    esac \
    && curl -L "$BINARY_URL" | tar xz -C /usr/local/bin \
    && chmod +x /usr/local/bin/speedtest

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python", "main.py"]
