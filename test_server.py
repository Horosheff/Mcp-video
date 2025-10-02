#!/usr/bin/env python3
"""
Test script for WordPress MCP Server
"""

import asyncio
import json
import httpx

# Configuration
BASE_URL = "http://localhost:8000"

async def test_health():
    """Test health endpoint"""
    print("\n=== Testing Health Endpoint ===")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

async def test_server_info():
    """Test server info endpoint"""
    print("\n=== Testing Server Info Endpoint ===")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

async def test_mcp_initialize():
    """Test MCP initialize"""
    print("\n=== Testing MCP Initialize ===")
    async with httpx.AsyncClient() as client:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {}
        }
        response = await client.post(f"{BASE_URL}/mcp", json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

async def test_mcp_list_tools():
    """Test MCP list tools"""
    print("\n=== Testing MCP List Tools ===")
    async with httpx.AsyncClient() as client:
        payload = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        response = await client.post(f"{BASE_URL}/mcp", json=payload)
        print(f"Status: {response.status_code}")
        result = response.json()
        
        if "result" in result and "tools" in result["result"]:
            print(f"\nAvailable Tools ({len(result['result']['tools'])}):")
            for tool in result["result"]["tools"]:
                print(f"  - {tool['name']}: {tool['description']}")
        else:
            print(f"Response: {json.dumps(result, indent=2)}")

async def test_get_posts():
    """Test getting WordPress posts"""
    print("\n=== Testing Get Posts ===")
    async with httpx.AsyncClient() as client:
        payload = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "get_posts",
                "arguments": {
                    "per_page": 5,
                    "page": 1
                }
            }
        }
        response = await client.post(f"{BASE_URL}/mcp", json=payload)
        print(f"Status: {response.status_code}")
        result = response.json()
        
        if "result" in result and "content" in result["result"]:
            content = json.loads(result["result"]["content"][0]["text"])
            print(f"Response: {json.dumps(content, indent=2)}")
        else:
            print(f"Response: {json.dumps(result, indent=2)}")

async def test_create_draft_post():
    """Test creating a draft post"""
    print("\n=== Testing Create Draft Post ===")
    async with httpx.AsyncClient() as client:
        payload = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {
                "name": "create_post",
                "arguments": {
                    "title": "Test Post from MCP Server",
                    "content": "<p>This is a test post created via MCP protocol.</p>",
                    "excerpt": "Test post excerpt",
                    "status": "draft"
                }
            }
        }
        response = await client.post(f"{BASE_URL}/mcp", json=payload)
        print(f"Status: {response.status_code}")
        result = response.json()
        
        if "result" in result and "content" in result["result"]:
            content = json.loads(result["result"]["content"][0]["text"])
            print(f"Response: {json.dumps(content, indent=2)}")
            
            if content.get("success"):
                return content.get("post_id")
        else:
            print(f"Response: {json.dumps(result, indent=2)}")
        
        return None

async def main():
    """Run all tests"""
    print("=" * 60)
    print("WordPress MCP Server - Test Suite")
    print("=" * 60)
    
    try:
        # Basic tests
        await test_health()
        await test_server_info()
        
        # MCP protocol tests
        await test_mcp_initialize()
        await test_mcp_list_tools()
        
        # WordPress operations tests
        await test_get_posts()
        
        # Create a test post (as draft)
        post_id = await test_create_draft_post()
        
        if post_id:
            print(f"\n✅ Test post created with ID: {post_id}")
            print(f"   You can manually delete it from WordPress admin panel")
        
        print("\n" + "=" * 60)
        print("✅ All tests completed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())

