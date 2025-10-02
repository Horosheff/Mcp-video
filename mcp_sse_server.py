#!/usr/bin/env python3
"""
WordPress MCP SSE Server for OpenAI and ChatGPT
Allows ChatGPT to create, update, get, and delete WordPress posts via MCP Protocol
"""

import asyncio
import json
import logging
from contextlib import asynccontextmanager
from typing import Any, Dict, Optional

import httpx
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from sse_starlette import EventSourceResponse
from mcp.server import Server
from mcp.types import Tool, TextContent

# ============================================
# CONFIGURATION - CHANGE THESE VALUES
# ============================================
WORDPRESS_URL = "https://your-wordpress-site.com/"
WORDPRESS_USERNAME = "your-username"
WORDPRESS_PASSWORD = "your-application-password"

# ============================================
# LOGGING SETUP
# ============================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================
# WORDPRESS MCP CLASS
# ============================================
class WordPressMCP:
    """WordPress API client for MCP operations"""
    
    def __init__(self, wp_url: str, username: str, password: str):
        self.wp_url = wp_url.rstrip('/') + '/'
        self.api_base = f"{self.wp_url}wp-json/wp/v2/"
        self.client = httpx.AsyncClient(
            auth=(username, password),
            timeout=30.0
        )
        logger.info(f"WordPressMCP initialized for {self.wp_url}")
    
    async def create_post(
        self, 
        title: str, 
        content: str, 
        excerpt: str = "", 
        status: str = "publish"
    ) -> Dict[str, Any]:
        """Create a new WordPress post"""
        try:
            logger.info(f"Creating post: {title}")
            
            payload = {
                "title": title,
                "content": content,
                "excerpt": excerpt,
                "status": status
            }
            
            response = await self.client.post(
                f"{self.api_base}posts",
                json=payload
            )
            
            if response.status_code in [200, 201]:
                data = response.json()
                logger.info(f"Post created successfully: ID {data['id']}")
                return {
                    "success": True,
                    "post_id": data["id"],
                    "url": data["link"],
                    "message": f"Post '{title}' created successfully"
                }
            else:
                error_msg = response.text
                logger.error(f"Failed to create post: {error_msg}")
                return {
                    "success": False,
                    "message": f"Failed to create post: {error_msg}"
                }
                
        except Exception as e:
            logger.error(f"Error creating post: {str(e)}")
            return {
                "success": False,
                "message": f"Error creating post: {str(e)}"
            }
    
    async def update_post(
        self,
        post_id: int,
        title: Optional[str] = None,
        content: Optional[str] = None,
        excerpt: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update an existing WordPress post"""
        try:
            logger.info(f"Updating post ID: {post_id}")
            
            payload = {}
            if title is not None:
                payload["title"] = title
            if content is not None:
                payload["content"] = content
            if excerpt is not None:
                payload["excerpt"] = excerpt
            
            response = await self.client.post(
                f"{self.api_base}posts/{post_id}",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Post {post_id} updated successfully")
                return {
                    "success": True,
                    "post_id": data["id"],
                    "url": data["link"],
                    "message": f"Post ID {post_id} updated successfully"
                }
            else:
                error_msg = response.text
                logger.error(f"Failed to update post: {error_msg}")
                return {
                    "success": False,
                    "message": f"Failed to update post: {error_msg}"
                }
                
        except Exception as e:
            logger.error(f"Error updating post: {str(e)}")
            return {
                "success": False,
                "message": f"Error updating post: {str(e)}"
            }
    
    async def get_posts(
        self,
        per_page: int = 10,
        page: int = 1
    ) -> Dict[str, Any]:
        """Get list of WordPress posts"""
        try:
            logger.info(f"Getting posts: page={page}, per_page={per_page}")
            
            response = await self.client.get(
                f"{self.api_base}posts",
                params={"per_page": per_page, "page": page}
            )
            
            if response.status_code == 200:
                posts = response.json()
                
                posts_data = []
                for post in posts:
                    posts_data.append({
                        "id": post["id"],
                        "title": post["title"]["rendered"],
                        "url": post["link"],
                        "status": post["status"],
                        "date": post["date"]
                    })
                
                logger.info(f"Retrieved {len(posts_data)} posts")
                return {
                    "success": True,
                    "posts": posts_data,
                    "count": len(posts_data),
                    "message": f"Retrieved {len(posts_data)} posts"
                }
            else:
                error_msg = response.text
                logger.error(f"Failed to get posts: {error_msg}")
                return {
                    "success": False,
                    "message": f"Failed to get posts: {error_msg}",
                    "posts": [],
                    "count": 0
                }
                
        except Exception as e:
            logger.error(f"Error getting posts: {str(e)}")
            return {
                "success": False,
                "message": f"Error getting posts: {str(e)}",
                "posts": [],
                "count": 0
            }
    
    async def delete_post(self, post_id: int) -> Dict[str, Any]:
        """Delete a WordPress post"""
        try:
            logger.info(f"Deleting post ID: {post_id}")
            
            response = await self.client.delete(
                f"{self.api_base}posts/{post_id}"
            )
            
            if response.status_code == 200:
                logger.info(f"Post {post_id} deleted successfully")
                return {
                    "success": True,
                    "post_id": post_id,
                    "message": f"Post ID {post_id} deleted successfully"
                }
            else:
                error_msg = response.text
                logger.error(f"Failed to delete post: {error_msg}")
                return {
                    "success": False,
                    "message": f"Failed to delete post: {error_msg}"
                }
                
        except Exception as e:
            logger.error(f"Error deleting post: {str(e)}")
            return {
                "success": False,
                "message": f"Error deleting post: {str(e)}"
            }
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()
        logger.info("WordPressMCP client closed")

# ============================================
# GLOBAL INSTANCES
# ============================================
wp_mcp: Optional[WordPressMCP] = None
mcp_server = Server("wordpress-mcp-server")

# ============================================
# MCP SERVER SETUP
# ============================================
@mcp_server.list_tools()
async def list_tools() -> list[Tool]:
    """List all available MCP tools"""
    return [
        Tool(
            name="create_post",
            description="Create a new WordPress post on your site",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Post title"
                    },
                    "content": {
                        "type": "string",
                        "description": "Post content in HTML"
                    },
                    "excerpt": {
                        "type": "string",
                        "description": "Post excerpt (optional)",
                        "default": ""
                    },
                    "status": {
                        "type": "string",
                        "enum": ["publish", "draft", "private"],
                        "description": "Post status",
                        "default": "publish"
                    }
                },
                "required": ["title", "content"]
            }
        ),
        Tool(
            name="update_post",
            description="Update an existing WordPress post",
            inputSchema={
                "type": "object",
                "properties": {
                    "post_id": {
                        "type": "integer",
                        "description": "Post ID to update"
                    },
                    "title": {
                        "type": "string",
                        "description": "New post title (optional)"
                    },
                    "content": {
                        "type": "string",
                        "description": "New post content (optional)"
                    },
                    "excerpt": {
                        "type": "string",
                        "description": "New post excerpt (optional)"
                    }
                },
                "required": ["post_id"]
            }
        ),
        Tool(
            name="get_posts",
            description="Get list of WordPress posts",
            inputSchema={
                "type": "object",
                "properties": {
                    "per_page": {
                        "type": "integer",
                        "description": "Number of posts per page (1-100)",
                        "default": 10,
                        "minimum": 1,
                        "maximum": 100
                    },
                    "page": {
                        "type": "integer",
                        "description": "Page number",
                        "default": 1,
                        "minimum": 1
                    }
                }
            }
        ),
        Tool(
            name="delete_post",
            description="Delete a WordPress post",
            inputSchema={
                "type": "object",
                "properties": {
                    "post_id": {
                        "type": "integer",
                        "description": "Post ID to delete"
                    }
                },
                "required": ["post_id"]
            }
        )
    ]

@mcp_server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle MCP tool calls"""
    global wp_mcp
    
    logger.info(f"Tool called: {name} with arguments: {arguments}")
    
    try:
        if name == "create_post":
            result = await wp_mcp.create_post(
                title=arguments["title"],
                content=arguments["content"],
                excerpt=arguments.get("excerpt", ""),
                status=arguments.get("status", "publish")
            )
        elif name == "update_post":
            result = await wp_mcp.update_post(
                post_id=arguments["post_id"],
                title=arguments.get("title"),
                content=arguments.get("content"),
                excerpt=arguments.get("excerpt")
            )
        elif name == "get_posts":
            result = await wp_mcp.get_posts(
                per_page=arguments.get("per_page", 10),
                page=arguments.get("page", 1)
            )
        elif name == "delete_post":
            result = await wp_mcp.delete_post(
                post_id=arguments["post_id"]
            )
        else:
            result = {"success": False, "message": f"Unknown tool: {name}"}
        
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
    except Exception as e:
        logger.error(f"Error in tool call: {str(e)}")
        error_result = {"success": False, "message": f"Error: {str(e)}"}
        return [TextContent(type="text", text=json.dumps(error_result, indent=2))]

# ============================================
# FASTAPI APPLICATION
# ============================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global wp_mcp
    
    # Startup
    logger.info("Starting WordPress MCP SSE Server...")
    wp_mcp = WordPressMCP(WORDPRESS_URL, WORDPRESS_USERNAME, WORDPRESS_PASSWORD)
    logger.info("WordPress MCP Server initialized successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down WordPress MCP Server...")
    if wp_mcp:
        await wp_mcp.close()
    logger.info("WordPress MCP Server shutdown complete")

app = FastAPI(
    title="WordPress MCP SSE Server",
    description="MCP Server for WordPress via SSE - OpenAI Compatible",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# ENDPOINTS
# ============================================

@app.get("/")
async def root():
    """Server information"""
    tools = await list_tools()
    return {
        "name": "WordPress MCP SSE Server",
        "version": "1.0.0",
        "protocol": "MCP over SSE",
        "description": "Manage WordPress posts via ChatGPT using MCP protocol",
        "endpoints": {
            "/": "Server information",
            "/health": "Health check",
            "/sse": "SSE endpoint for ChatGPT",
            "/mcp": "MCP JSON-RPC endpoint"
        },
        "tools": [
            {
                "name": tool.name,
                "description": tool.description
            }
            for tool in tools
        ],
        "wordpress_url": WORDPRESS_URL
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "wordpress-mcp-sse-server"
    }

@app.api_route("/sse", methods=["GET", "POST"])
async def sse_endpoint(request: Request):
    """SSE endpoint for ChatGPT/MCP connection (supports both GET and POST)"""
    
    async def event_generator():
        try:
            # Send initial ping comment to prevent buffering
            yield ": ping\n\n"
            
            # Get the external URL from request
            host = request.headers.get("host", "localhost:8000")
            scheme = "https" if "trycloudflare.com" in host else "http"
            mcp_url = f"{scheme}://{host}/mcp"
            
            # Send endpoint information in proper SSE format
            endpoint_data = json.dumps({"url": mcp_url})
            yield f"event: endpoint\ndata: {endpoint_data}\n\n"
            
            # Send heartbeat every 2 seconds
            while True:
                if await request.is_disconnected():
                    logger.info("SSE client disconnected")
                    break
                
                await asyncio.sleep(2)
                
                heartbeat_data = json.dumps({
                    "status": "alive",
                    "timestamp": asyncio.get_event_loop().time()
                })
                yield f"event: heartbeat\ndata: {heartbeat_data}\n\n"
                
        except asyncio.CancelledError:
            logger.info("SSE connection cancelled")
        except Exception as e:
            logger.error(f"SSE error: {e}")
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive"
        }
    )

@app.post("/mcp")
async def mcp_endpoint(request: Request):
    """MCP JSON-RPC endpoint"""
    try:
        body = await request.json()
        logger.info(f"MCP request: {body.get('method')}")
        
        method = body.get("method")
        params = body.get("params", {})
        request_id = body.get("id")
        
        if method == "initialize":
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "wordpress-mcp-server",
                        "version": "1.0.0"
                    }
                }
            }
            
        elif method == "tools/list":
            tools = await list_tools()
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "tools": [
                        {
                            "name": tool.name,
                            "description": tool.description,
                            "inputSchema": tool.inputSchema
                        }
                        for tool in tools
                    ]
                }
            }
            
        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            result = await call_tool(tool_name, arguments)
            
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": result[0].text
                        }
                    ]
                }
            }
            
        else:
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            }
        
        return JSONResponse(content=response)
        
    except Exception as e:
        logger.error(f"Error in MCP endpoint: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "jsonrpc": "2.0",
                "id": request_id if 'request_id' in locals() else None,
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }
        )

# ============================================
# MAIN
# ============================================
if __name__ == "__main__":
    logger.info("="*50)
    logger.info("WordPress MCP SSE Server")
    logger.info("="*50)
    logger.info(f"WordPress URL: {WORDPRESS_URL}")
    logger.info("Starting server on http://0.0.0.0:8000")
    logger.info("="*50)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )

