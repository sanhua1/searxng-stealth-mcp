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
    version: "2.0.0",
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
        description: "Search the web using SearXNG with stealth headers.",
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

  const { query } = request.params.arguments as { query: string };

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
      timeout: 10000,
    });

    const results = (response.data.results || []).slice(0, MAX_RESULTS);
    const output = results.map((r: any) => 
      `Title: ${r.title}\nURL: ${r.url}\nSnippet: ${r.content}\n`
    ).join("\n---\n");

    return {
      content: [
        {
          type: "text",
          text: output || "No results found.",
        },
      ],
    };
  } catch (error: any) {
    return {
      content: [
        {
          type: "text",
          text: `API Error (${error.response?.status || 'Unknown'}): ${error.message}`,
        },
      ],
      isError: true,
    };
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);
