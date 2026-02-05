import unittest
from unittest.mock import patch, MagicMock
from tools.system_tools import execute_terminal

class TestSystemTools(unittest.TestCase):
    
    @patch('builtins.input', return_value='y')
    @patch('subprocess.run')
    def test_execute_terminal_allow(self, mock_run, mock_input):
        """Test that command is executed when user allows it."""
        # Setup mock return
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_process.stdout = "Success"
        mock_process.stderr = ""
        mock_run.return_value = mock_process
        
        result = execute_terminal("echo test")
        
        # Verify input was called
        mock_input.assert_called_once()
        
        # Verify subprocess was called
        mock_run.assert_called_with("echo test", shell=True, capture_output=True, text=True)
        
        # Verify output format
        self.assertIn("EXIT CODE: 0", result)
        self.assertIn("STDOUT: Success", result)

    @patch('builtins.input', return_value='n')
    @patch('subprocess.run')
    def test_execute_terminal_deny(self, mock_run, mock_input):
        """Test that command is NOT executed when user denies it."""
        result = execute_terminal("rm -rf /")
        
        # Verify input was called
        mock_input.assert_called_once()
        
        # Verify subprocess was NOT called
        mock_run.assert_not_called()
        
        # Verify error message
        self.assertEqual(result, "Error: Command denied by user.")

    @patch('builtins.input', return_value='y')
    @patch('subprocess.run')
    def test_execute_terminal_failure(self, mock_run, mock_input):
        """Test handling of failed commands."""
        # Setup mock return for failure
        mock_process = MagicMock()
        mock_process.returncode = 1
        mock_process.stdout = ""
        mock_process.stderr = "Command not found"
        mock_run.return_value = mock_process
        
        result = execute_terminal("invalid_command")
        
        self.assertIn("EXIT CODE: 1", result)
        self.assertIn("STDERR: Command not found", result)

if __name__ == "__main__":
    unittest.main()
