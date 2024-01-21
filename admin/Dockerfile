FROM python:3.10.13-alpine3.18

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=0 \
    POETRY_HOME="/etc/poetry" \
    POETRY_CACHE_DIR="/tmp/poetry_cache" \
    POETRY_VERSION=1.7.0

# Install build dependencies
RUN apk update && apk add --no-cache libffi libffi-dev gcc g++ musl-dev

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir "poetry==$POETRY_VERSION" \
    && poetry install --without bot --without dev --no-root \
    && pip uninstall -y poetry \
    # Clean up unnecessary packages and cache
    && apk del gcc g++ musl-dev \
    && rm -rf /root/.cache \
    && rm -rf $POETRY_CACHE_DIR \
    && rm -rf /usr/src/app/__pycache__ \
    && adduser -D appuser \
    && chown -R appuser:appuser .

USER appuser

CMD ["gunicorn", "-c", "admin/gunicorn_conf.py"]
