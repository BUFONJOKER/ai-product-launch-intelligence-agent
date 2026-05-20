# --- Stage 1: Build ---
FROM python:3.11-slim-bookworm AS builder

# Install PostgreSQL build dependencies for psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv binaries from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory and environment variables
WORKDIR /app
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

# Install dependencies first (for better Docker caching)
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# --- Stage 2: Runtime ---
FROM python:3.11-slim-bookworm

WORKDIR /app

# Keep runtime small and deterministic
ENV PATH="/app/.venv/bin:$PATH" \
    HOST="0.0.0.0" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Copy only the virtual environment and the code required at runtime
COPY --from=builder /app/.venv /app/.venv
COPY __init__.py ./
COPY main.py ./
COPY config.py ./
COPY api ./api
COPY agent ./agent

# Run the application
CMD ["python", "-m", "main"]
