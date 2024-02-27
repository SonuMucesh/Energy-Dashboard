import unittest
from unittest.mock import patch, mock_open
from main import load_config

class TestLoadConfig(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data='{"key": "value"}')
    def test_load_config(self, mock_file):
        # Here you can call the function and assert the expected output
        expected_output = {"key": "value"}
        self.assertEqual(load_config(), expected_output)

if __name__ == '__main__':
    unittest.main()