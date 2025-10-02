#!/bin/bash

echo "==================================="
echo "WordPress MCP Server - Installation"
echo "==================================="

# Шаг 1: Обновить систему
echo "Step 1: Updating system..."
sudo apt update && sudo apt upgrade -y

# Шаг 2: Установить зависимости
echo "Step 2: Installing dependencies..."
sudo apt install -y python3 python3-pip python3-venv git curl wget net-tools

# Шаг 3: Создать директорию проекта
echo "Step 3: Creating project directory..."
sudo mkdir -p /opt/wordpress-mcp-server
cd /opt/wordpress-mcp-server

# Шаг 4: Копировать файлы проекта
echo "Step 4: Please copy these files to /opt/wordpress-mcp-server/:"
echo "  - mcp_sse_server.py"
echo "  - requirements.txt"
echo ""
read -p "Press Enter when files are copied..."

# Шаг 5: Создать виртуальное окружение
echo "Step 5: Creating Python virtual environment..."
python3 -m venv venv

# Шаг 6: Активировать и установить зависимости
echo "Step 6: Installing Python packages..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Шаг 7: Настроить WordPress credentials
echo "Step 7: Configure WordPress credentials..."
echo "Edit mcp_sse_server.py and set:"
echo "  WORDPRESS_URL = 'https://your-site.com/'"
echo "  WORDPRESS_USERNAME = 'your-username'"
echo "  WORDPRESS_PASSWORD = 'your-password'"
echo ""
read -p "Press Enter when configured..."

# Шаг 8: Создать systemd сервис
echo "Step 8: Creating systemd service..."
sudo tee /etc/systemd/system/wordpress-mcp-server.service > /dev/null <<EOF
[Unit]
Description=WordPress MCP SSE Server for OpenAI
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/wordpress-mcp-server
Environment=PATH=/opt/wordpress-mcp-server/venv/bin
ExecStart=/opt/wordpress-mcp-server/venv/bin/python mcp_sse_server.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Шаг 9: Включить и запустить сервис
echo "Step 9: Starting MCP server..."
sudo systemctl daemon-reload
sudo systemctl enable wordpress-mcp-server
sudo systemctl start wordpress-mcp-server

# Шаг 10: Настроить firewall
echo "Step 10: Configuring firewall..."
sudo ufw allow 8000/tcp
echo "Firewall configured!"

# Шаг 11: Проверить статус
echo ""
echo "Step 11: Checking server status..."
sleep 3
sudo systemctl status wordpress-mcp-server --no-pager

# Шаг 12: Тестирование
echo ""
echo "Step 12: Testing endpoints..."
echo "Health check:"
curl -s http://localhost:8000/health | python3 -m json.tool

echo ""
echo "Server info:"
curl -s http://localhost:8000/ | python3 -m json.tool

# Шаг 13: Установить Cloudflare Tunnel
echo ""
echo "Step 13: Installing Cloudflare Tunnel for HTTPS..."
cd /root
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
chmod +x cloudflared-linux-amd64
sudo mv cloudflared-linux-amd64 /usr/local/bin/cloudflared

echo "Starting Cloudflare Tunnel..."
nohup cloudflared tunnel --url http://localhost:8000 > cloudflared.log 2>&1 &
sleep 5

echo ""
echo "Getting HTTPS URL..."
cat cloudflared.log | grep "https://"

# Итоги
echo ""
echo "==================================="
echo "✅ INSTALLATION COMPLETE!"
echo "==================================="
echo ""
echo "MCP Server is running on port 8000"
echo ""
echo "Your HTTPS URL (for ChatGPT):"
cat cloudflared.log | grep "https://" | grep -o 'https://[^ ]*' | head -1
echo ""
echo "Use this URL in ChatGPT: https://your-url.trycloudflare.com/sse"
echo ""
echo "Management commands:"
echo "  Status:  sudo systemctl status wordpress-mcp-server"
echo "  Logs:    sudo journalctl -u wordpress-mcp-server -f"
echo "  Restart: sudo systemctl restart wordpress-mcp-server"
echo ""
echo "==================================="

