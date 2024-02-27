import unittest
from main import calculate_cost

class TestCalculateCost(unittest.TestCase):

    def test_calculate_cost(self):
        # Test with positive values
        self.assertEqual(calculate_cost(10, 0.2, 0.5), 2.5)

        # Test with zero usage
        self.assertEqual(calculate_cost(0, 0.2, 0.5), 0.5)

        # Test with zero unit rate
        self.assertEqual(calculate_cost(10, 0, 0.5), 0.5)

        # Test with zero standing charge
        self.assertEqual(calculate_cost(10, 0.2, 0), 2.0)

        # Test with all zero values
        self.assertEqual(calculate_cost(0, 0, 0), 0)

if __name__ == '__main__':
    unittest.main()