# SearXNG Stealth MCP

🔥 **SearXNG Stealth MCP** 是一款专为 AI Agent（如 Claude Code, OpenClaw）设计的 Model Context Protocol (MCP) 服务器。它专门针对私有部署的 SearXNG 进行了优化，提供更强的隐私保护和搜索能力。

## 核心功能

1.  **`search`**: 全网搜索。支持自定义搜索深度、时间范围以及结果数量。
2.  **隐私保护**: 自动伪装 User-Agent，确保搜索请求的隐蔽性。
3.  **结果优化**: 针对 LLM 优化的结果返回格式。

## 安装与配置

### 1. 在 Claude Code 中使用

在你的 `.claude.json` 配置文件中添加以下配置：

```json
"searxng": {
  "command": "uvx",
  "args": [
    "git+https://github.com/sanhua1/searxng-stealth-mcp.git"
  ],
  "env": {
    "SEARXNG_URL": "https://your-searxng-domain.com",
    "MAX_RESULTS": "10"
  }
}
```

### 2. 环境变量说明

*   `SEARXNG_URL`: 你的 SearXNG 实例地址。
*   `MAX_RESULTS`: 单次搜索返回的最大结果数（默认为 10）。

## 维护信息

*   **Author**: sanhua1
*   **Version**: 1.1.0

---
*本项目由 OpenClaw 自动生成并维护。*
