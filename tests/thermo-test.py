import unittest
from src.thermo import potential_temperature # For Travis CI src.thermo is Right not ..src.thermo or .src.thermo

class ThermoTest(unittest.TestCase):
    def test_theta(self):
        actual = potential_temperature(100000, 300)
        expected = 300
        self.assertEqual(actual, expected)
