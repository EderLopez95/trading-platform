#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if ! command -v openssl >/dev/null 2>&1; then
  echo "openssl not found in PATH"
  exit 1
fi

if [[ ! -f root-ca.key || ! -f root-ca.pem ]]; then
  openssl genrsa -out root-ca.key 4096
  openssl req -x509 -new -nodes -key root-ca.key -sha256 -days 3650 -out root-ca.pem -subj "/CN=Trading-Platform-Root-CA"
fi

generate_service_cert() {
  local service_name="$1"
  local common_name="$2"
  local ext_file="$3"

  openssl genrsa -out "${service_name}.key" 2048
  openssl req -new -key "${service_name}.key" -out "${service_name}.csr" -subj "/CN=${common_name}"
  openssl x509 -req -in "${service_name}.csr" -CA root-ca.pem -CAkey root-ca.key -CAcreateserial -out "${service_name}.pem" -days 825 -sha256 -extfile "${ext_file}"
  rm -f "${service_name}.csr"
}

generate_service_cert "auth-service" "auth_service" "auth-service.ext"
generate_service_cert "signal-service" "signal_service" "signal-service.ext"
generate_service_cert "market-data-service" "market_data_service" "market-data-service.ext"

echo "Certificates generated in ${SCRIPT_DIR}"
