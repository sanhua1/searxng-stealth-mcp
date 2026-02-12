# SearXNG Stealth MCP (Python)

🔥 **SearXNG Stealth MCP** 是一款专为 AI Agent（如 Claude Code, OpenClaw）设计的 Model Context Protocol (MCP) 服务器。这是基于 Python 的稳健版本，提供了最强的搜索引擎兼容性和隐身能力。

## 核心功能

1.  **`search`**: 全网搜索。支持自定义搜索结果数量。
2.  **隐身增强**: 模拟真实浏览器请求头，绕过 WAF 拦截。
3.  **双模配置**: 兼容 URL 嵌入认证和环境变量独立配置。

## 安装与配置

### 1. 在 Claude Code 中使用

在你的 `.claude.json` 配置文件中添加以下配置：

```json
"searxng": {
  "command": "uvx",
  "args": [
    "--from",
    "git+https://github.com/sanhua1/searxng-stealth-mcp.git",
    "searxng-stealth-mcp"
  ],
  "env": {
    "SEARXNG_URL": "https://admin:yourpassword@your-searxng-domain.com",
    "MAX_RESULTS": "12",
    "REQUEST_TIMEOUT": "30"
  }
}
```

### 2. 环境变量说明

*   `SEARXNG_URL`: 你的 SearXNG 实例地址（支持 `https://user:pass@domain` 格式）。
*   `AUTH_USER` / `AUTH_PASS`: (可选) 如果 URL 里没写，也可以分开配置。
*   `MAX_RESULTS`: 单次搜索返回的最大结果数。
*   `REQUEST_TIMEOUT`: 请求超时上限（秒）。

## 维护信息

*   **Author**: sanhua1
*   **Version**: 1.2.0

---
*本项目由 OpenClaw 自动生成并维护。*
