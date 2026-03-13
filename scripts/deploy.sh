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

DEPLOY_PATH="${PI_DEPLOY_PATH:-/home/${PI_USER}/piness}"
SSH_OPTS="-o StrictHostKeyChecking=no"

# Use sshpass if PI_PASSWORD is set, otherwise plain ssh (key-based)
if [ -n "${PI_PASSWORD:-}" ]; then
    SSH_CMD="sshpass -p ${PI_PASSWORD} ssh ${SSH_OPTS}"
    RSYNC_SSH="sshpass -p ${PI_PASSWORD} ssh ${SSH_OPTS}"
else
    SSH_CMD="ssh ${SSH_OPTS}"
    RSYNC_SSH="ssh ${SSH_OPTS}"
fi

echo "Deploying to ${PI_USER}@${PI_HOST}:${DEPLOY_PATH}"

# Create deploy directory and venv if needed
$SSH_CMD ${PI_USER}@${PI_HOST} "mkdir -p ${DEPLOY_PATH}"

# Sync project files preserving directory structure
rsync -avz --delete \
    --exclude '.venv' \
    --exclude '__pycache__' \
    --exclude '.env' \
    --exclude '.git' \
    -e "${RSYNC_SSH}" \
    "$PROJECT_ROOT/src" \
    "$PROJECT_ROOT/pyproject.toml" \
    "$PROJECT_ROOT/scripts" \
    "${PI_USER}@${PI_HOST}:${DEPLOY_PATH}/"

# Install/update deps on Pi if pyproject.toml changed
echo "Installing dependencies on Pi..."
$SSH_CMD ${PI_USER}@${PI_HOST} "cd ${DEPLOY_PATH} && \
    python3 -m venv --system-site-packages venv 2>/dev/null || true && \
    venv/bin/pip install -e '.[rpi]' 2>&1 | tail -3"

echo "Deploy complete."
