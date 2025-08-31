# Copyright (c) 2025, NakaMetPy Develoers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# Command Example1: python -m unittest tests/product/test_liden.py -v
# Command Example2: python -m unittest tests.product.test_liden -v
# Command Example3: python -m unittest tests.product.test_liden.UtilTest.test_parse_tableB_into_dataframe_001 -v
# 
import unittest
from src.nakametpy.product.liden import liden
import os

class UtilTest(unittest.TestCase):
  def test_get_telegram_header_001(self):
    """
    test case: test_get_telegram_header_001
    
    Method
    --------
      get_telegram_header
    """
    # print(self.test_get_telegram_header_001.__doc__)
    actual = liden(os.path.join(os.path.dirname(__file__), "../data/product/liden/20160415_LIDEN_Sample.bin"))
    actual_value = actual.get_telegram_header()
    self.assertEqual("VFJP40", actual_value[0])
    self.assertEqual("RJTT", actual_value[1])
    self.assertEqual("151253", actual_value[2])
    
  def test_get_header_data_001(self):
    """
    test case: test_get_header_data_001
    
    Method
    --------
      get_header_data
    """
    # print(self.test_get_header_data_001.__doc__)
    actual = liden(os.path.join(os.path.dirname(__file__), "../data/product/liden/20160415_LIDEN_Sample.bin"))
    actual_value = actual.get_header_data()
    self.assertEqual(2016, actual_value[0])
    self.assertEqual(415, actual_value[1])
    self.assertEqual(1252, actual_value[2])
    self.assertEqual(0, actual_value[3])
    self.assertEqual(60, actual_value[4])
    self.assertEqual(15, actual_value[5])
    
  def test_get_data_001(self):
    """
    test case: test_get_data_001
    
    Method
    --------
      get_data
    """
    # print(self.test_get_data_001.__doc__)
    actual = liden(os.path.join(os.path.dirname(__file__), "../data/product/liden/20160415_LIDEN_Sample.bin"))
    actual_value = actual.get_data()[-4]
    self.assertEqual(1570, actual_value[0])
    self.assertEqual(35811, actual_value[1])
    self.assertEqual(39316, actual_value[2])
    self.assertEqual("  ", actual_value[3])
    self.assertEqual(" 4", actual_value[4])