FROM python:3.12-alpine AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:0.10.2 /uv /uvx /bin/

RUN apk update && apk add --no-cache \
    build-base \
    postgresql-dev \
    musl-dev \
    libffi-dev \
    openssl-dev

COPY pyproject.toml ./

ARG ENVIRONMENT=production
RUN if [ "$ENVIRONMENT" = "development" ]; then \
    uv pip install . --no-cache --system --group dev; \
    else \
    uv pip install . --no-cache --system; \
    fi

FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
