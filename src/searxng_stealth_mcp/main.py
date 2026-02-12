import asyncio
import os
import sys
import base64
from mcp.server.stdio import stdio_server
from mcp.server import Server
from mcp.types import Tool, TextContent
import requests
from urllib.parse import urlparse

# --- Configuration ---
SEARXNG_URL_RAW = os.environ.get("SEARXNG_URL", "https://searxng.oneding.top")
AUTH_USER = os.environ.get("AUTH_USER")
AUTH_PASS = os.environ.get("AUTH_PASS")
MAX_RESULTS = int(os.environ.get("MAX_RESULTS", "12"))
REQUEST_TIMEOUT = int(os.environ.get("REQUEST_TIMEOUT", "30"))

# --- Helper: Parse Auth ---
def get_auth_headers():
    # 1. Check if auth is embedded in URL: https://user:pass@domain.com
    parsed = urlparse(SEARXNG_URL_RAW)
    if parsed.username and parsed.password:
        auth_str = f"{parsed.username}:{parsed.password}"
        base_url = f"{parsed.scheme}://{parsed.netloc.split('@')[-1]}{parsed.path}".rstrip('/')
        return base_url, {"Authorization": f"Basic {base64.b64encode(auth_str.encode()).decode()}"}
    
    # 2. Check if auth is provided via separate env vars
    if AUTH_USER and AUTH_PASS:
        auth_str = f"{AUTH_USER}:{AUTH_PASS}"
        return SEARXNG_URL_RAW.rstrip('/'), {"Authorization": f"Basic {base64.b64encode(auth_str.encode()).decode()}"}
    
    return SEARXNG_URL_RAW.rstrip('/'), {}

BASE_URL, AUTH_HEADERS = get_auth_headers()

# --- MCP Server ---
server = Server("searxng-stealth")

@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    return [
        Tool(
            name="search",
            description="Search the web using SearXNG with stealth headers and auto-retry.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                },
                "required": ["query"],
            },
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[TextContent]:
    if name != "search":
        raise ValueError(f"Unknown tool: {name}")

    query = arguments.get("query")
    if not query:
        raise ValueError("Missing query")

    # Stealth Headers (Copied from working Python logic)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/html, */*",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        **AUTH_HEADERS
    }

    max_retries = 2
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(
                f"{BASE_URL}/search",
                params={"q": query, "format": "json", "pageno": 1},
                headers=headers,
                timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()
            data = response.json()
            
            results = data.get("results", [])
            
            # Anti-shake retry logic
            if not results and attempt < max_retries:
                await asyncio.sleep(1)
                continue

            output = []
            for r in results[:MAX_RESULTS]:
                output.append(f"Title: {r.get('title')}\nURL: {r.get('url')}\nSnippet: {r.get('content')}\n")
            
            return [TextContent(type="text", text="\n---\n".join(output) if output else "No results found after safety retries.")]
        except Exception as e:
            if attempt == max_retries:
                return [TextContent(type="text", text=f"API Error after {attempt} attempts: {str(e)}")]
            await asyncio.sleep(1.5)

def main():
    asyncio.run(_run())

async def _run():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    main()
