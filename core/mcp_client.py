
import asyncio
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class MCPClientManager:
    """Manages connections to MCP servers."""
    
    def __init__(self):
        self.sessions = {}
        self.exit_stack = AsyncExitStack()

    async def connect_to_server(self, name: str, command: str, args: list[str]):
        """Connects to an MCP server via stdio."""
        server_params = StdioServerParameters(command=command, args=args, env=None)
        
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        stdio, write = stdio_transport
        
        session = await self.exit_stack.enter_async_context(ClientSession(stdio, write))
        await session.initialize()
        
        self.sessions[name] = session
        print(f"✅ Connected to MCP server: {name}")

    async def list_tools(self):
        """Aggregates tools from all connected servers."""
        all_tools = []
        for name, session in self.sessions.items():
            result = await session.list_tools()
            for tool in result.tools:
                # Add server name prefix or metadata if needed, but for now raw tool is fine
                # We might need to wrap it to track which server it belongs to
                tool.server_name = name 
                all_tools.append(tool)
        return all_tools

    async def call_tool(self, name: str, arguments: dict):
        """Calls a tool on the appropriate server."""
        # Find which server has the tool
        # In a real implementations we should cache this map
        for server_name, session in self.sessions.items():
            result = await session.list_tools()
            for tool in result.tools:
                if tool.name == name:
                    return await session.call_tool(name, arguments)
        



    async def cleanup(self):
        """Closes all connections."""
        await self.exit_stack.aclose()
