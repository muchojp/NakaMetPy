# Copyright (c) 2024, NakaMetPy Develoers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# Command Example1: python -m unittest tests/test_util.py -v
# Command Example2: python -m unittest tests.test_util -v
# Command Example3: python -m unittest tests.test_util.UtilTest.test_load_jmara250m_grib2_001 -v
# 
import unittest
from src.nakametpy.util import dt_ymdhm, dt_yyyymmdd, unit_ms1_knots, unit_knots_ms1,\
                               anom_levels, concat_array, myglob, check_tar_content,\
                               load_jmara_grib2, get_jmara_lat, get_jmara_lon,\
                               load_jmara250m_grib2,\
                               get_grib2_latlon, get_gsmap_lat, get_gsmap_lon,\
                               jma_rain_lat, jma_rain_lon, gsmap_lat, gsmap_lon
from src.nakametpy._error import NotHaveSetArgError, NotMatchTarContentNameError
import os
import numpy as np

class UtilTest(unittest.TestCase):
  def test_dt_ymdhm_001(self):
    """
    test case: test_dt_ymdhm_001
    method:
      dt_ymdhm
    args:
      date: `datetime.datetime`
    note:
      opt の指定無し
    """
    # print(self.test_dt_ymdhm_001.__doc__)
    
    import datetime
    date = datetime.datetime(2024, 3, 3, 8, 1, 9)
    actual = dt_ymdhm(date)
    expect = ("2024", "03", "03", "08", "01", "09")
    
  def test_dt_ymdhm_002(self):
    """
    test case: test_dt_ymdhm_002
    method:
      dt_ymdhm
    args:
      date: `datetime.datetime`
      opt=1: `int`
    """
    # print(self.test_dt_ymdhm_002.__doc__)
    
    import datetime
    date = datetime.datetime(2024, 3, 3, 8, 1, 9)
    actual = dt_ymdhm(date, opt=1)
    expect = ("2024", "03", "03", "08", "01", "09")
    
  def test_dt_ymdhm_003(self):
    """
    test case: test_dt_ymdhm_003
    method:
      dt_ymdhm
    args:
      date: `datetime.datetime`
      opt=0: `int`
    """
    # print(self.test_dt_ymdhm_003.__doc__)
    
    import datetime
    date = datetime.datetime(2024, 3, 3, 8, 1, 9)
    actual = dt_ymdhm(date, opt=0)
    expect = (2024, 3, 3, 8, 1, 9)


  def test_dt_yyyymmdd_001(self):
    """
    test case: test_dt_yyyymmdd_001
    method:
      dt_yyyymmdd
    args:
      date: `datetime.datetime`
      fmt: `str`
    note:
      fmt の指定無し
    """
    # print(self.test_dt_yyyymmdd_001.__doc__)
    
    import datetime
    date = datetime.datetime(2024, 3, 3, 8, 1, 9)
    actual = dt_yyyymmdd(date)
    expected = "20240303"
    self.assertEqual(actual, expected)
      
  def test_dt_yyyymmdd_002(self):
    """
    test case: test_dt_yyyymmdd_002
    method:
      dt_yyyymmdd
    args:
      date: `datetime.datetime`
      fmt='yyyymmdd': `str`
    """
    # print(self.test_dt_yyyymmdd_002.__doc__)
    
    import datetime
    date = datetime.datetime(2024, 3, 3, 8, 1, 9)
    actual = dt_yyyymmdd(date, fmt="yyyymmdd")
    expected = "20240303"
    self.assertEqual(actual, expected)
      
  def test_dt_yyyymmdd_003(self):
    """
    test case: test_dt_yyyymmdd_003
    method:
      dt_yyyymmdd
    args:
      date: `datetime.datetime`
      fmt='yyyymmddHHMMSS': `str`
    """
    # print(self.test_dt_yyyymmdd_003.__doc__)
    
    import datetime
    date = datetime.datetime(2024, 3, 3, 8, 1, 9)
    actual = dt_yyyymmdd(date, fmt="yyyymmddHHMMSS")
    expected = "20240303080109"
    self.assertEqual(actual, expected)
      
  def test_dt_yyyymmdd_004(self):
    """
    test case: test_dt_yyyymmdd_004
    method:
      dt_yyyymmdd
    args:
      date: `datetime.datetime`
      fmt='hoge_yymmdd_HHMM': `str`
    """
    # print(self.test_dt_yyyymmdd_004.__doc__)
    
    import datetime
    date = datetime.datetime(2024, 3, 3, 8, 1, 9)
    actual = dt_yyyymmdd(date, fmt="hoge_yymmdd_HHMM")
    expected = "hoge_240303_0801"
    self.assertEqual(actual, expected)


  def test_unit_ms1_knots_001(self):
    """
    test case: test_unit_ms1_knots_001
    method:
      unit_ms1_knots
    args:
      ms: `int`or`float`
    """
    # print(self.test_unit_ms1_knots_001.__doc__)
    
    ms = 17
    actual = unit_ms1_knots(ms)
    expected = ms*3600/1852
    self.assertEqual(actual, expected)


  def test_unit_knots_ms1_001(self):
    """
    test case: test_unit_knots_ms1_001
    method:
      unit_knots_ms1
    args:
      kt: `int`or`float`
    """
    # print(self.test_unit_knots_ms1_001.__doc__)
    
    kt = 34
    actual = unit_knots_ms1(kt)
    expected = kt*1852/3600
    self.assertEqual(actual, expected)


  def test_anom_levels_001(self):
    """
    test case: test_anom_levels_001
    method:
      anom_levels
    args:
      levs: `list`
    """
    # print(self.test_anom_levels_001.__doc__)
    
    import numpy as np
    levs = [1, 2, 3]
    actual = anom_levels(levs)
    expected = np.array((-3, -2, -1, 1, 2, 3))
    self.assertEqual(len(actual), len(expected))
    for i in range(len(actual)):
      self.assertEqual(actual[i], expected[i])

  def test_anom_levels_002(self):
    """
    test case: test_anom_levels_002
    method:
      anom_levels
    args:
      levs: `list`
    note:
      負の値がある場合のチェック
    """
    # print(self.test_anom_levels_002.__doc__)
    
    import numpy as np
    levs = [-1, 2, 3]
    actual = anom_levels(levs)
    expected = np.array((-3, -2, -1, 1, 2, 3))
    self.assertEqual(len(actual), len(expected))
    for i in range(len(actual)):
      self.assertEqual(actual[i], expected[i])

  def test_anom_levels_003(self):
    """
    test case: test_anom_levels_003
    method:
      anom_levels
    args:
      levs: `numpy.ndarray`
    """
    # print(self.test_anom_levels_003.__doc__)
    
    import numpy as np
    levs = np.array([1, 2, 3])
    actual = anom_levels(levs)
    expected = np.array((-3, -2, -1, 1, 2, 3))
    self.assertEqual(len(actual), len(expected))
    for i in range(len(actual)):
      self.assertEqual(actual[i], expected[i])

  def test_anom_levels_004(self):
    """
    test case: test_anom_levels_004
    method:
      anom_levels
    args:
      levs: `numpy.ndarray`
    note:
      負の値がある場合のチェック
    """
    # print(self.test_anom_levels_004.__doc__)
    
    import numpy as np
    levs = np.array([-1, 2, 3])
    actual = anom_levels(levs)
    expected = np.array((-3, -2, -1, 1, 2, 3))
    self.assertEqual(len(actual), len(expected))
    for i in range(len(actual)):
      self.assertEqual(actual[i], expected[i])


  def test_concat_array_001(self):
    """
    test case: test_concat_array_001
    method:
      concat_array
    args:
      levs1: `list`
      levs2: `list`
    """
    # print(self.test_concat_array_001.__doc__)
    
    import numpy as np
    levs1 = [-1, 2, 3]
    levs2 = [4, 5, -6]
    actual = concat_array(levs1, levs2)
    expected = np.array((-6, -1, 2, 3, 4, 5))
    self.assertEqual(len(actual), len(expected))
    for i in range(len(actual)):
      self.assertEqual(actual[i], expected[i])

  def test_concat_array_002(self):
    """
    test case: test_concat_array_002
    method:
      concat_array
    args:
      levs1: `list`
      levs2: `list`
      sort=True: `bool`
    """
    # print(self.test_concat_array_002.__doc__)
    
    import numpy as np
    levs1 = [-1, 2, 3]
    levs2 = [4, 5, -6]
    actual = concat_array(levs1, levs2, sort=True)
    expected = np.array((-6, -1, 2, 3, 4, 5))
    self.assertEqual(len(actual), len(expected))
    for i in range(len(actual)):
      self.assertEqual(actual[i], expected[i])

  def test_concat_array_003(self):
    """
    test case: test_concat_array_003
    method:
      concat_array
    args:
      levs1: `list`
      levs2: `list`
      sort=False: `bool`
    """
    # print(self.test_concat_array_003.__doc__)
    
    import numpy as np
    levs1 = [-1, 2, 3]
    levs2 = [4, 5, -6]
    actual = concat_array(levs1, levs2, sort=False)
    expected = np.array((-1, 2, 3, 4, 5, -6))
    self.assertEqual(len(actual), len(expected))
    for i in range(len(actual)):
      self.assertEqual(actual[i], expected[i])


  def test_myglob_001(self):
    """
    test case: test_myglob_001
    method:
      myglob
    args:
      path: `str`
    """
    # print(self.test_myglob_001.__doc__)
    
    path = "./tests/data/util/myglob/*"
    actual = myglob(path)
    expected = list((os.path.join("./tests/data/util/myglob", "test1.txt"), os.path.join("./tests/data/util/myglob", "test2.txt")))
    self.assertEqual(actual, expected)

  def test_myglob_002(self):
    """
    test case: test_myglob_002
    method:
      myglob
    args:
      path: `str`
      reverse=False: `bool`
    """
    # print(self.test_myglob_002.__doc__)
    
    path = "./tests/data/util/myglob/*"
    actual = myglob(path, reverse=False)
    expected = list((os.path.join("./tests/data/util/myglob", "test1.txt"), os.path.join("./tests/data/util/myglob", "test2.txt")))
    self.assertEqual(actual, expected)

  def test_myglob_003(self):
    """
    test case: test_myglob_003
    method:
      myglob
    args:
      path: `str`
      reverse=True: `bool`
    """
    # print(self.test_myglob_003.__doc__)
    
    path = "./tests/data/util/myglob/*"
    actual = myglob(path, reverse=True)
    expected = list((os.path.join("./tests/data/util/myglob", "test2.txt"), os.path.join("./tests/data/util/myglob", "test1.txt")))
    self.assertEqual(actual, expected)
  
  def test_check_tar_content_001(self):
    """
    test case: test_check_tar_content_001
    method:
      check_tar_content
    args:
      file: `str`
    """
    # print(self.test_check_tar_content_001.__doc__)
    
    import sys
    from io import StringIO
    import tarfile
    
    file = "./tests/data/util/check_tar_content/test.tar"
    
    inout = StringIO()
    # 標準出力を inout に結びつける
    sys.stdout = inout
    check_tar_content(file)
    # 標準出力を元に戻す
    sys.stdout = sys.__stdout__
    
    actual = inout.getvalue()
    expected = "test\ntest/test1.txt\ntest/test2.txt\n"
    self.assertEqual(actual, expected)
  
  def test_load_jmara_grib2_001(self):
    """
    test case: test_load_jmara_grib2_001
    method:
      load_jmara_grib2
    args:
      file: `str`
    """
    # print(self.test_load_jmara_grib2_001.__doc__)
    
    path = "./tests/data/util/load_jmara_grib2/Z__C_RJTD_20220808000000_RDR_JMAGPV_Ggis1km_Prr10lv_ANAL_grib2.bin"
    actual = load_jmara_grib2(path).shape
    expected = (3360, 2560)
    self.assertEqual(actual, expected)
  
  def test_load_jmara_grib2_002(self):
    """
    test case: test_load_jmara_grib2_002
    method:
      load_jmara_grib2
    args:
      file: `str`
      tar_flag=False: `bool`
    """
    # print(self.test_load_jmara_grib2_002.__doc__)
    
    path = "./tests/data/util/load_jmara_grib2/Z__C_RJTD_20220808000000_RDR_JMAGPV_Ggis1km_Prr10lv_ANAL_grib2.bin"
    actual = load_jmara_grib2(path, tar_flag=False).shape
    expected = (3360, 2560)
    self.assertEqual(actual, expected)
  
  def test_load_jmara_grib2_003(self):
    """
    test case: test_load_jmara_grib2_003
    method:
      load_jmara_grib2
    args:
      file: `str`
    """
    # print(self.test_load_jmara_grib2_003.__doc__)
    
    path = "./tests/data/util/load_jmara_grib2/Z__C_RJTD_20220808000000_RDR_JMAGPV_Gll2p5km_Phhlv_ANAL_grib2.bin"
    actual = load_jmara_grib2(path).shape
    expected = (1120, 1024)
    self.assertEqual(actual, expected)
  
  def test_load_jmara_grib2_004(self):
    """
    test case: test_load_jmara_grib2_004
    method:
      load_jmara_grib2
    args:
      file: `str`
      tar_flag=False: `bool`
    """
    # print(self.test_load_jmara_grib2_004.__doc__)
    
    path = "./tests/data/util/load_jmara_grib2/Z__C_RJTD_20220808000000_RDR_JMAGPV_Gll2p5km_Phhlv_ANAL_grib2.bin"
    actual = load_jmara_grib2(path, tar_flag=False).shape
    expected = (1120, 1024)
    self.assertEqual(actual, expected)
  
  def test_load_jmara_grib2_005(self):
    """
    test case: test_load_jmara_grib2_005
    method:
      load_jmara_grib2
    args:
      file: `str`
      tar_flag=False: `True`
    """
    # print(self.test_load_jmara_grib2_005.__doc__)
    
    path = "./tests/data/util/load_jmara_grib2/Z__C_RJTD_20220808000000_RDR_JMAGPV__grib2.tar"
    with self.assertRaises(NotHaveSetArgError):
      load_jmara_grib2(path, tar_flag=True)
  
  def test_load_jmara_grib2_006(self):
    """
    test case: test_load_jmara_grib2_006
    method:
      load_jmara_grib2
    args:
      file: `str`
      tar_flag=False: `True`
      tar_contentname="hoge": `str`
    """
    # print(self.test_load_jmara_grib2_006.__doc__)
    
    path = "./tests/data/util/load_jmara_grib2/Z__C_RJTD_20220808000000_RDR_JMAGPV__grib2.tar"
    with self.assertRaises(NotMatchTarContentNameError):
      load_jmara_grib2(path, tar_flag=True, tar_contentname="hoge")
  
  def test_load_jmara_grib2_007(self):
    """
    test case: test_load_jmara_grib2_007
    method:
      load_jmara_grib2
    args:
      file: `str`
      tar_flag=False: `True`
      tar_contentname="Z__C_RJTD_20220808000000_RDR_JMAGPV_Ggis1km_Prr10lv_ANAL_grib2.bin": `str`
    """
    # print(self.test_load_jmara_grib2_007.__doc__)
    
    path = "./tests/data/util/load_jmara_grib2/Z__C_RJTD_20220808000000_RDR_JMAGPV__grib2.tar"
    tar_contentname = "Z__C_RJTD_20220808000000_RDR_JMAGPV_Ggis1km_Prr10lv_ANAL_grib2.bin"
    actual = load_jmara_grib2(path, tar_flag=True, tar_contentname=tar_contentname).shape
    expected = (3360, 2560)
    self.assertEqual(actual, expected)
  
  def test_load_jmara_grib2_008(self):
    """
    test case: test_load_jmara_grib2_008
    method:
      load_jmara_grib2
    args:
      file: `str`
      tar_flag=False: `True`
      tar_contentname="Z__C_RJTD_20220808000000_RDR_JMAGPV_Gll2p5km_Phhlv_ANAL_grib2.bin": `str`
    """
    # print(self.test_load_jmara_grib2_008.__doc__)
    
    path = "./tests/data/util/load_jmara_grib2/Z__C_RJTD_20220808000000_RDR_JMAGPV__grib2.tar"
    tar_contentname = "Z__C_RJTD_20220808000000_RDR_JMAGPV_Gll2p5km_Phhlv_ANAL_grib2.bin"
    actual = load_jmara_grib2(path, tar_flag=True, tar_contentname=tar_contentname).shape
    expected = (1120, 1024)
    self.assertEqual(actual, expected)
  
  def test_load_jmara_grib2_009(self):
    """
    test case: test_load_jmara_grib2_009
    method:
      load_jmara_grib2
    args:
      file: `str`
    """
    # print(self.test_load_jmara_grib2_009.__doc__)
    
    path = "./tests/data/util/load_jmara_grib2/Z__C_RJTD_20240301000000_RDR_GPV_Ggis1km_Phhlv_Aper5min_ANAL_grib2.bin"
    actual = load_jmara_grib2(path).shape
    expected = (3360, 2560)
    self.assertEqual(actual, expected)
  
  def test_load_jmara_grib2_010(self):
    """
    test case: test_load_jmara_grib2_010
    method:
      load_jmara_grib2
    args:
      file: `str`
    """
    # print(self.test_load_jmara_grib2_010.__doc__)
    
    path = "./tests/data/util/load_jmara_grib2/Z__C_RJTD_20240301000000_RDR_GPV_Ggis1km_Phhlv_Aper5min_ANAL_grib2.bin"
    actual = load_jmara_grib2(path).shape
    expected = (3360, 2560)
    self.assertEqual(actual, expected)
  
  def test_load_jmara_grib2_011(self):
    """
    test case: test_load_jmara_grib2_011
    method:
      load_jmara_grib2
    args:
      file: `str`
    """
    # print(self.test_load_jmara_grib2_011.__doc__)
    
    path = "./tests/data/util/load_jmara_grib2/Z__C_RJTD_20240301000000_RDR_GPV_Ggis1km_Phhlv_Aper5min_ANAL_grib2.bin.gz"
    actual = load_jmara_grib2(path).shape
    expected = (3360, 2560)
    self.assertEqual(actual, expected)
  
  def test_load_jmara_grib2_012(self):
    """
    test case: test_load_jmara_grib2_012
    method:
      load_jmara_grib2
    args:
      file: `str`
    """
    # print(self.test_load_jmara_grib2_012.__doc__)
    
    path = "./tests/data/util/load_jmara_grib2/Z__C_RJTD_20241018000500_RDR_JMAGPV_Ggis1km_Prr05lv_ANAL_grib2.bin"
    actual = load_jmara_grib2(path).shape
    expected = (3360, 2560)
    self.assertEqual(actual, expected)

  def test_get_jmara_lat_001(self):
    """
    test case: test_get_jmara_lat_001
    method:
      get_jmara_lat
    """
    # print(self.test_get_jmara_lat_001.__doc__)
    actual_lat = get_jmara_lat()
    self.assertEqual(actual_lat.size, 3360)
    self.assertEqual(jma_rain_lat.size, 3360)

  def test_get_jmara_lat_002(self):
    """
    test case: test_get_jmara_lat_002
    method:
      get_jmara_lat
    """
    # print(self.test_get_jmara_lat_002.__doc__)
    for mesh, nlat in ((None, 3360), (2500, 1120), (1000, 3360), (250, 13440)):
      with self.subTest(mesh=mesh, nlat=nlat):
        actual_lat = get_jmara_lat(mesh)
        self.assertEqual(actual_lat.size, nlat)

  def test_get_jmara_lon_001(self):
    """
    test case: test_get_jmara_lon_001
    method:
      get_jmara_lon
    args:
      mesh: `int`
    """
    # print(self.test_get_jmara_lon_001.__doc__)
    actual_lon = get_jmara_lon()
    self.assertEqual(actual_lon.size, 2560)
    self.assertEqual(jma_rain_lon.size, 2560)

  def test_get_jmara_lon_002(self):
    """
    test case: test_get_jmara_lon_002
    method:
      get_jmara_lon
    """
    # print(self.test_get_jmara_lon_002.__doc__)
    for mesh, nlon in ((None, 2560), (2500, 1024), (1000, 2560), (250, 10240)):
      with self.subTest(mesh=mesh, nlon=nlon):
        actual_lon = get_jmara_lon(mesh)
        self.assertEqual(actual_lon.size, nlon)

  def test_load_jmara250m_grib2_001(self):
    """
    test case: test_load_jmara250m_grib2_001
    method:
      load_jmara250m_grib2
    args:
      file: `str`
    """
    # print(self.test_load_jmara250m_grib2_001.__doc__)
    
    path = "./tests/data/util/load_jmara250m_grib2/Z__C_RJTD_20210706233000_RDR_GPV_Ggis0p25km_Pri60lv_Aper5min_ANAL_grib2.bin"
    actual_array_0250m, actual_array_1000m = load_jmara250m_grib2(path)
    expected_0250m = (13440, 10240)
    expected_1000m = (3360, 2560)
    self.assertEqual(actual_array_0250m.shape, expected_0250m)
    self.assertEqual(actual_array_1000m.shape, expected_1000m)

  def test_load_jmara250m_grib2_002(self):
    """
    test case: test_load_jmara250m_grib2_002
    method:
      load_jmara250m_grib2
    args:
      file: `str`
    """
    # print(self.test_load_jmara250m_grib2_002.__doc__)
    
    path = "./tests/data/util/load_jmara250m_grib2/Z__C_RJTD_20210706233000_RDR_GPV_Ggis0p25km_Pri60lv_Aper5min_ANAL_grib2.bin.gz"
    actual_array_0250m, actual_array_1000m = load_jmara250m_grib2(path)
    expected_0250m = (13440, 10240)
    expected_1000m = (3360, 2560)
    self.assertEqual(actual_array_0250m.shape, expected_0250m)
    self.assertEqual(actual_array_1000m.shape, expected_1000m)

  def test_load_jmara250m_grib2_003(self):
    """
    test case: test_load_jmara250m_grib2_003
    method:
      load_jmara250m_grib2
    """
    # print(self.test_load_jmara250m_grib2_003.__doc__)
    path = "./tests/data/util/load_jmara250m_grib2/Z__C_RJTD_20210706233000_RDR_GPV_Ggis0p25km_Pri60lv_Aper5min_ANAL_grib2.bin"
    index_list = (3360//2+200, 2560//2)
    for only250, expectedType in ((False, np.float64), (True, np.ma.core.MaskedConstant)):
      with self.subTest(only250=only250, expectedType=expectedType):
        _, actual_array_1000m = load_jmara250m_grib2(path, only250=only250)
        self.assertIsInstance(actual_array_1000m[index_list], expectedType)

  def test_load_jmara250m_grib2_004(self):
    """
    test case: test_load_jmara250m_grib2_004
    method:
      load_jmara250m_grib2
    """
    # print(self.test_load_jmara250m_grib2_004.__doc__)
    path = "./tests/data/util/load_jmara250m_grib2/Z__C_RJTD_20210706233000_RDR_GPV_Ggis0p25km_Pri60lv_Aper5min_ANAL_grib2.bin.gz"
    index_list = (3360//2+200, 2560//2)
    for only250, expectedType in ((False, np.float64), (True, np.ma.core.MaskedConstant)):
      with self.subTest(only250=only250, expectedType=expectedType):
        _, actual_array_1000m = load_jmara250m_grib2(path, only250=only250)
        self.assertIsInstance(actual_array_1000m[index_list], expectedType)

  def test_get_grib2_latlon_001(self):
    """
    test case: test_get_grib2_latlon_001
    method:
      get_grib2_latlon
    """
    # print(self.test_get_grib2_latlon_001.__doc__)
    path = "./tests/data/util/load_jmara_grib2/Z__C_RJTD_20220808000000_RDR_JMAGPV_Ggis1km_Prr10lv_ANAL_grib2.bin"
    actual_glat, actual_glon = get_grib2_latlon(path)
    self.assertEqual(actual_glat.size, 3360)
    self.assertEqual(actual_glon.size, 2560)

  def test_get_jmara_latlon_001(self):
    """
    test case: test_get_jmara_lat_001
    method:
      get_jmara_lat
    """
    # print(self.test_get_jmara_lat_001.__doc__)
    actual_lat = get_jmara_lat()
    actual_lon = get_jmara_lon()
    path = "./tests/data/util/load_jmara_grib2/Z__C_RJTD_20220808000000_RDR_JMAGPV_Ggis1km_Prr10lv_ANAL_grib2.bin"
    actual_glat, actual_glon = get_grib2_latlon(path)
    actual1 = np.all(np.isclose(actual_lat, actual_glat, atol=1E-6, rtol=0, equal_nan=False))
    self.assertEqual(actual1, True)
    actual2 = np.all(np.isclose(actual_lon, actual_glon, atol=1E-6, rtol=0, equal_nan=False))
    self.assertEqual(actual2, True)
    actual3 = np.all(np.isclose(jma_rain_lat, actual_glat, atol=1E-6, rtol=0, equal_nan=False))
    self.assertEqual(actual3, True)
    actual4 = np.all(np.isclose(jma_rain_lon, actual_glon, atol=1E-6, rtol=0, equal_nan=False))
    self.assertEqual(actual4, True)

  def test_get_gsmap_lat_001(self):
    """
    test case: test_get_gsmap_lat_001
    method:
      get_gsmap_lat
    """
    # print(self.test_get_gsmap_lat_001.__doc__)
    actual_lat = get_gsmap_lat()
    self.assertEqual(actual_lat.size, 1200)
    self.assertEqual(gsmap_lat.size, 1200)

  def test_get_gsmap_lon_001(self):
    """
    test case: test_get_gsmap_lon_001
    method:
      get_gsmap_lon
    """
    # print(self.test_get_gsmap_lon_001.__doc__)
    actual_lon = get_gsmap_lon()
    self.assertEqual(actual_lon.size, 3600)
    self.assertEqual(gsmap_lon.size, 3600)
