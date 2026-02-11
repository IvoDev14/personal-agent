
import unittest
import asyncio
from core.mcp_client import MCPClientManager

class TestMCPClientManager(unittest.TestCase):
    
    def test_connect_and_list_tools(self):
        """Test connecting to the local hello_world server and listing tools."""
        
        async def run_test():
            manager = MCPClientManager()
            try:
                # Path assumes running from project root
                await manager.connect_to_server(
                    "hello_world", 
                    "python", 
                    ["modules/hello_world/hello_mcp.py"]
                )
                
                tools = await manager.list_tools()
                print(f"Discovered tools: {[t.name for t in tools]}")
                
                self.assertTrue(len(tools) > 0)
                self.assertTrue(any(t.name == "presentation" for t in tools))
                
                # Test calling the tool
                result = await manager.call_tool("presentation", {})
                print("Tool Result:", result)
                self.assertIsNotNone(result)
                
            finally:
                await manager.cleanup()
                
        asyncio.run(run_test())

if __name__ == "__main__":
    unittest.main()
