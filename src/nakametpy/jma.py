# Copyright 2021 nakamura_yuki
# 
from .util import jma_rain_lat, jma_rain_lon

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
  The same as util.load_jmara_grib2.
  '''
  from .util import load_jmara_grib2 as _func
  return _func(file)

jma_rain_lat = jma_rain_lat
jma_rain_lon = jma_rain_lon


def get_jmara_lat():
  r'''解析雨量の緯度を返す関数

  Returns
  -------
  lat: `numpy.ndarray`

  Note
  -----
  The same as util.get_jmara_lat.
  '''
  from .util import get_jmara_lat as _func
  return _func()

def get_jmara_lon():
  r'''解析雨量の経度を返す関数

  Returns
  -------
  lon: `numpy.ndarray`
  
  Note
  -----
  The same as util.get_jmara_lon.
  '''
  from .util import get_jmara_lon as _func
  return _func()