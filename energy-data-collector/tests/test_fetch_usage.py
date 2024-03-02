import unittest
from unittest.mock import patch, Mock
import main

class TestFetchUsage(unittest.TestCase):
    @patch('main.requests.get')
    def test_fetch_usage(self, mock_get):
        # Mock the API responses
        mock_get.return_value.json.return_value = {
            'results': [{'consumption': 10}],
            'next': None
        }

        # Define a sample configuration
        config = {
            'BASE_64_API_KEY': 'sample_api_key',
            'GAS_MPRN': 'sample_gas_mprn',
            'GAS_SERIAL_NUMBER': 'sample_gas_serial_number',
            'ELECTRICITY_MPAN': 'sample_electricity_mpan',
            'ELECTRICITY_SERIAL_NUMBER': 'sample_electricity_serial_number'
        }

        # Call the function with the sample configuration
        electricity_data, gas_data = main.fetch_usage(
            config['GAS_MPRN'], config['GAS_SERIAL_NUMBER'],
            config['ELECTRICITY_MPAN'], config['ELECTRICITY_SERIAL_NUMBER'],
            config
        )

        # Assert that the function returned the expected results
        self.assertEqual(electricity_data, [{'consumption': 10}])
        self.assertEqual(gas_data, [{'consumption': 10}])

if __name__ == '__main__':
    unittest.main()