ARG ENVIRONMENT="production"

# Build stage
FROM python:3.13-bullseye AS builder
ARG ENVIRONMENT
ENV ENVIRONMENT=$ENVIRONMENT

# Install requirements
RUN pip install poetry==2.1.2

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN --mount=type=cache,target=$POETRY_CACHE_DIR [ $ENVIRONMENT = development ] && poetry install --with dev || poetry install

# Runtime stage
FROM python:3.13-slim-bullseye AS runtime
ARG ENVIRONMENT
ENV ENVIRONMENT=$ENVIRONMENT

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

WORKDIR /app
COPY . ./

CMD ["script/server"]