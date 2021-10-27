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

  Notes
  -----
  The same as util.load_jmara_grib2.
  '''
  from .util import load_jmara_grib2
  return load_jmara_grib2(file)

jma_rain_lat = jma_rain_lat
jma_rain_lon = jma_rain_lon


def get_jrara_lat():
  r'''解析雨量の緯度を返す関数

  Returns
  -------
  lat: `numpy.ndarray`

  Notes
  -----
  The same as util.load_jmara_grib2.
  '''
  from .util import get_jrara_lat
  return get_jrara_lat()

def get_jrara_lon():
  r'''解析雨量の経度を返す関数

  Returns
  -------
  lon: `numpy.ndarray`
  
  Notes
  -----
  The same as util.load_jmara_grib2.
  '''
  from .util import get_jrara_lon
  return get_jrara_lon()