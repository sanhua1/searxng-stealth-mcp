import asyncio
import os
import sys
from mcp.server.stdio import stdio_server
from mcp.server import Server
from mcp.types import Tool, TextContent
import requests

# Get config from env
SEARXNG_URL = os.environ.get("SEARXNG_URL", "https://searxng.oneding.top")
MAX_RESULTS = int(os.environ.get("MAX_RESULTS", "10"))

server = Server("searxng-stealth")

@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    return [
        Tool(
            name="search",
            description="Search the web using SearXNG with stealth headers.",
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

    # Stealth Headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }

    try:
        response = requests.get(
            f"{SEARXNG_URL}/search",
            params={"q": query, "format": "json", "pageno": 1},
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        results = data.get("results", [])[:MAX_RESULTS]
        output = []
        for r in results:
            output.append(f"Title: {r.get('title')}\nURL: {r.get('url')}\nSnippet: {r.get('content')}\n")
        
        return [TextContent(type="text", text="\n---\n".join(output) if output else "No results found.")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
