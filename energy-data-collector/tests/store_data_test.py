import unittest
from unittest.mock import patch, MagicMock
from main import store_data

class TestStoreData(unittest.TestCase):
    def setUp(self):
        self.config = {
            'INFLUXDB_HOST': 'http://localhost:8086',
            'INFLUXDB_TOKEN': 'my-token',
            'INFLUXDB_ORG': 'my-org',
            'INFLUXDB_BUCKET': 'my-bucket'
        }

    @patch('main.InfluxDBClient')
    @patch('main.fetch_and_prepare_data')
    @patch('main.sched.scheduler')
    def test_store_data(self, mock_scheduler, mock_fetch_and_prepare_data, mock_influxdb_client):
        mock_influxdb_client.return_value.query_api.return_value.query.return_value = [MagicMock()]
        mock_fetch_and_prepare_data.return_value = []
        mock_scheduler.return_value.enter.return_value = None

        store_data(self.config)

        mock_influxdb_client.assert_called_once_with(url=self.config['INFLUXDB_HOST'], token=self.config['INFLUXDB_TOKEN'], org=self.config['INFLUXDB_ORG'])
        mock_fetch_and_prepare_data.assert_called_once()

if __name__ == '__main__':
    unittest.main()