# Copyright (c) 2025, NakaMetPy Develoers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# Command Example1: python -m unittest tests/test_aviation.py -v
# Command Example2: python -m unittest tests.test_aviation -v
# Command Example3: python -m unittest tests.test_aviation.UtilTest.test_search_icao_airport_code_match_001 -v
# 
import unittest
from src.nakametpy.aviation import airport_info

class UtilTest(unittest.TestCase):
  def test_search_icao_airport_code_001(self):
    """
    test case: test_search_icao_airport_code_001
    
    Method
    --------
      search_icao_airport_code
    Parameters
    --------
      code: `str`
    """
    # print(self.test_search_icao_airport_code_001.__doc__)
    actual = airport_info()
    # 'RJAA', 'NRT', '-', '47686', 35.765, 140.386, 36, 'Narita Intl', '12', 'JP', 4
    actual_value = actual.search_icao_airport_code("RJAA").values[0]
    self.assertEqual("RJAA", actual_value[0])
    self.assertEqual("NRT", actual_value[1])
    self.assertEqual("-", actual_value[2])
    self.assertEqual("47686", actual_value[3])
    self.assertEqual(35.765, actual_value[4])
    self.assertEqual(140.386, actual_value[5])
    self.assertEqual(36, actual_value[6])
    self.assertEqual('Narita Intl', actual_value[7])
    self.assertEqual('12', actual_value[8])
    self.assertEqual('JP', actual_value[9])
    self.assertEqual(4, actual_value[10])
  
  def test_search_icao_airport_code_002(self):
    """
    test case: test_search_icao_airport_code_002
    
    Method
    --------
      search_icao_airport_code
    Parameters
    --------
      code: `str`
    """
    # print(self.test_search_icao_airport_code_002.__doc__)
    actual = airport_info()
    actual_value = actual.search_icao_airport_code("RJFF")
    self.assertEqual('RJFF', actual_value["icaoId"].values)
    self.assertEqual('FUK', actual_value["iataId"].values)
    self.assertEqual('-', actual_value["faaId"].values)
    self.assertEqual('47808', actual_value["wmoId"].values)
    self.assertEqual(33.584, actual_value["lat"].values)
    self.assertEqual(130.452, actual_value["lon"].values)
    self.assertEqual(7, actual_value["elev"].values)
    self.assertEqual('Fukuoka Arpt', actual_value["site"].values)
    self.assertEqual('40', actual_value["state"].values)
    self.assertEqual('JP', actual_value["country"].values)
    self.assertEqual(3, actual_value["priority"].values)
  
  def test_search_iata_airport_code_001(self):
    """
    test case: test_search_iata_airport_code_001
    
    Method
    --------
      search_iata_airport_code
    Parameters
    --------
      code: `str`
    """
    # print(self.test_search_iata_airport_code_001.__doc__)
    actual = airport_info()
    actual_value = actual.search_iata_airport_code("KIX").values[0]
    # 'RJBB', 'KIX', '-', '47774', 34.434, 135.233, 8, 'Osaka\/Kansai Intl', '28', 'JP', 4
    self.assertEqual("RJBB", actual_value[0])
    self.assertEqual("KIX", actual_value[1])
    self.assertEqual("-", actual_value[2])
    self.assertEqual("47774", actual_value[3])
    self.assertEqual(34.434, actual_value[4])
    self.assertEqual(135.233, actual_value[5])
    self.assertEqual(8, actual_value[6])
    self.assertEqual('Osaka/Kansai Intl', actual_value[7])
    self.assertEqual('28', actual_value[8])
    self.assertEqual('JP', actual_value[9])
    self.assertEqual(4, actual_value[10])
  
  def test_search_iata_airport_code_002(self):
    """
    test case: test_search_iata_airport_code_002
    
    Method
    --------
      search_iata_airport_code
    Parameters
    --------
      code: `str`
    """
    # print(self.test_search_iata_airport_code_002.__doc__)
    actual = airport_info()
    actual_value = actual.search_iata_airport_code("NGS")
    self.assertEqual('RJFU', actual_value["icaoId"].values[0])
    self.assertEqual('NGS', actual_value["iataId"].values[0])
    self.assertEqual('-', actual_value["faaId"].values[0])
    self.assertEqual('47855', actual_value["wmoId"].values[0])
    self.assertEqual(32.917, actual_value["lat"].values[0])
    self.assertEqual(129.914, actual_value["lon"].values[0])
    self.assertEqual(2, actual_value["elev"].values[0])
    self.assertEqual('Nagasaki Arpt', actual_value["site"].values[0])
    self.assertEqual('42', actual_value["state"].values[0])
    self.assertEqual('JP', actual_value["country"].values[0])
    self.assertEqual(2, actual_value["priority"].values[0])

  def test_search_icao_airport_code_match_001(self):
    """
    test case: test_search_icao_airport_code_match_001
    
    Method
    --------
      search_icao_airport_code_match
    Parameters
    --------
      code: `str`
    """
    # print(self.test_search_icao_airport_code_match_001.__doc__)
    actual = airport_info()
    self.assertEqual(16, len(actual.search_icao_airport_code_match(r'^RJF[a-zA-Z0-9]+$').values))

  def test_search_iata_airport_code_match_001(self):
    """
    test case: test_search_iata_airport_code_match_001
    
    Method
    --------
      search_iata_airport_code_match
    Parameters
    --------
      code: `str`
    """
    # print(self.test_search_iata_airport_code_match_001.__doc__)
    actual = airport_info()
    self.assertEqual(18, len(actual.search_iata_airport_code_match(r'.*AX.*').values))

  def test_search_elem_code_match_001(self):
    """
    test case: test_search_elem_code_match_001
    
    Method
    --------
      search_elem_code_match
    Parameters
    --------
      elem: `str`
      code: `str`
    """
    # print(self.test_search_elem_code_match_001.__doc__)
    actual = airport_info()
    self.assertEqual(2, len(actual.search_elem_code_match("site", r'.*\(NPMOD\)$').values))

  def test_get_df_001(self):
    """
    test case: test_get_df_001
    
    Method
    --------
      get_df
    """
    # print(self.test_get_df_001.__doc__)
    actual = airport_info()
    self.assertEqual(9747, len(actual.get_df().values))

  def test_get_columns_001(self):
    """
    test case: test_get_columns_001
    
    Method
    --------
      get_columns
    """
    # print(self.test_get_columns_001.__doc__)
    actual = airport_info()
    self.assertEqual(11, len(actual.get_columns()))