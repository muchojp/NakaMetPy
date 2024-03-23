import unittest
from src.nakametpy.util import dt_ymdhm, dt_yyyymmdd, unit_ms1_knots, unit_knots_ms1,\
                               anom_levels, concat_array, myglob, check_tar_content

class UtilTest(unittest.TestCase):
  def test_dt_ymdhm_001(self):
    import datetime
    date = datetime.datetime(2024, 3, 3, 8, 1, 9)
    actual = dt_ymdhm(date)
    expect = ("2024", "03", "03", "08", "01", "09")
    
  def test_dt_ymdhm_002(self):
    import datetime
    date = datetime.datetime(2024, 3, 3, 8, 1, 9)
    actual = dt_ymdhm(date, opt=1)
    expect = ("2024", "03", "03", "08", "01", "09")
    
  def test_dt_ymdhm_003(self):
    import datetime
    date = datetime.datetime(2024, 3, 3, 8, 1, 9)
    actual = dt_ymdhm(date, opt=0)
    expect = (2024, 3, 3, 8, 1, 9)


  def test_dt_yyyymmdd_001(self):
    import datetime
    date = datetime.datetime(2024, 3, 3, 8, 1, 9)
    actual = dt_yyyymmdd(date)
    expected = "20240303"
    self.assertEqual(actual, expected)
      
  def test_dt_yyyymmdd_002(self):
    import datetime
    date = datetime.datetime(2024, 3, 3, 8, 1, 9)
    actual = dt_yyyymmdd(date, fmt="yyyymmdd")
    expected = "20240303"
    self.assertEqual(actual, expected)
      
  def test_dt_yyyymmdd_003(self):
    import datetime
    date = datetime.datetime(2024, 3, 3, 8, 1, 9)
    actual = dt_yyyymmdd(date, fmt="yyyymmddHHMMSS")
    expected = "20240303080109"
    self.assertEqual(actual, expected)
      
  def test_dt_yyyymmdd_004(self):
    import datetime
    date = datetime.datetime(2024, 3, 3, 8, 1, 9)
    actual = dt_yyyymmdd(date, fmt="hoge_yymmdd_HHMM")
    expected = "hoge_240303_0801"
    self.assertEqual(actual, expected)


  def test_unit_ms1_knots_001(self):
    ms = 17
    actual = unit_ms1_knots(ms)
    expected = ms*3600/1852
    self.assertEqual(actual, expected)


  def test_unit_knots_ms1_001(self):
    kt = 34
    actual = unit_knots_ms1(kt)
    expected = kt*1852/3600
    self.assertEqual(actual, expected)


  def test_anom_levels_001(self):
    import numpy as np
    levs = [1, 2, 3]
    actual = anom_levels(levs)
    expected = np.array((-3, -2, -1, 1, 2, 3))
    self.assertEqual(len(actual), len(expected))
    for i in range(len(actual)):
      self.assertEqual(actual[i], expected[i])

  def test_anom_levels_002(self):
    import numpy as np
    levs = [-1, 2, 3]
    actual = anom_levels(levs)
    expected = np.array((-3, -2, -1, 1, 2, 3))
    self.assertEqual(len(actual), len(expected))
    for i in range(len(actual)):
      self.assertEqual(actual[i], expected[i])

  def test_anom_levels_003(self):
    import numpy as np
    levs = np.array([1, 2, 3])
    actual = anom_levels(levs)
    expected = np.array((-3, -2, -1, 1, 2, 3))
    self.assertEqual(len(actual), len(expected))
    for i in range(len(actual)):
      self.assertEqual(actual[i], expected[i])

  def test_anom_levels_004(self):
    import numpy as np
    levs = np.array([-1, 2, 3])
    actual = anom_levels(levs)
    expected = np.array((-3, -2, -1, 1, 2, 3))
    self.assertEqual(len(actual), len(expected))
    for i in range(len(actual)):
      self.assertEqual(actual[i], expected[i])


  def test_concat_array_001(self):
    import numpy as np
    levs1 = [-1, 2, 3]
    levs2 = [4, 5, -6]
    actual = concat_array(levs1, levs2)
    expected = np.array((-6, -1, 2, 3, 4, 5))
    self.assertEqual(len(actual), len(expected))
    for i in range(len(actual)):
      self.assertEqual(actual[i], expected[i])

  def test_concat_array_002(self):
    import numpy as np
    levs1 = [-1, 2, 3]
    levs2 = [4, 5, -6]
    actual = concat_array(levs1, levs2, sort=True)
    expected = np.array((-6, -1, 2, 3, 4, 5))
    self.assertEqual(len(actual), len(expected))
    for i in range(len(actual)):
      self.assertEqual(actual[i], expected[i])

  def test_concat_array_003(self):
    import numpy as np
    levs1 = [-1, 2, 3]
    levs2 = [4, 5, -6]
    actual = concat_array(levs1, levs2, sort=False)
    expected = np.array((-1, 2, 3, 4, 5, -6))
    self.assertEqual(len(actual), len(expected))
    for i in range(len(actual)):
      self.assertEqual(actual[i], expected[i])


  def test_myglob_001(self):
    import glob
    path = "./tests/data/util/myglob/*"
    actual = myglob(path)
    expected = list(("./tests/data/util/myglob/test1.txt", "./tests/data/util/myglob/test2.txt"))
    self.assertEqual(actual, expected)

  def test_myglob_002(self):
    import glob
    path = "./tests/data/util/myglob/*"
    actual = myglob(path, reverse=False)
    expected = list(("./tests/data/util/myglob/test1.txt", "./tests/data/util/myglob/test2.txt"))
    self.assertEqual(actual, expected)

  def test_myglob_003(self):
    import glob
    path = "./tests/data/util/myglob/*"
    actual = myglob(path, reverse=True)
    expected = list(("./tests/data/util/myglob/test2.txt", "./tests/data/util/myglob/test1.txt"))
    self.assertEqual(actual, expected)
  
  def test_check_tar_content_001(self):
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
