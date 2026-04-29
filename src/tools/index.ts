import { Tool } from "../types/tool";
import { helloTool } from "./hello";
import { predictHeartDiseaseTool } from "./predict";

export { Tool };

export const tools: Tool[] = [
  helloTool,
  predictHeartDiseaseTool,
];
