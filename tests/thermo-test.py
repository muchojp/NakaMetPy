import unittest
from nakametpy.thermo import potential_temperature

class ThermoTest(unittest.TestCase):
    def test_theta(self):
        actual = potential_temperature(100000, 300)
        expected = 300
        self.assertEqual(actual, expected)
