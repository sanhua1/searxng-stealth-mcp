import os
import sys
import json
import asyncio
import httpx
from mcp.server.fastmcp import FastMCP

# 初始化 FastMCP
mcp = FastMCP("searxng")

# 从环境变量获取配置
SEARXNG_URL = os.environ.get("SEARXNG_URL", "http://localhost:18888")
MAX_RESULTS = int(os.environ.get("MAX_RESULTS", "5"))
REQUEST_TIMEOUT = float(os.environ.get("REQUEST_TIMEOUT", "30.0"))

@mcp.tool()
async def search(query: str):
    """Search the web using SearXNG."""
    # 强力伪装 Header
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0"
    }
    
    # 构造请求 URL
    url = f"{SEARXNG_URL}/search?q={query}&format=json"
    
    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT, follow_redirects=True) as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            results = data.get("results", [])
            if not results:
                unresponsive = data.get("unresponsive_engines", [])
                if unresponsive:
                    return f"No results found. Warning: Some engines timed out: {unresponsive}"
                return "No results found."
                
            # 使用动态配置的 MAX_RESULTS
            formatted = []
            for r in results[:MAX_RESULTS]:
                formatted.append(f"Title: {r.get('title')}\nURL: {r.get('url')}\nContent: {r.get('content')}\n")
            
            return "\n".join(formatted)
        except Exception as e:
            return f"Error connecting to SearXNG: {str(e)}"

if __name__ == "__main__":
    mcp.run()
