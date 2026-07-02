#!/bin/bash
set -e

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "==> Updating repository..."
git -C "$REPO_DIR" pull

echo "==> Building frontend..."
cd "$REPO_DIR/frontend"
npm install
npm run build

echo "==> Updating Python dependencies..."
cd "$REPO_DIR/backend"
source venv/bin/activate
pip install -r requirements.txt

echo "==> Restarting Gunicorn..."
sudo systemctl restart gunicorn

echo "==> Checking services..."
sudo systemctl is-active gunicorn nginx

echo ""
echo "Deployment complete!"
