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

echo "==> Updating services..."
sudo cp "$REPO_DIR/biblioteca.service" /etc/systemd/system/biblioteca.service
sudo cp "$REPO_DIR/biblioteca.nginx.conf" /etc/nginx/sites-available/biblioteca.conf
sudo systemctl daemon-reload

echo "==> Restarting Gunicorn (Biblioteca)..."
sudo systemctl restart biblioteca
sudo systemctl stop gunicorn || true  # Stop the wrong service if it's running

echo "==> Checking services..."
sudo systemctl reload nginx
sudo systemctl is-active biblioteca nginx

echo ""
echo "Deployment complete!"
