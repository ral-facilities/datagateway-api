#!/bin/sh -eu

# Use a tempfile instead of sed -i so that only the file, not the directory needs to be writable
TEMPFILE="$(mktemp)"

# Set values in config.yaml from environment variables
# No quotes for icat_check_cert because it's boolean
sed -e "s|icat_url: \".*\"|icat_url: \"$ICAT_URL\"|" \
    -e "s|icat_check_cert: .*|icat_check_cert: $ICAT_CHECK_CERT|" \
    -e "s|log_location: \".*\"|log_location: \"$LOG_LOCATION\"|" \
    datagateway_api/config.yaml > "$TEMPFILE"

cat "$TEMPFILE" > datagateway_api/config.yaml
rm "$TEMPFILE"

# Run the CMD instruction
exec "$@"
