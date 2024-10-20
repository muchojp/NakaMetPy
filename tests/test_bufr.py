# Copyright (c) 2024, NakaMetPy Develoers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# Command Example1: python -m unittest tests/test_bufr.py -v
# Command Example2: python -m unittest tests.test_bufr -v
# Command Example3: python -m unittest tests.test_bufr.UtilTest.test_parse_tableB_into_dataframe_001 -v
# 
import unittest
from src.nakametpy.bufr import parse_tableB_into_dataframe, parse_tableD_into_dict,\
                        parse_codeFlag_into_dict
import os
import pandas as pd
import numpy as np

class UtilTest(unittest.TestCase):
  def test_parse_tableB_into_dataframe_001(self):
    """
    test case: test_parse_tableB_into_dataframe_001
    method:
      parse_tableB_into_dataframe
    args:
      date: `datetime.datetime`
    note:
      opt の指定無し
    """
    # print(self.test_parse_tableB_into_dataframe_001.__doc__)
    actual = parse_tableB_into_dataframe()
    actual_value = actual[actual["F-XX-YYY"] == "0-00-004"]["MNEMONIC"].values
    self.assertEqual(actual_value, "MTABL")
  
  def test_parse_tableB_into_dataframe_002(self):
    """
    test case: test_parse_tableB_into_dataframe_002
    method:
      parse_tableB_into_dataframe
    args:
      date: `datetime.datetime`
    note:
      opt の指定無し
    """
    # print(self.test_parse_tableB_into_dataframe_002.__doc__)
    for version, fxxyyy, expected in (("LOC_0_7_1", "0-01-195", "SACO"),
                                      ("STD_0_42", "0-01-024", "WSPDS")):
      with self.subTest(version=version, fxxyyy=fxxyyy, expected=expected):
        actual = parse_tableB_into_dataframe()
        actual_value = actual[actual["F-XX-YYY"] == fxxyyy]["MNEMONIC"].values
        self.assertEqual(actual_value, expected)
        