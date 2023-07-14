#!/bin/bash
set -eu -o pipefail

exec uvicorn \
  --host 0.0.0.0 \
  --ssl-keyfile /home/aleks/certs/conscious_canvas.local.key \
  --ssl-certfile /home/aleks/certs/conscious_canvas.local.crt \
  conscious_canvas.main:app
