import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

import {
  ListToolsRequestSchema,
  CallToolRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { tools } from "./tools/index";

// Create server
const server = new Server(
  {
    name: "my-mcp-server",
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

server.setRequestHandler(
  CallToolRequestSchema,
  async (request) => {
    const tool = tools.find(t => t.definition.name === request.params.name);
    
    if (tool) {
      return tool.handler(request.params.arguments);
    }

    throw new Error(`Unknown tool: ${request.params.name}`);
  }
);

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main();