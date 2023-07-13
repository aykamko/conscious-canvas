#!/bin/bash
set -eu -o pipefail

exec uvicorn --host 0.0.0.0 conscious_canvas.main:app
