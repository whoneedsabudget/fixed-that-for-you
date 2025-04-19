# Build stage
FROM ubuntu:24.10 AS builder

# Avoid stuck build due to user prompt
ARG DEBIAN_FRONTEND=noninteractive

# Install updates and Python
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    rm -rf /var/lib/apt/lists/*
RUN add-apt-repository "deb https://ppa.launchpadcontent.net/deadsnakes/ppa/ubuntu noble main"
RUN apt-get update && apt-get install --no-install-recommends -y python3.13 python3.13-dev python3.13-venv python3-pip python3-wheel pipx build-essential && \
  apt-get clean && rm -rf /var/lib/apt/lists/*

# Install requirements
WORKDIR /app
COPY . /app

RUN script/bootstrap
RUN rm -f /root/.local/state/pipx/log/*.log

# Runtime stage
FROM ubuntu:24.10 AS runtime
ENV ENVIRONMENT=production

# Install updates and Python
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    rm -rf /var/lib/apt/lists/*
RUN add-apt-repository "deb https://ppa.launchpadcontent.net/deadsnakes/ppa/ubuntu noble main"
RUN apt-get update && apt-get install --no-install-recommends -y python3.13 python3-venv pipx && \
  apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy binaries and app code from builder image
COPY --from=builder /root/.local /root/.local
COPY --from=builder /app /app
WORKDIR /app

# Make sure all messages always reach console
ENV PYTHONUNBUFFERED=1

# Run it
CMD ["script/server"]