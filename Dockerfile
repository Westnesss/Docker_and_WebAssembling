# syntax=docker/dockerfile:1
# ------------------------------------------------------------------
# Docker Container PoC - FICA UCE
# Multi-stage build on python:3.11-alpine (small, secure, non-root)
# ------------------------------------------------------------------

# ---------- Stage 1: builder ----------
FROM python:3.11-alpine AS builder
WORKDIR /build
COPY app/ ./app/
# Byte-compile the code: the build fails early if there is a syntax error
RUN python -m compileall -q app/

# ---------- Stage 2: runtime ----------
FROM python:3.11-alpine
LABEL org.opencontainers.image.title="docker-poc" \
      org.opencontainers.image.description="Docker Container PoC - FICA UCE" \
      org.opencontainers.image.version="1.0.0"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

# Create an unprivileged user
RUN addgroup -S appgroup && adduser -S -G appgroup appuser

WORKDIR /app
COPY --from=builder --chown=appuser:appgroup /build/app/ ./

USER appuser
EXPOSE 8080

HEALTHCHECK --interval=15s --timeout=3s --start-period=5s --retries=3 \
  CMD wget -qO- http://127.0.0.1:8080/health || exit 1

CMD ["python", "server.py"]
