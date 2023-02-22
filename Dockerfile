# Dockerfile to build and serve datagateway-api

# Build stage
FROM python:3.11-alpine3.17 as builder

WORKDIR /datagateway-api-build

COPY README.md poetry.lock pyproject.toml ./
COPY datagateway_api/ datagateway_api/

RUN --mount=type=cache,target=/root/.cache \
    set -eux; \
    \
    python3 -m pip install 'poetry~=1.3.2'; \
    poetry build;


# Install & run stage
FROM python:3.11-alpine3.17

WORKDIR /datagateway-api-run

COPY --from=builder /datagateway-api-build/dist/datagateway_api-*.whl /tmp/

RUN --mount=type=cache,target=/root/.cache \
    set -eux; \
    \
    python3 -m pip install \
        'gunicorn~=20.1.0' \
        /tmp/datagateway_api-*.whl; \
    \
    DATAGATEWAY_API_LOCATION="$(python3 -m pip show datagateway_api | awk '/^Location:/ { print $2 }')"; \
    \
    # Create search_api_mapping.json from its .example file \
    cp "$DATAGATEWAY_API_LOCATION/datagateway_api/search_api_mapping.json.example" "$DATAGATEWAY_API_LOCATION/datagateway_api/search_api_mapping.json"; \
    \
    # Create config.yaml from its .example file. It will need to be editted by the entrypoint script so create it in our non-root user's home directory and create a symlink \
    cp "$DATAGATEWAY_API_LOCATION/datagateway_api/config.yaml.example" /datagateway-api-run/config.yaml; \
    ln -s /datagateway-api-run/config.yaml "$DATAGATEWAY_API_LOCATION/datagateway_api/config.yaml"; \
    \
    # Create a non-root user to run as \
    addgroup -S datagateway-api; \
    adduser -S -D -G datagateway-api -H -h /datagateway-api-run datagateway-api; \
    chown -R datagateway-api:datagateway-api /datagateway-api-run;

USER datagateway-api

ENV ICAT_URL="http://localhost"
ENV ICAT_CHECK_CERT="true"
ENV LOG_LOCATION="/dev/stdout"

COPY docker/docker-entrypoint.sh /usr/local/bin/
ENTRYPOINT ["docker-entrypoint.sh"]

# Serve the application using gunicorn - production ready WSGI server
CMD ["gunicorn", "-b", "0.0.0.0:8000", "datagateway_api.wsgi"]
EXPOSE 8000
