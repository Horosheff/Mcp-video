#!/bin/bash

echo "Restarting Cloudflare Tunnel..."

# Kill existing cloudflared processes
echo "Stopping existing tunnel..."
pkill cloudflared
sleep 2

# Start new tunnel
echo "Starting new tunnel..."
nohup cloudflared tunnel --url http://localhost:8000 > cloudflared.log 2>&1 &

# Wait for tunnel to start
echo "Waiting for tunnel to initialize..."
sleep 5

# Show the HTTPS URL
echo ""
echo "==================================="
echo "Cloudflare Tunnel URL:"
echo "==================================="
cat cloudflared.log | grep "https://" | grep -o 'https://[^ ]*' | head -1
echo ""
echo "Use this URL in ChatGPT: [URL]/sse"
echo "==================================="

