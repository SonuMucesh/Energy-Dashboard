import unittest
from unittest.mock import patch, Mock
from main import fetch_tariff

class TestFetchTariff(unittest.TestCase):

    @patch('requests.get')
    def test_fetch_tariff(self, mock_get):
        # Mock the response from the Octopus API
        mock_response = Mock()
        mock_response.json.return_value = {
            'electricity_fuel_type': {
                'fuel_type_code': {
                    'payment_method': {
                        'standing_charge_inc_vat': 0.20,
                        'standard_unit_rate_inc_vat': 0.15
                    }
                }
            },
            'gas_fuel_type': {
                'fuel_type_code': {
                    'payment_method': {
                        'standing_charge_inc_vat': 0.30,
                        'standard_unit_rate_inc_vat': 0.25
                    }
                }
            }
        }
        mock_get.return_value = mock_response

        # Call the function with test data
        tariff_code = 'test_tariff_code'
        electricity_fuel_type = 'electricity_fuel_type'
        gas_fuel_type = 'gas_fuel_type'
        fuel_type_code = 'fuel_type_code'
        payment_method = 'payment_method'

        electricity_unit_rate, electricity_standing_charge, gas_unit_rate, gas_standing_charge = fetch_tariff(
            tariff_code, electricity_fuel_type, gas_fuel_type, fuel_type_code, payment_method)

        # Assert that the function returns the expected data
        self.assertEqual(electricity_unit_rate, 0.15)
        self.assertEqual(electricity_standing_charge, 0.20)
        self.assertEqual(gas_unit_rate, 0.25)
        self.assertEqual(gas_standing_charge, 0.30)

        # Assert that requests.get was called with the expected arguments
        mock_get.assert_called_once_with(f'https://api.octopus.energy/v1/products/{tariff_code}/')

if __name__ == '__main__':
    unittest.main()