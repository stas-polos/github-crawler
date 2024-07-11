ARG PYTHON_IMAGE_VERSION
ARG POETRY_HOME='/root/.local/pypoetry'
ARG POETRY_CACHE_DIR='/tmp/poetry_cache'
ARG VIRTUALENV='/app/.venv'

FROM python:${PYTHON_IMAGE_VERSION} as builder

ARG POETRY_HOME
ARG POETRY_CACHE_DIR
ARG VIRTUALENV

ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=on \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.7.1 \
    POETRY_HOME=$POETRY_HOME \
    POETRY_CACHE_DIR=$POETRY_CACHE_DIR \
    VIRTUALENV=$VIRTUALENV \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1

RUN apt-get update -yq \
    && apt-get install -yq --no-install-recommends \
    curl \
    ; \
    # installing poetry: https://github.com/python-poetry/poetry
    curl -sSL https://install.python-poetry.org | python - \
    # cleaning cache
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="$POETRY_HOME/bin:$VIRTUALENV/bin:$PATH"

WORKDIR /app
COPY pyproject.toml poetry.lock /app/

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --only main --no-root

# 'development' stage installs all dev deps and can be used to develop code.
FROM builder as development

RUN poetry install --only dev --no-root && rm -rf $POETRY_CACHE_DIR

COPY scripts/ /app/scripts
COPY tests/ /app/tests
COPY src/ /app/src

# `production` image used for runtime (without poetry, only virtualenv)
FROM python:${PYTHON_IMAGE_VERSION} as production

ARG VIRTUALENV

ENV PATH="$VIRTUALENV/bin:$PATH"

COPY --from=builder $VIRTUALENV $VIRTUALENV

WORKDIR /app
COPY src/ /app/src/
