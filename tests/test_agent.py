import unittest
from tools.basic_tools import hello_world

class TestAgent(unittest.TestCase):
    def test_hello_world_tool(self):
        """Test that the hello world tool returns the expected string."""
        result = hello_world()
        self.assertEqual(result, "hello_world has been executed")

if __name__ == "__main__":
    unittest.main()
