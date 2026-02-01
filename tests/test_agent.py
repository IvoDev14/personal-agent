import unittest
from tools.basic_tools import printHelloWorld

class TestAgent(unittest.TestCase):
    def test_hello_world_tool(self):
        """Test that the hello world tool returns the expected string."""
        result = printHelloWorld()
        self.assertEqual(result, "printHelloWorld has been executed")

if __name__ == "__main__":
    unittest.main()
