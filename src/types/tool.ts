import { CallToolResult } from "@modelcontextprotocol/sdk/types.js";

export interface ToolDefinition {
  name: string;
  description: string;
  inputSchema: {
    type: "object";
    properties: Record<string, unknown>;
    required?: string[];
  };
}

/**
 * Interface for an MCP Tool.
 * T represents the type of the arguments passed to the handler.
 */
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export interface Tool<T = any> {
  definition: ToolDefinition;
  handler: (args: T) => Promise<CallToolResult>;
}
