# Copyright 2021 nakamura_yuki
# 
# This program comes from Qiita article
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

    Notes
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


jma_rain_lat = np.linspace(48, 20, 3360, endpoint=False)[::-1] - 1/80/1.5 / 2
jma_rain_lon = np.linspace(118, 150, 2560, endpoint=False) + 1/80 / 2


def get_jrara_lat():
    r'''解析雨量の緯度を返す関数

    Returns
    -------
    lat: `numpy.ndarray`
    '''
    return np.linspace(48, 20, 3360, endpoint=False)[::-1] - 1/80/1.5 / 2
    

def get_jrara_lat():
    r'''解析雨量の経度を返す関数

    Returns
    -------
    lon: `numpy.ndarray`
    '''
    return np.linspace(118, 150, 2560, endpoint=False) + 1/80 / 2
