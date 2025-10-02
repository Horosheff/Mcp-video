#!/bin/bash

echo "==================================="
echo "WordPress MCP Server - Uninstall"
echo "==================================="
echo ""
echo "⚠️  WARNING: This will completely remove the MCP server!"
echo ""
read -p "Are you sure you want to continue? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "Uninstall cancelled."
    exit 0
fi

echo ""
echo "Starting uninstall process..."

# Stop and disable systemd service
echo "Step 1: Stopping systemd service..."
sudo systemctl stop wordpress-mcp-server 2>/dev/null
sudo systemctl disable wordpress-mcp-server 2>/dev/null

# Remove systemd service file
echo "Step 2: Removing systemd service file..."
sudo rm -f /etc/systemd/system/wordpress-mcp-server.service
sudo systemctl daemon-reload

# Stop Cloudflare Tunnel
echo "Step 3: Stopping Cloudflare Tunnel..."
pkill cloudflared

# Remove Cloudflare binary (optional)
read -p "Remove Cloudflare Tunnel binary? (yes/no): " REMOVE_CF
if [ "$REMOVE_CF" = "yes" ]; then
    sudo rm -f /usr/local/bin/cloudflared
    rm -f /root/cloudflared.log
    echo "Cloudflare Tunnel removed."
fi

# Remove project directory
echo "Step 4: Removing project directory..."
if [ -d "/opt/wordpress-mcp-server" ]; then
    sudo rm -rf /opt/wordpress-mcp-server
    echo "Project directory removed."
fi

# Remove firewall rule
read -p "Remove firewall rule for port 8000? (yes/no): " REMOVE_FW
if [ "$REMOVE_FW" = "yes" ]; then
    sudo ufw delete allow 8000/tcp 2>/dev/null
    echo "Firewall rule removed."
fi

echo ""
echo "==================================="
echo "✅ Uninstall complete!"
echo "==================================="
echo ""
echo "The following were removed:"
echo "  - Systemd service"
echo "  - Project files"
if [ "$REMOVE_CF" = "yes" ]; then
    echo "  - Cloudflare Tunnel"
fi
if [ "$REMOVE_FW" = "yes" ]; then
    echo "  - Firewall rule"
fi
echo ""

