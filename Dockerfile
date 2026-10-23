
########################################################################################################################
# Base stage, includes uv
########################################################################################################################
FROM python:3.11-alpine3.24@sha256:5fb4bc53dd0180955e31e5245b648bbb24a4ac4ab03a1de81513642325220bcd AS base

# Copy uv + uvx binaries
COPY --from=ghcr.io/astral-sh/uv:0.13.5@sha256:32a7bb39b496babbd997b0a39a4d66c126bdaf5661b302bf6f06abda8deca6ff /uv /uvx /bin/

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1
# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy
# Disable use of uv-managed Python versions
ENV UV_NO_MANAGED_PYTHON=1
# Disable Python downloads so that the system interpreter is used across images
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /datagateway-api-run

COPY pyproject.toml uv.lock README.md ./

########################################################################################################################
# Stage for local development
########################################################################################################################
FROM base AS dev

RUN --mount=type=cache,target=/root/.cache/uv \
    set -eux; \
    # Lock and install all dependencies but do not install the project \
    uv sync --locked --no-install-project

COPY datagateway_api/ datagateway_api/

RUN --mount=type=cache,target=/root/.cache/uv \
    set -eux; \
    # Install the project \
    uv sync --locked


CMD ["/datagateway-api-run/.venv/bin/fastapi", "dev", "datagateway_api/main.py", "--host", "0.0.0.0", "--port", "8000"]

EXPOSE 8000

########################################################################################################################
# Stage for testing, linting and formatting development
########################################################################################################################
FROM dev AS test

COPY util/ util/
COPY test/ test/
COPY .flake8 .flake8
COPY .env.example .env 
COPY logging.example.ini logging.ini  

# Create local config files from examples only if they do not already exist.
# This avoids overwriting repository or environment-specific settings.
RUN if [ ! -f datagateway_api/search_api_mapping.json ]; then \
        cp datagateway_api/search_api_mapping.json.example datagateway_api/search_api_mapping.json; \
    fi

CMD []


########################################################################################################################
# Stage for production-ready build of the project
########################################################################################################################
FROM base AS prod-build

# Omit development dependencies
ENV UV_NO_DEV=1

RUN --mount=type=cache,target=/root/.cache/uv \
    set -eux; \
     # Lock and install all dependencies but do not install the project \
    uv sync --locked --no-install-project

COPY datagateway_api/ datagateway_api/

RUN --mount=type=cache,target=/root/.cache/uv \
    set -eux; \
    # Install the project \
    uv sync --locked

########################################################################################################################
# Minimal production-ready image
########################################################################################################################
FROM python:3.11-alpine3.24@sha256:5fb4bc53dd0180955e31e5245b648bbb24a4ac4ab03a1de81513642325220bcd AS prod

WORKDIR /datagateway-api-run
ENV WORKERS=1

# Copy the application from the prod-build stage
COPY --from=prod-build /datagateway-api-run /datagateway-api-run

RUN set -eux; \
    \
    # Create a non-root user to run as \
    addgroup -S datagateway-api; \
    adduser -S -D -G datagateway-api -H -h /datagateway-api-run datagateway-api;

USER datagateway-api

CMD exec /datagateway-api-run/.venv/bin/fastapi run datagateway_api/main.py --workers=$WORKERS --host=0.0.0.0 --port=8000

EXPOSE 8000
