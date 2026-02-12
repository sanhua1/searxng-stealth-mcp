#!/usr/bin/env node
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import axios from "axios";

const SEARXNG_URL = process.env.SEARXNG_URL || "https://searxng.oneding.top";
const AUTH_USER = process.env.AUTH_USER || "admin";
const AUTH_PASS = process.env.AUTH_PASS || "D1elevend1!";
const MAX_RESULTS = parseInt(process.env.MAX_RESULTS || "10", 10);

const AUTH_TOKEN = Buffer.from(`${AUTH_USER}:${AUTH_PASS}`).toString("base64");

const server = new Server(
  {
    name: "searxng-stealth-js",
    version: "2.1.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "search",
        description: "Search the web using SearXNG with stealth headers and auto-retry.",
        inputSchema: {
          type: "object",
          properties: {
            query: { type: "string", description: "The search query" },
          },
          required: ["query"],
        },
      },
    ],
  };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name !== "search") {
    throw new Error("Tool not found");
  }

  const { query } = request.params.arguments;
  const maxRetries = 2;

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const response = await axios.get(`${SEARXNG_URL}/search`, {
        params: {
          q: query,
          format: "json",
          pageno: 1,
        },
        headers: {
          Authorization: `Basic ${AUTH_TOKEN}`,
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
          Accept: "application/json",
        },
        timeout: 20000, // 给私有引擎留足响应时间
      });

      const results = (response.data.results || []);
      
      // 防抖增强：如果结果为空且还有重试机会，自动重试（应对引擎冷启动/超时）
      if (results.length === 0 && attempt < maxRetries) {
        await new Promise(resolve => setTimeout(resolve, 1000));
        continue;
      }

      const output = results.slice(0, MAX_RESULTS).map((r) => 
        `Title: ${r.title}\nURL: ${r.url}\nSnippet: ${r.content}\n`
      ).join("\n---\n");

      return {
        content: [
          {
            type: "text",
            text: output || "No results found after safety retries.",
          },
        ],
      };
    } catch (error) {
      if (attempt === maxRetries) {
        return {
          content: [{ type: "text", text: `API Error (Attempt ${attempt}): ${error.message}` }],
          isError: true,
        };
      }
      await new Promise(resolve => setTimeout(resolve, 1500));
    }
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);
