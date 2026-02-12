# SearXNG Stealth MCP (Node.js)

🔥 **SearXNG Stealth MCP** 是一款专为 AI Agent（如 Claude Code, OpenClaw）设计的 Model Context Protocol (MCP) 服务器。这是基于 Node.js 的高性能版本，提供了更快的启动速度和更流畅的交互体验。

## 核心功能

1.  **`search`**: 全网搜索。支持自定义搜索结果数量。
2.  **隐私保护**: 自动伪装 User-Agent 并支持 Basic Auth 认证。
3.  **结果优化**: 针对 LLM 优化的结果返回格式。

## 安装与配置

### 1. 在 Claude Code 中使用

在你的 `.claude.json` 配置文件中添加以下配置：

```json
"searxng": {
  "command": "npx",
  "args": [
    "-y",
    "git+https://github.com/sanhua1/searxng-stealth-mcp.git"
  ],
  "env": {
    "SEARXNG_URL": "https://your-searxng-domain.com",
    "AUTH_USER": "your-username",
    "AUTH_PASS": "your-password",
    "MAX_RESULTS": "10"
  }
}
```

### 2. 环境变量说明

*   `SEARXNG_URL`: 你的 SearXNG 实例地址。
*   `AUTH_USER`: 认证用户名（默认为 `admin`）。
*   `AUTH_PASS`: 认证密码。
*   `MAX_RESULTS`: 单次搜索返回的最大结果数（默认为 10）。

## 维护信息

*   **Author**: sanhua1
*   **Version**: 2.0.0

---
*本项目由 OpenClaw 自动生成并维护。*
