
########################################################################################################################
# Base stage, includes uv
########################################################################################################################
FROM python:3.11-alpine3.17 AS base

# Copy uv + uvx binaries
COPY --from=ghcr.io/astral-sh/uv:0.10.8 /uv /uvx /bin/


# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1
# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy
# Disable use of uv-managed Python versions
ENV UV_NO_MANAGED_PYTHON=1
# Disable Python downloads so that the system interpreter is used across images
ENV UV_PYTHON_DOWNLOADS=0
# Add timezone configuration - https://github.com/regebro/tzlocal/issues/70
ENV TZ=UTC

WORKDIR /app

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


CMD ["fastapi", "dev", "datagateway_api/main.py", "--host", "0.0.0.0", "--port", "8000"]

EXPOSE 8000

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
FROM python:3.11-alpine3.17 AS prod

WORKDIR /datagateway-api-run

# Copy the application from the prod-build stage
COPY --from=prod-build /app /datagateway-api-run


RUN set -eux; \
    \
    # Create config.yaml and search_api_mapping.json from their .example files \
    cp datagateway_api/config.yaml.example datagateway_api/config.yaml; \
    cp datagateway_api/search_api_mapping.json.example datagateway_api/search_api_mapping.json; \
    cp datagateway_api/logging.example.ini datagateway_api/logging.ini; \
    \
    # Create a non-root user to run as \
    addgroup -S datagateway-api; \
    adduser -S -D -G datagateway-api -H -h /datagateway-api-run datagateway-api; \
    \
    # Change ownership of settings location - the entrypoint script will need to edit it \
    chown -R datagateway-api:datagateway-api datagateway_api/

    
USER datagateway-api

ENV ICAT_URL="http://localhost"
ENV ICAT_CHECK_CERT="false"

COPY docker/docker-entrypoint.sh /usr/local/bin/
ENTRYPOINT ["docker-entrypoint.sh"]

CMD ["fastapi", "run", "datagateway_api/main.py", "--host", "0.0.0.0", "--port", "8000"]

EXPOSE 8000
