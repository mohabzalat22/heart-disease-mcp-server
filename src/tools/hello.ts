import { Tool } from "./index";
import { HelloArgs } from "../types/hello";

export const helloTool: Tool<HelloArgs> = {
  definition: {
    name: "hello",
    description: "Say hello",
    inputSchema: {
      type: "object",
      properties: {
        name: { type: "string" },
      },
      required: ["name"],
    },
  },
  handler: async (args: HelloArgs) => {
    const { name } = args;
    return {
      content: [
        {
          type: "text",
          text: `Hello ${name}! 👋`,
        },
      ],
    };
  },
};
