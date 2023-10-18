# Build stage
FROM ubuntu:22.04 AS builder

# Avoid stuck build due to user prompt
ARG DEBIAN_FRONTEND=noninteractive

# Install updates and Python
RUN apt-get update && apt-get install --no-install-recommends -y python3.10 python3.10-dev python3.10-venv python3-pip python3-wheel build-essential && \
  apt-get clean && rm -rf /var/lib/apt/lists/*

# Install requirements
ENV PIPX_HOME=/opt/pipx
ENV PIPX_BIN_DIR=/usr/local/bin

WORKDIR /app
COPY . /app

RUN script/bootstrap && rm -rf ~/.cache/pip

# Runtime stage
FROM ubuntu:22.04 AS runtime
ENV ENVIRONMENT=production

# Install updates and Python
RUN apt-get update && apt-get install --no-install-recommends -y python3.10 python3-venv && \
  apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy binaries and app code from builder image
COPY --from=builder /opt/pipx /opt/pipx
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /app /app
WORKDIR /app

# Make sure all messages always reach console
ENV PYTHONUNBUFFERED=1

# Run it
CMD ["script/server"]