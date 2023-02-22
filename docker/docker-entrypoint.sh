#!/bin/sh

# Set values in config.yaml from environment variables
sed -i "s|icat_url: \".*\"|icat_url: \"$ICAT_URL\"|" /datagateway-api-run/config.yaml
sed -i "s|icat_check_cert: \".*\"|icat_check_cert: \"$ICAT_CHECK_CERT\"|" /datagateway-api-run/config.yaml
sed -i "s|log_location: .*|log_location: $LOG_LOCATION|" /datagateway-api-run/config.yaml

# Run the CMD instruction
exec "$@"
