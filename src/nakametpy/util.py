# Copyright (c) 2021, NakaMetPy Develoers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
# 
# Function load_jmara_grib2 is based on Qiita article
# URL: https://qiita.com/vpcf/items/b680f504cfe8b6a64222
#

import struct
import numpy as np
from itertools import repeat


def _set_table(section5):
  max_level = struct.unpack_from('>H', section5, 15)[0]
  table = (
    -10, # define representative of level 0　(Missing Value)
    *struct.unpack_from('>'+str(max_level)+'H', section5, 18)
  )
  return np.array(table, dtype=np.int16)

def _decode_runlength(code, hi_level):
  for raw in code:
    if raw <= hi_level:
      level = raw
      pwr = 0
      yield level
    else:
      length = (0xFF - hi_level)**pwr * (raw - (hi_level + 1))
      pwr += 1
      yield from repeat(level, length)

def load_jmara_grib2(file):
  r'''気象庁解析雨量やレーダー雨量を返す関数

  欠損値は負の値として表現される

  Parameters
  --------
  file: `str`
    file path 
    ファイルのPATH

  Returns
  -------
  rain: `numpy.ma.MaskedArray`
    単位 (mm)

  Note
  -----
  ``jma_rain_lat`` , ``jma_rain_lon`` はそれぞれ返り値に対応する
  `np.ndarray` 型の緯度経度である。
  '''
  with open(file, 'rb') as f:
    binary = f.read()
  
  len_ = {'sec0':16, 'sec1':21, 'sec3':72, 'sec4':82, 'sec6':6}
  
  end4 = len_['sec0'] + len_['sec1'] + len_['sec3'] + len_['sec4'] - 1
  len_['sec5'] = struct.unpack_from('>I', binary, end4+1)[0]
  section5 = binary[end4:(end4+len_['sec5']+1)]
  power = section5[17]
  # print(power)
  
  end6 = end4 + len_['sec5'] + len_['sec6']
  len_['sec7'] = struct.unpack_from('>I', binary, end6+1)[0]
  section7 = binary[end6:(end6+len_['sec7']+1)]
  
  highest_level = struct.unpack_from('>H', section5, 13)[0]
  level_table = _set_table(section5)
  decoded = np.fromiter(
    _decode_runlength(section7[6:], highest_level), dtype=np.int16
  ).reshape((3360, 2560))
  
  # convert level to representative
  return np.ma.masked_less((level_table[decoded]/(10**power))[::-1, :], 0)

def get_jmara_lat():
  r'''解析雨量の緯度を返す関数

  Returns
  -------
  lat: `numpy.ndarray`
  '''
  return np.linspace(48, 20, 3360, endpoint=False)[::-1] - 1/80/1.5 / 2
    

def get_jmara_lon():
  r'''解析雨量の経度を返す関数

  Returns
  -------
  lon: `numpy.ndarray`
  '''
  return np.linspace(118, 150, 2560, endpoint=False) + 1/80 / 2

def get_gsmap_lat():
  r'''GSMaPの緯度を返す関数

  Returns
  -------
  lat: `numpy.ndarray`
  '''
  return np.arange(-60, 60, 0.1)[::-1] + 0.05
    

def get_gsmap_lon():
  r'''GSMaPの経度を返す関数

  Returns
  -------
  lon: `numpy.ndarray`
  '''
  return np.arange(0, 360, 0.1) + 0.05


def dt_ymdhm(date, opt=1):
  r'''
  datetime.datetime から year, month, day, hour, minute の set を返す関数。
  opt = 1 : string, 0 : int

  Return the set of year, month, day, hour, minute from datetime.datetime.

  Parameters
  ----------
  date: `datetime.datetime`
    datetime
  opt: `int`
    return string or not
  
  Returns
  -------
  `set`
    (year, month, day, hour, minute)
  '''
  if opt == 0:
    return (date.year, date.month, date.day, date.hour, date.minute)
  elif opt == 1:
    return (f"{date.year}", f"{date.month:02}", f"{date.day:02}", f"{date.hour:02}", f"{date.minute:02}")


jma_rain_lat = np.linspace(48, 20, 3360, endpoint=False)[::-1] - 1/80/1.5 / 2
jma_rain_lon = np.linspace(118, 150, 2560, endpoint=False) + 1/80 / 2

gsmap_lat = np.arange(-60, 60, 0.1)[::-1] + 0.05
gsmap_lon = np.arange(0, 360, 0.1) + 0.05

def unit_ms1_knots(ms):
  r"""
  Convert unit m/s into knots.
  
  Parameters
  ----------
  ms: `int`
    Velocity in meter per second.
  
  Returns
  -------
  `kt`
    Velocity in knots.
  """
  return ms*3600/1852

def unit_knots_ms1(kt):
  r"""
  Convert unit knots into m/s.
  
  Parameters
  ----------
  kt: `int`
    Velocity in knots.
  
  Returns
  -------
  `ms`
    Velocity in meter per second.
  """
  return kt*1852/3600

def anom_levels(levs):
  """
  Return minus ans plus levels.

  Parameters
  ----------
  levs: `list`or`np.ndarray`

  Returns
  -------
  anom levels: `np.ndarray`
  
  Examples  
  --------
      >>> levs = [0.5, 1., 2.]
      >>> print(anom_levels(levs))
      [-2.  -1.  -0.5  0.5  1.   2. ]
  
  
  """
  levs = list(set(np.abs(levs)))
  levs.sort()
  return np.array([-i for i in levs[::-1]]+levs)