import unittest
import main

class TestCalculateCost(unittest.TestCase):
    def test_calculate_cost_electricity(self):
        # Test the calculation for electricity
        result = main.calculate_cost("electricity", 10, 0.15)
        self.assertEqual(result, 1.5)

    def test_calculate_cost_gas(self):
        # Test the calculation for gas
        result = main.calculate_cost("gas", 10, 0.15)
        self.assertAlmostEqual(result, 16.74573, places=5)

    def test_calculate_cost_invalid_fuel_type(self):
        # Test the calculation for an invalid fuel type
        result = main.calculate_cost("invalid", 10, 0.15)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()