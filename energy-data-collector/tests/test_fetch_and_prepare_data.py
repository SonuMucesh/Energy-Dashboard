import unittest
from unittest.mock import patch, Mock
import main

class TestFetchAndPrepareData(unittest.TestCase):
    @patch('main.fetch_tariff')
    @patch('main.fetch_usage')
    @patch('main.calculate_cost')
    def test_fetch_and_prepare_data(self, mock_calculate_cost, mock_fetch_usage, mock_fetch_tariff):
        # Mock the API responses
        mock_fetch_tariff.return_value = (0.15, 0.20, 0.25, 0.30)
        mock_fetch_usage.return_value = [{'consumption': 10, 'interval_start': '2021-01-01T00:00:00Z', 'interval_end': '2021-01-01T01:00:00Z'}], [{'consumption': 10, 'interval_start': '2021-01-01T00:00:00Z', 'interval_end': '2021-01-01T01:00:00Z'}]
        mock_calculate_cost.return_value = 1.5

        # Define a sample configuration
        config = {
            'OCTOPUS_FLEXIBLE_TARIFF_CODE': 'sample_flexible_tariff_code',
            'OCTOPUS_ELECTRICITY_FUEL_TYPE': 'sample_electricity_fuel_type',
            'OCTOPUS_GAS_FUEL_TYPE': 'sample_gas_fuel_type',
            'OCTOPUS_TARIFF_GSP': 'sample_tariff_gsp',
            'OCTOPUS_PAYMENT_METHOD_FLEXIBLE': 'sample_payment_method_flexible',
            'OCTOPUS_TRACKER_TARIFF': 'sample_tracker_tariff',
            'OCTOPUS_PAYMENT_METHOD_TRACKER': 'sample_payment_method_tracker',
            'GAS_MPRN': 'sample_gas_mprn',
            'GAS_SERIAL_NUMBER': 'sample_gas_serial_number',
            'ELECTRICITY_MPAN': 'sample_electricity_mpan',
            'ELECTRICITY_SERIAL_NUMBER': 'sample_electricity_serial_number'
        }

        # Call the function with the sample configuration
        result = main.fetch_and_prepare_data(config)

        # Assert that the function returned the expected results
        self.assertEqual(len(result), 6)
        self.assertEqual(result[0]['measurement'], 'flexible_tariff')
        self.assertEqual(result[1]['measurement'], 'tracker_tariff')
        self.assertEqual(result[2]['measurement'], 'electricity_cost')
        self.assertEqual(result[3]['measurement'], 'gas_cost')
        self.assertEqual(result[4]['measurement'], 'electricity_usage')
        self.assertEqual(result[5]['measurement'], 'gas_usage')

if __name__ == '__main__':
    unittest.main()