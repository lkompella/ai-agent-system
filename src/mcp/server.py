"""
Model Context Protocol (MCP) Server Implementation
"""

import logging
from typing import Dict, List, Any, Callable
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class Tool:
    """Tool definition for MCP"""
    name: str
    description: str
    parameters: Dict[str, Any]
    handler: Callable

@dataclass
class ToolResult:
    """Result from tool execution"""
    success: bool
    data: Any
    error: str = None

class MCPServer:
    """MCP Server implementation"""
    
    def __init__(self, config):
        self.config = config
        self.tools: Dict[str, Tool] = {}
    
    def register_tool(self, name: str, description: str, parameters: Dict[str, Any], handler: Callable):
        """Register a new tool"""
        tool = Tool(name=name, description=description, parameters=parameters, handler=handler)
        self.tools[name] = tool
        logger.info(f"Registered tool: {name}")
    
    async def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> ToolResult:
        """Execute a tool with given parameters"""
        if tool_name not in self.tools:
            return ToolResult(success=False, data=None, error=f"Tool '{tool_name}' not found")
        
        tool = self.tools[tool_name]
        
        try:
            result = tool.handler(**parameters)
            return ToolResult(success=True, data=result)
        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {e}")
            return ToolResult(success=False, data=None, error=str(e))
    
    def get_available_tools(self) -> List[Dict[str, Any]]:
        """Get list of available tools"""
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters
            }
            for tool in self.tools.values()
        ]
    
    async def health_check(self) -> Dict[str, Any]:
        """Health check for MCP server"""
        return {
            "status": "healthy",
            "tool_count": len(self.tools)
        }
