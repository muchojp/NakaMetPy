# Copyright (c) 2021-2024, NakaMetPy Develoers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# Command Example: python -m unittest tests/test_thermo.py -v
# 
import unittest
from src.nakametpy.thermo import potential_temperature
# For Travis CI src.thermo is Right not ..src.thermo or .src.thermo

class ThermoTest(unittest.TestCase):
  def test_theta(self):
    actual = potential_temperature(100000, 300)
    expected = 300
    self.assertEqual(actual, expected)
