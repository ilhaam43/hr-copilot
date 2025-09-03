#!/usr/bin/env bash
set -euo pipefail
LOG_DIR="${LOG_DIR:-$HOME/hrcopilot/logs}"

echo "==> Stop Backend AI"
if [[ -f "$LOG_DIR/ai.pid" ]]; then
  kill -15 "$(cat "$LOG_DIR/ai.pid")" 2>/dev/null || true
  rm -f "$LOG_DIR/ai.pid"
fi
# jaga-jaga bila masih ada proses di port default
lsof -t -iTCP:8001 -sTCP:LISTEN | xargs -r kill -15 || true

echo "==> Stop containers (Qdrant & Presidio)"
docker stop qdrant presidio 2>/dev/null || true
echo "Done. Cek dengan: docker ps"
