#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Load environment
if [ -f "$PROJECT_ROOT/.env" ]; then
    set -a
    source "$PROJECT_ROOT/.env"
    set +a
else
    echo "Error: .env file not found at $PROJECT_ROOT/.env" >&2
    exit 1
fi

if [ -z "${PI_HOST:-}" ] || [ -z "${PI_USER:-}" ]; then
    echo "Error: PI_HOST and PI_USER must be set in .env" >&2
    exit 1
fi

DEPLOY_PATH="${PI_DEPLOY_PATH:-/home/pi/piness}"

echo "Deploying to ${PI_USER}@${PI_HOST}:${DEPLOY_PATH}"

rsync -avz --delete \
    "$PROJECT_ROOT/src/" \
    "$PROJECT_ROOT/pyproject.toml" \
    "$PROJECT_ROOT/scripts/" \
    "${PI_USER}@${PI_HOST}:${DEPLOY_PATH}/"

echo "Deploy complete."
