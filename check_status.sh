#!/bin/bash

echo "==================================="
echo "WordPress MCP Server - Status Check"
echo "==================================="

# Check if systemd service is running
echo ""
echo "1. Systemd Service Status:"
echo "-----------------------------------"
sudo systemctl status wordpress-mcp-server --no-pager | grep -E "Active:|Loaded:|Main PID:"

# Check if server responds
echo ""
echo "2. Server Health Check:"
echo "-----------------------------------"
HEALTH=$(curl -s http://localhost:8000/health 2>/dev/null)
if [ $? -eq 0 ]; then
    echo "✅ Server is responding"
    echo "$HEALTH" | python3 -m json.tool 2>/dev/null || echo "$HEALTH"
else
    echo "❌ Server is not responding"
fi

# Check Cloudflare Tunnel
echo ""
echo "3. Cloudflare Tunnel Status:"
echo "-----------------------------------"
TUNNEL_PID=$(pgrep -f "cloudflared tunnel")
if [ -n "$TUNNEL_PID" ]; then
    echo "✅ Tunnel is running (PID: $TUNNEL_PID)"
    if [ -f "/root/cloudflared.log" ]; then
        TUNNEL_URL=$(cat /root/cloudflared.log | grep "https://" | grep -o 'https://[^ ]*' | head -1)
        if [ -n "$TUNNEL_URL" ]; then
            echo "🔗 Tunnel URL: $TUNNEL_URL"
            echo "📝 ChatGPT URL: $TUNNEL_URL/sse"
        fi
    fi
else
    echo "❌ Tunnel is not running"
fi

# Check port 8000
echo ""
echo "4. Port 8000 Status:"
echo "-----------------------------------"
PORT_CHECK=$(netstat -tuln 2>/dev/null | grep ":8000 " || ss -tuln 2>/dev/null | grep ":8000 ")
if [ -n "$PORT_CHECK" ]; then
    echo "✅ Port 8000 is listening"
else
    echo "❌ Port 8000 is not open"
fi

# Recent logs
echo ""
echo "5. Recent Logs (last 10 lines):"
echo "-----------------------------------"
sudo journalctl -u wordpress-mcp-server -n 10 --no-pager

echo ""
echo "==================================="
echo "Status check complete!"
echo "==================================="

