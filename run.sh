#!/bin/bash
set -eu -o pipefail

exec uvicorn conscious_canvas.main:app