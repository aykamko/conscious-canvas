#!/bin/bash
set -eu -o pipefail

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

exec uvicorn \
  --host 0.0.0.0 \
  --ssl-keyfile "$SCRIPT_DIR/certs/192.168.4.85-key.pem" \
  --ssl-certfile "$SCRIPT_DIR/certs/192.168.4.85.pem" \
  conscious_canvas.main:app
