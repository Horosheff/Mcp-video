#!/bin/bash

echo "Starting WordPress MCP Server..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found!"
    echo "Please run install.sh first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if mcp_sse_server.py exists
if [ ! -f "mcp_sse_server.py" ]; then
    echo "Error: mcp_sse_server.py not found!"
    exit 1
fi

# Start the server
echo "Server starting on http://0.0.0.0:8000"
python mcp_sse_server.py

