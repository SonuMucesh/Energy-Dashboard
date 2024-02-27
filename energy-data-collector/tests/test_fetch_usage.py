import unittest
from unittest.mock import patch, MagicMock
from main import fetch_usage

class TestFetchUsage(unittest.TestCase):
    def setUp(self):
        self.config = {
            'BASE_64_API_KEY': 'c2tfbGl2ZV9aZFBtUEoxaWU5M29BVmo4dElzYlB1MVg6',
            'GAS_MPRN': '7592684900',
            'GAS_SERIAL_NUMBER': 'E6S17061332161',
            'ELECTRICITY_MPAN': '2500000477284',
            'ELECTRICITY_SERIAL_NUMBER': '19L4007890'
        }
        self.period_to = '2022-01-01T00:00:00'
        self.period_from = '2022-01-01T00:00:00'

    @patch('requests.get')
    def test_fetch_usage(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.json.return_value = {'results': [{'consumption': 5, 'interval_end': '2022-01-02T00:00:00'}]}
        mock_get.return_value = mock_resp

        result = fetch_usage(self.config['GAS_MPRN'], self.config['GAS_SERIAL_NUMBER'],
                             self.config['ELECTRICITY_MPAN'], self.config['ELECTRICITY_SERIAL_NUMBER'],
                             self.period_to, self.period_from, self.config)

        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)

if __name__ == '__main__':
    unittest.main()