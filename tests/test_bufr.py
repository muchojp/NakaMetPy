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
    
    Method
    --------
      parse_tableB_into_dataframe
    Parameters
    --------
      version: `str`
    Notes
    --------
      `version`の指定なし
    """
    # print(self.test_parse_tableB_into_dataframe_001.__doc__)
    actual = parse_tableB_into_dataframe()
    actual_value = actual[actual["F-XX-YYY"] == "0-00-004"]["MNEMONIC"].values
    self.assertEqual(actual_value, "MTABL")
  
  def test_parse_tableB_into_dataframe_002(self):
    """
    test case: test_parse_tableB_into_dataframe_002
    
    Method
    --------
      parse_tableB_into_dataframe
    Parameters
    --------
      version: `str`
    Notes
    --------
      `version`の指定あり
    """
    # print(self.test_parse_tableB_into_dataframe_002.__doc__)
    for version, fxxyyy, expected in (("LOC_0_7_1", "0-01-195", "SACO"),
                                      ("STD_0_42", "0-01-024", "WSPDS")):
        with self.subTest(version=version, fxxyyy=fxxyyy, expected=expected):
          actual = parse_tableB_into_dataframe(version)
          # print(actual[actual["F-XX-YYY"] == fxxyyy])
          actual_value = actual[actual["F-XX-YYY"] == fxxyyy]["MNEMONIC"].values
          self.assertEqual(actual_value, expected)
  
  def test_parse_tableD_into_dict_001(self):
    """
    test case: test_parse_tableD_into_dict_001
    
    Method
    --------
      parse_tableD_into_dict
    Parameters
    --------
      version: `str`
    Notes
    --------
      `version`の指定なし
    """
    # print(self.test_parse_tableD_into_dict_001.__doc__)
    actual = parse_tableD_into_dict()
    self.assertEqual(actual["3-01-036"]["MNEMONIC"], "SHIPSEQ1")
    self.assertEqual(actual["3-01-036"]["NAME"], "Ship")
    self.assertEqual(actual["3-01-036"]["SEQUENCE"][2]["FXXYYY"], "3-01-011")
    self.assertEqual(actual["3-01-036"]["SEQUENCE"][2]["NAME"], "Year, month, day")

  def test_parse_tableD_into_dict_002(self):
    """
    test case: test_parse_tableD_into_dict_002
    
    Method
    --------
      parse_tableD_into_dict
    Parameters
    --------
      version: `str`
    Notes
    --------
      `version`の指定あり
    """
    # print(self.test_parse_tableD_into_dict_002.__doc__)
    for version, fxxyyy1, mnemonic, name1, fxxyyy2, name2 in (
      ("LOC_0_7_1", "3-52-003", "RCPTIM", "Report receipt time data", "0-04-204", "Receipt minute"),
      ("STD_0_30", "3-16-007", "FRONTSEQ", "Front", "0-31-001", "Delayed descriptor replication factor")):
      with self.subTest(version=version, fxxyyy1=fxxyyy1, mnemonic=mnemonic,
                        name1=name1, fxxyyy2=fxxyyy2, name2=name2):
        actual = parse_tableD_into_dict(version)
        self.assertEqual(actual[fxxyyy1]["MNEMONIC"], mnemonic)
        self.assertEqual(actual[fxxyyy1]["NAME"], name1)
        self.assertEqual(actual[fxxyyy1]["SEQUENCE"][5]["FXXYYY"], fxxyyy2)
        self.assertEqual(actual[fxxyyy1]["SEQUENCE"][5]["NAME"], name2)
  
  def test_parse_codeFlag_into_dict_001(self):
    """
    test case: test_parse_codeFlag_into_dict_001
    
    Method
    --------
      parse_codeFlag_into_dict
    Parameters
    --------
      version: `str`
    Notes
    --------
      `version`の指定なし
    """
    # print(self.test_parse_codeFlag_into_dict_001.__doc__)
    actual = parse_codeFlag_into_dict()
    # CODE, No dependency
    self.assertEqual(actual["0-01-007"]["MNEMONIC"], "SAID")
    self.assertEqual(actual["0-01-007"]["CODEFLAG"], "CODE")
    self.assertEqual(actual["0-01-007"]["HAS_DEPENDENCY"], False)
    self.assertEqual(actual["0-01-007"]["VALBITS"]["122"], "GCOM-W1")
    # FLAG, No dependency
    self.assertEqual(actual["0-02-002"]["MNEMONIC"], "TIWM")
    self.assertEqual(actual["0-02-002"]["CODEFLAG"], "FLAG")
    self.assertEqual(actual["0-02-002"]["HAS_DEPENDENCY"], False)
    self.assertEqual(actual["0-02-002"]["VALBITS"]["3"], "Originally measured in km h**-1")
    # CODE, has dependency
    self.assertEqual(actual["0-01-034"]["MNEMONIC"], "GSES")
    self.assertEqual(actual["0-01-034"]["CODEFLAG"], "CODE")
    self.assertEqual(actual["0-01-034"]["HAS_DEPENDENCY"], True)
    self.assertEqual(len(actual["0-01-034"]["VALBITS"].keys()), 3)
    self.assertEqual(len(actual["0-01-034"]["VALBITS"]["0-01-031"]["34"].keys()), 4)
    self.assertEqual(actual["0-01-034"]["VALBITS"]["0-01-031"]["34"]["240"], "Kiyose")
    self.assertEqual(actual["0-01-034"]["VALBITS"]["0-01-035"]["46"]["0"], "No sub-centre")
  
  def test_parse_codeFlag_into_dict_002(self):
    """
    test case: test_parse_codeFlag_into_dict_002
    
    Method
    --------
      parse_codeFlag_into_dict
    Parameters
    --------
      version: `str`
    Notes
    --------
      `version`の指定なし
    """
    # print(self.test_parse_codeFlag_into_dict_002.__doc__)
    actual = parse_codeFlag_into_dict("LOC_0_7_1")
    # CODE, No dependency
    self.assertEqual(actual["0-02-194"]["MNEMONIC"], "AUTO")
    self.assertEqual(actual["0-02-194"]["CODEFLAG"], "CODE")
    self.assertEqual(actual["0-02-194"]["HAS_DEPENDENCY"], False)
    self.assertEqual(actual["0-02-194"]["VALBITS"]["3"], "METAR/SPECI report with 'A01' found in report, but 'AUTO' not found in report")
    # FLAG, No dependency
    self.assertEqual(actual["0-33-200"]["MNEMONIC"], "WSEQC1")
    self.assertEqual(actual["0-33-200"]["CODEFLAG"], "FLAG")
    self.assertEqual(actual["0-33-200"]["HAS_DEPENDENCY"], False)
    self.assertEqual(actual["0-33-200"]["VALBITS"]["26"], "Rain flag based on TBs (or from SDR processor)")
    # CODE, has dependency
    self.assertEqual(actual["0-07-246"]["MNEMONIC"], "PQM")
    self.assertEqual(actual["0-07-246"]["CODEFLAG"], "CODE")
    self.assertEqual(actual["0-07-246"]["HAS_DEPENDENCY"], True)
    self.assertEqual(len(actual["0-07-246"]["VALBITS"].keys()), 1)
    self.assertEqual(len(actual["0-07-246"]["VALBITS"]["0-07-247"]["1"].keys()), 9)
    self.assertEqual(actual["0-07-246"]["VALBITS"]["0-07-247"]["1"]["15"], "Observation is flagged for non-use by analysis")
    self.assertEqual(actual["0-07-246"]["VALBITS"]["0-07-247"]["14"]["1"], "Good")