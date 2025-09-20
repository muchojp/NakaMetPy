# Copyright (c) 2025, NakaMetPy Develoers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

import struct
import os
import logging
import glob
from nakametpy.constants import convert_format_to_size, available_flag, current_weather_code

# Change HERE when developing from INFO into DEBUG
# It will be help you.
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
# logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
# logging.disable(logging.CRITICAL)

class synop1min:
  def __init__(self, file_path: str) -> None:
    r"""Read synop1min

    地上気象観測1分値データを読むクラス

    Parameters
    ----------
    file_path : `str`
      path to SYNOP 1min file.

      地上気象観測1分値データファイルのパス
    """
    self.file_path = file_path
    with open(self.file_path, 'rb') as f:
      self.binary = f.read()
    
    
  def get_data(self, idx: int) -> list:
    r"""get data

    Parameters
    ----------
    idx : `int`
      specify n-th data

    Returns
    -------
    list
      data
    """
    
    data = []
    self.body = self.binary[idx*255:(idx+1)*255]
    logging.debug(self.body)
    self.offset = 0
    logging.debug("==============================")
    logging.debug("=========== 地点情報 =========")
    logging.debug("==============================")
    chiten_info = []
    chiten_info.append(self._get_item("機関番号", "H", 0, 0, False))
    chiten_info.append(self._get_item("府県番号", "H", 0, 0, False))
    chiten_info.append(self._get_item("観測所番号", "I", 0, 0, False))
    chiten_info.append(self._get_item("観測所種別", "H", 0, 0, False))
    chiten_info.append(self._get_item("緯度", "I", 1, 0, False))
    chiten_info.append(self._get_item("経度", "I", 1, 0, False))
    chiten_info.append(self._get_item("標高", "H", 1, -20000, False))
    chiten_info.append(self._get_item("雨量計地上の高さ", "H", 1, 0, False))
    chiten_info.append(self._get_item("風向風速計の高さ", "H", 1, 0, False))
    chiten_info.append(self._get_item("温度計地上の高さ", "H", 1, 0, False))
    chiten_info.append(self._get_item("日照計地上の高さ", "H", 1, 0, False))
    chiten_info.append(self._get_item("全天日射計地上の高さ", "H", 1, 0, False))
    chiten_info.append(self._get_item("気圧計の高さ", "H", 1, -20000, False))
    chiten_info.append(self._get_item("視程計地上の高さ", "H", 1, 0, False))
    self.offset += 6
    chiten_info.append(self._get_item("年", "H", 0, 0, False))
    chiten_info.append(self._get_item("月", "H", 0, 0, False))
    chiten_info.append(self._get_item("日", "H", 0, 0, False))
    chiten_info.append(self._get_item("時", "H", 0, 0, False))
    chiten_info.append(self._get_item("分", "H", 0, 0, False))
    logging.debug(f"地点情報：{chiten_info}")
    data.append(chiten_info)
    
    logging.debug("==============================")
    logging.debug("============= 雨 =============")
    logging.debug("==============================")
    rain_info = []
    self.offset += 1
    rain_info.append(self._get_item("降水積算カウンタ", "I", 0, 0, False))
    rain_info.append(self._get_item("前1分間降水量", "I", 1, 0, False))
    rain_info.append(available_flag[self._get_item("利用フラグ", "B", 0, 0, False)].split("/")[0])
    self.offset += 1
    rain_info.append(self._get_item("降水強度", "I", 1, 0, False))
    rain_info.append(available_flag[self._get_item("利用フラグ", "B", 0, 0, False)].split("/")[0])
    self.offset += 1
    rain_info.append(self._get_item("最大降水強度", "I", 1, 0, False))
    rain_info.append(available_flag[self._get_item("利用フラグ", "B", 0, 0, False)].split("/")[0])
    self.offset += 1
    rain_info.append(self._get_item("降水の有無", "I", 1, 0, False))
    rain_info.append(available_flag[self._get_item("利用フラグ", "B", 0, 0, False)].split("/")[0])
    self.offset += 1
    rain_info.append(self._get_item("降水種別", "I", 1, 0, False))
    rain_info.append(available_flag[self._get_item("利用フラグ", "B", 0, 0, False)].split("/")[0])
    self.offset += 1
    logging.debug(f"雨：{rain_info}")
    data.append(rain_info)
    
    logging.debug("==============================")
    logging.debug("============= 風 =============")
    logging.debug("==============================")
    wind_info = []
    self.offset += 1
    wind_info.append(self._get_item("CW風向の最大値", "I", 0, 0, False))
    wind_info.append(available_flag[self._get_item("利用フラグ", "B", 0, 0, False)].split("/")[0])
    self.offset += 1
    wind_info.append(self._get_item("CCW風向の最大値", "I", 0, 0, False))
    wind_info.append(available_flag[self._get_item("利用フラグ", "B", 0, 0, False)].split("/")[0])
    self.offset += 1
    wind_info.append(self._get_item("最大瞬間風速（3秒移動平均）", "I", 1, 0, False))
    wind_info.append(available_flag[self._get_item("利用フラグ", "B", 0, 0, False)].split("/")[0])
    self.offset += 1
    wind_info.append(self._get_item("最大瞬間風速（3秒移動平均）時の風向（16方位）", "I", 0, 0, False))
    wind_info.append(self._get_item("最大瞬間風速（3秒移動平均）時の風向（36方位）", "I", 0, 0, False))
    wind_info.append(self._get_item("最小瞬間風速（3秒移動平均）", "I", 1, 0, False))
    wind_info.append(available_flag[self._get_item("利用フラグ", "B", 0, 0, False)].split("/")[0])
    self.offset += 1
    wind_info.append(self._get_item("平均風向（前10分間のベクトル平均）（16方位）", "I", 0, 0, False))
    wind_info.append(available_flag[self._get_item("利用フラグ", "B", 0, 0, False)].split("/")[0])
    self.offset += 1
    wind_info.append(self._get_item("平均風向（前10分間のベクトル平均）（36方位）", "I", 0, 0, False))
    wind_info.append(available_flag[self._get_item("利用フラグ", "B", 0, 0, False)].split("/")[0])
    self.offset += 1
    wind_info.append(self._get_item("風程", "I", 0, 0, False))
    wind_info.append(available_flag[self._get_item("利用フラグ", "B", 0, 0, False)].split("/")[0])
    self.offset += 1
    wind_info.append(self._get_item("風程有効データ数", "I", 0, 0, False))
    wind_info.append(self._get_item("平均風速（10分移動平均）", "I", 1, 0, False))
    wind_info.append(available_flag[self._get_item("利用フラグ", "B", 0, 0, False)].split("/")[0])
    self.offset += 1
    logging.debug(f"風：{wind_info}")
    data.append(wind_info)
    
    logging.debug("==============================")
    logging.debug("============ 気温 ============")
    logging.debug("==============================")
    temperature_info = []
    self.offset += 1
    temperature_info.append(self._get_item("瞬間気温（1分移動平均）", "I", 1, 0, False))
    temperature_info.append(available_flag[self._get_item("利用フラグ", "B", 0, 0, False)].split("/")[0])
    self.offset += 1
    temperature_info.append(self._get_item("最高気温（１分移動平均）", "I", 1, 0, False))
    temperature_info.append(available_flag[self._get_item("利用フラグ", "B", 0, 0, False)].split("/")[0])
    self.offset += 1
    temperature_info.append(self._get_item("最低気温（１分移動平均）", "I", 1, 0, False))
    temperature_info.append(available_flag[self._get_item("利用フラグ", "B", 0, 0, False)].split("/")[0])
    self.offset += 1
    logging.debug(f"気温：{temperature_info}")
    data.append(temperature_info)
    
    logging.debug("==============================")
    logging.debug("============ 日照 ============")
    logging.debug("==============================")
    sunshine_info = []
    self.offset += 1
    sunshine_info.append(self._get_item("日照積算カウンタ", "I", 0, 0, False))
    sunshine_info.append(self._get_item("日照時間", "I", 0, 0, False))
    sunshine_info.append(available_flag[self._get_item("利用フラグ", "B", 0, 0, False)].split("/")[0])
    self.offset += 1
    logging.debug(f"日照：{sunshine_info}")
    data.append(sunshine_info)
    
    logging.debug("==============================")
    logging.debug("============ 予備 ============")
    logging.debug("==============================")
    self.offset += 13
    
    logging.debug("==============================")
    logging.debug("============ 積雪 ============")
    logging.debug("==============================")
    snow_info = []
    self.offset += 1
    snow_info.append(self._get_item("積雪深", "I", 0, 0, False))
    snow_info.append(available_flag[self._get_item("利用フラグ", "B", 0, 0, False)].split("/")[0])
    self.offset += 1
    logging.debug(f"積雪：{snow_info}")
    data.append(snow_info)
    
    logging.debug("==============================")
    logging.debug("============ 気圧 ============")
    logging.debug("==============================")
    pressure_info = []
    self.offset += 1
    pressure_info.append(self._get_item("重力加速度", "H", 4, 90000, False))
    pressure_info.append(self._get_item("現地気圧（１分移動平均）", "I", 1, 0, False))
    pressure_info.append(available_flag[self._get_item("利用フラグ", "B", 0, 0, False)].split("/")[0])
    self.offset += 1
    pressure_info.append(self._get_item("海面気圧", "I", 1, 0, False))
    pressure_info.append(available_flag[self._get_item("利用フラグ", "B", 0, 0, False)].split("/")[0])
    self.offset += 1
    pressure_info.append(self._get_item("最低海面気圧", "I", 1, 0, False))
    pressure_info.append(available_flag[self._get_item("利用フラグ", "B", 0, 0, False)].split("/")[0])
    self.offset += 1
    logging.debug(f"気圧：{pressure_info}")
    data.append(pressure_info)
    
    logging.debug("==============================")
    logging.debug("============ 湿度 ============")
    logging.debug("==============================")
    humidity_info = []
    self.offset += 1
    humidity_info.append(self._get_item("瞬間湿度（１分移動平均）", "I", 0, 0, False))
    humidity_info.append(available_flag[self._get_item("利用フラグ", "B", 0, 0, False)].split("/")[0])
    self.offset += 1
    humidity_info.append(self._get_item("最低湿度", "I", 0, 0, False))
    humidity_info.append(available_flag[self._get_item("利用フラグ", "B", 0, 0, False)].split("/")[0])
    self.offset += 1
    humidity_info.append(self._get_item("瞬間蒸気圧", "I", 1, 0, False))
    humidity_info.append(available_flag[self._get_item("利用フラグ", "B", 0, 0, False)].split("/")[0])
    self.offset += 1
    humidity_info.append(self._get_item("露点温度", "I", 1, 0, False))
    humidity_info.append(available_flag[self._get_item("利用フラグ", "B", 0, 0, False)].split("/")[0])
    self.offset += 1
    logging.debug(f"湿度：{humidity_info}")
    data.append(humidity_info)
    
    logging.debug("==============================")
    logging.debug("============ 視程 ============")
    logging.debug("==============================")
    weather_info = []
    self.offset += 1
    weather_info.append(self._get_item("視程（10分平均）", "I", 3, 0, False))
    weather_info.append(available_flag[self._get_item("利用フラグ", "B", 0, 0, False)].split("/")[0])
    self.offset += 1
    weather_info.append(current_weather_code[self._get_item("現在天気", "I", 0, 0, False)])
    weather_info.append(available_flag[self._get_item("利用フラグ", "B", 0, 0, False)].split("/")[0])
    self.offset += 1
    logging.debug(f"視程：{weather_info}")
    data.append(weather_info)
    logging.debug(f"offset：{self.offset}")
    return data
  
  def _get_item(self, item_name: str, fmt: str, calibration: int, ioffset: int, debug: bool):
    item = struct.unpack_from(f'<{fmt}', self.body, self.offset)[0]
    if calibration != 0:
      item = (item + ioffset) / 10**calibration
    elif ioffset != 0:
      item += ioffset
    self.offset += convert_format_to_size[fmt]
    if debug:
      logging.debug(f"{item_name}：{item}")
    return item

if __name__=='__main__':
  filelist = glob.glob("../../../tests/data/product/synop1min/20241030000000/*")
  for ifile in filelist:
    synop1min_class = synop1min(os.path.join(os.path.dirname(__file__), ifile))
    print(synop1min_class.get_data(0))
  # synop1min_class = synop1min(os.path.join(os.path.dirname(__file__), "../../../tests/data/product/synop1min/20241030000000/Z__C_JMBS_20241030000000_OBS_SURF_Rjp_Opermin_jmasf_401.bin"))
  # print(synop1min_class.get_data(0))