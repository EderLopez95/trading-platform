#!/bin/sh
set -e

# Generate the runtime configuration consumed by the SPA (see web/public/config.js).
# This runs on container start via the nginx image's /docker-entrypoint.d hook,
# so a single build can target multiple environments by setting API_URL.

CONFIG_FILE="/usr/share/nginx/html/config.js"

cat > "$CONFIG_FILE" <<EOF
window.__APP_CONFIG__ = {
  API_URL: "${API_URL:-http://localhost:8080}",
};
EOF

echo "Generated ${CONFIG_FILE} with API_URL=${API_URL:-http://localhost:8080}"
