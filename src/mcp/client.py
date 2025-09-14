"""
MCP Client Implementation
"""

import logging
from typing import Dict, List, Any
import re

from .server import MCPServer, ToolResult

logger = logging.getLogger(__name__)

class MCPClient:
    """MCP Client for tool execution"""
    
    def __init__(self, config):
        self.config = config
        self.server = MCPServer(config)
        self._register_default_tools()
    
    async def initialize(self):
        """Initialize MCP client"""
        logger.info("MCP client initialized")
    
    def _register_default_tools(self):
        """Register default tools"""
        
        # File search tool
        self.server.register_tool(
            name="file_search",
            description="Search for files matching a pattern",
            parameters={
                "type": "object",
                "properties": {
                    "pattern": {"type": "string"},
                    "directory": {"type": "string"}
                },
                "required": ["pattern"]
            },
            handler=self._file_search_handler
        )
        
        # Calculator tool
        self.server.register_tool(
            name="calculator",
            description="Perform mathematical calculations",
            parameters={
                "type": "object",
                "properties": {
                    "expression": {"type": "string"}
                },
                "required": ["expression"]
            },
            handler=self._calculator_handler
        )
    
    async def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Any:
        """Execute a tool and return the result"""
        result = await self.server.execute_tool(tool_name, parameters)
        
        if result.success:
            return result.data
        else:
            raise Exception(f"Tool execution failed: {result.error}")
    
    async def get_available_tools(self) -> List[Dict[str, Any]]:
        """Get available tools"""
        return self.server.get_available_tools()
    
    async def health_check(self) -> Dict[str, Any]:
        """Health check for MCP client"""
        return await self.server.health_check()
    
    # Tool handlers
    def _file_search_handler(self, pattern: str, directory: str = ".") -> List[str]:
        """Search for files matching pattern"""
        try:
            import glob
            import os
            search_path = os.path.join(directory, pattern)
            matches = glob.glob(search_path, recursive=True)
            return matches[:10]  # Limit results
        except Exception as e:
            logger.error(f"File search error: {e}")
            return []
    
    def _calculator_handler(self, expression: str) -> Dict[str, Any]:
        """Perform mathematical calculation"""
        try:
            # Only allow safe mathematical operations
            if re.match(r'^[0-9+\-*/().\s]+$', expression):
                result = eval(expression)
                return {"result": result, "expression": expression}
            else:
                return {"error": "Invalid expression"}
        except Exception as e:
            return {"error": str(e)}
