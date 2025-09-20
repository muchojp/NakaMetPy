# Copyright (c) 2025, NakaMetPy Develoers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# Command Example1: python -m unittest tests/product/test_synop1min.py -v
# Command Example2: python -m unittest tests.product.test_synop1min -v
# Command Example3: python -m unittest tests.product.test_synop1min.UtilTest.test_synop1min_001 -v
# 
import unittest
from src.nakametpy.product.synop1min import synop1min
import os
import glob

class UtilTest(unittest.TestCase):
  def test_synop1min_001(self):
    """
    test case: test_synop1min_001
    
    Method
    --------
      get_telegram_header
    """
    # print(self.test_synop1min_001.__doc__)
  filelist = glob.glob(os.path.join(os.path.dirname(__file__), "../data/product/synop1min/20241030000000/*"))
  for ifile in filelist:
    synop1min_class = synop1min(os.path.join(os.path.dirname(__file__), ifile))
    actual = synop1min_class.get_data(0)