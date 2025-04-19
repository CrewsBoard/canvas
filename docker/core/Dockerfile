FROM python:3.10-slim as builder

ARG APP_NAME
ARG ENVIRONMENT
ENV APP_NAME=${APP_NAME}
ENV PYTHONPATH="/${APP_NAME}"
WORKDIR /${APP_NAME}

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    && PATH="/root/.local/bin:$PATH" uv --version

COPY .python-version .
COPY uv.lock .
COPY pyproject.toml .
COPY LICENSE .
COPY README.md .
COPY core/ core/
COPY shared/ shared/
COPY flow_engine/ flow_engine/

RUN PATH="/root/.local/bin:$PATH" && uv venv && . .venv/bin/activate && \
    uv pip install hatchling && \
    uv pip install .

ENV PATH="/${APP_NAME}/.venv/bin:$PATH"

EXPOSE 8000
