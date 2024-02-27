import unittest
from unittest.mock import patch, MagicMock
from main import fetch_and_prepare_data

class TestFetchAndPrepareData(unittest.TestCase):
    def setUp(self):
        self.config = {
            'OCTOPUS_FLEXIBLE_TARIFF_CODE': 'code1',
            'OCTOPUS_ELECTRICITY_FUEL_TYPE': 'type1',
            'OCTOPUS_GAS_FUEL_TYPE': 'type2',
            'OCTOPUS_TARIFF_GSP': 'gsp',
            'OCTOPUS_PAYMENT_METHOD_FLEXIBLE': 'method1',
            'OCTOPUS_TRACKER_TARIFF': 'tariff',
            'OCTOPUS_PAYMENT_METHOD_TRACKER': 'method2',
            'GAS_MPRN': 'mprn',
            'GAS_SERIAL_NUMBER': 'serial1',
            'ELECTRICITY_MPAN': 'mpan',
            'ELECTRICITY_SERIAL_NUMBER': 'serial2'
        }
        self.last_timestamp = '2022-01-01T00:00:00'

    @patch('main.fetch_tariff')
    @patch('main.fetch_usage')
    def test_fetch_and_prepare_data(self, mock_fetch_usage, mock_fetch_tariff):
        mock_fetch_tariff.return_value = (1, 2, 3, 4)
        mock_fetch_usage.return_value = [{'consumption': 5, 'interval_end': '2022-01-02T00:00:00'}], []

        result = fetch_and_prepare_data(self.last_timestamp, self.config)

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 4)

if __name__ == '__main__':
    unittest.main()