import unittest
from src.nakametpy.util import dt_yyyymmdd

class UtilTest(unittest.TestCase):
    def test_dt_yyyymmdd_001(self):
        import datetime
        date = datetime.datetime(2024, 3, 23, 8, 15, 30)
        actual = dt_yyyymmdd(date)
        expected = "20240323"
        self.assertEqual(actual, expected)
