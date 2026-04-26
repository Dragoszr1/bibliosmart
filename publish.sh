#!/bin/bash
set -e

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "==> Building frontend..."
cd "$REPO_DIR/frontend"
npm run build

echo "==> Copying Nginx config..."
sudo cp "$REPO_DIR/biblioteca.nginx.conf" /etc/nginx/sites-available/biblioteca
sudo cp "$HOME/.cloudflared/config.yml" /etc/cloudflared/config.yml 2>/dev/null || true

echo "==> Restarting services..."
sudo systemctl restart biblioteca
sudo systemctl restart nginx
sudo systemctl start cloudflared

echo "==> Status:"
sudo systemctl is-active biblioteca nginx cloudflared

echo ""
echo "Site is LIVE at https://bibliosmart.online"
