import { createServer } from "http";
import { URL } from "url";
import dotenv from "dotenv";

dotenv.config();
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";
import {
  ListToolsRequestSchema,
  CallToolRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { tools } from "./tools/index";

const PORT = process.env.PORT || 3000;

// Store active sessions (server + transport) by sessionId
const activeSessions = new Map<string, { transport: SSEServerTransport; server: Server }>();

/**
 * Creates a new MCP Server instance with tool handlers.
 * We use a factory because each SSE connection needs its own Server instance
 * to avoid the "Already connected to a transport" error.
 */
function createMcpServer() {
  const server = new Server(
    {
      name: "heart-disease-server-http",
      version: "1.0.0",
    },
    {
      capabilities: {
        tools: {},
      },
    }
  );

  server.setRequestHandler(ListToolsRequestSchema, async () => {
    return {
      tools: tools.map(tool => tool.definition),
    };
  });

  server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const tool = tools.find(t => t.definition.name === request.params.name);
    if (tool) return tool.handler(request.params.arguments);
    throw new Error(`Unknown tool: ${request.params.name}`);
  });

  return server;
}

const httpServer = createServer(async (req, res) => {
  // CORS Headers
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, Accept");

  if (req.method === "OPTIONS") {
    res.statusCode = 204;
    res.end();
    return;
  }

  const url = new URL(req.url || "", `http://localhost:${PORT}`);

  if (url.pathname === "/sse" && req.method === "GET") {
    console.log(`[${new Date().toISOString()}] New SSE connection request`);
    try {
      const transport = new SSEServerTransport("/messages", res);
      const server = createMcpServer();
      
      await server.connect(transport);
      
      const sessionId = transport.sessionId;
      activeSessions.set(sessionId, { transport, server });
      console.log(`[${new Date().toISOString()}] Session ${sessionId} connected`);

      transport.onclose = async () => {
        console.log(`[${new Date().toISOString()}] Session ${sessionId} closed`);
        activeSessions.delete(sessionId);
        await server.close();
      };
    } catch (error) {
      console.error("SSE Connection Error:", error);
      if (!res.headersSent) {
        res.statusCode = 500;
        res.end(`SSE Error: ${error}`);
      }
    }
  } else if (url.pathname === "/messages" && req.method === "POST") {
    const sessionId = url.searchParams.get("sessionId");
    console.log(`[${new Date().toISOString()}] Message for session: ${sessionId}`);
    
    const session = activeSessions.get(sessionId || "");
    if (session) {
      try {
        await session.transport.handlePostMessage(req, res);
      } catch (error) {
        console.error("Message Error:", error);
        if (!res.headersSent) {
          res.statusCode = 500;
          res.end(`Message Error: ${error}`);
        }
      }
    } else {
      res.statusCode = 404;
      res.end("Session not found or inactive");
    }
  } else {
    res.statusCode = 404;
    res.end("Not Found");
  }
});

httpServer.listen(PORT, () => {
  console.log(`🚀 MCP HTTP Server running on http://localhost:${PORT}`);
  console.log(`📡 SSE endpoint: http://localhost:${PORT}/sse`);
  console.log(`✉️ Messages endpoint: http://localhost:${PORT}/messages`);
});

process.on('uncaughtException', (err) => {
  console.error('Uncaught Exception:', err);
});

process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection at:', promise, 'reason:', reason);
});
