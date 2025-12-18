########################
# Stage 1: Builder
########################
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


########################
# Stage 2: Runtime
########################
FROM python:3.11-slim

# Set timezone to UTC (CRITICAL)
ENV TZ=UTC

WORKDIR /app

# Install system dependencies (cron + tzdata)
RUN apt-get update && \
    apt-get install -y cron tzdata && \
    ln -sf /usr/share/zoneinfo/UTC /etc/localtime && \
    echo "UTC" > /etc/timezone && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy python deps from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY app ./app
COPY scripts ./scripts
COPY cron /etc/cron.d

# Fix cron permissions
RUN chmod 0644 /etc/cron.d/2fa-cron && \
    crontab /etc/cron.d/2fa-cron

# Create volume mount points
RUN mkdir -p /data /cron && chmod 755 /data /cron

EXPOSE 8080

# Start cron + API
CMD cron && python -m uvicorn app.main:app --host 0.0.0.0 --port 8080
