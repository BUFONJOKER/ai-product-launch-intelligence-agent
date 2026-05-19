FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System dependencies for PostgreSQL drivers and building wheels when needed.
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv and dependencies from lockfile for reproducible builds.
RUN python -m pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./

RUN uv export --frozen --no-dev --no-emit-project --format requirements-txt > requirements.lock.txt \
    && uv pip install --system --no-cache -r requirements.lock.txt \
    && rm requirements.lock.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
