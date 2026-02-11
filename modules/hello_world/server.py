from mcp.server.fastmcp import FastMCP

#Server instance
mcp = FastMCP("HelloServer")

#Tools definitions
@mcp.tool()
def presentation() -> str:
    """Run a presentation of the MCP tools.
    
    Returns:
        str: A markdown formatted presentation of the server capabilities.
    """
    return """## 🛠️ MCP Tools Presentation

### 🚀 Server Status
- **Name:** HelloServer
- **Status:** Active & Running

### 📦 Available Tools

1. **presentation**
   - *Description:* Shows this presentation of available tools.
   - *Usage:* Call without arguments to view server capabilities.

### 🔗 Connection Info 
- **Protocol:** Model Context Protocol (MCP)
- **Transport:** Standard IO (stdio)

*This server is ready to handle your requests!*"""


#Run the server in stdio mode
if __name__ == "__main__":
    mcp.run(transport="stdio")
