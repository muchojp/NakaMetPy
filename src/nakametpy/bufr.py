# Copyright (c) 2024, NakaMetPy Develoers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

import numpy as np
import pandas as pd
from nakametpy.constants import LATEST_MASTER_TABLE_VERSION, OLDEST_MASTER_TABLE_VERSION
from nakametpy.tables import bufrtab_TableA
from nakametpy._error import NotSupportedNewerVersionMSWarning, NotSupportedOlderVersionMSWarning,\
                    NotSupportedBufrError, UnexpectedBufrError
import os
import re
import logging
import warnings

# Change HERE when developing from INFO into DEBUG
# It will be help you.
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
# logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
# logging.disable(logging.CRITICAL)

def parse_bufrtab(file_path: str) -> list:
  with open(file_path, mode="r", encoding="utf-8") as f:
    raw_text = f.readlines()
  # 特定の文字列から始まる行を除く
  _records = list(filter(lambda x: not x.startswith("Table"), raw_text))
  _records = list(filter(lambda x: not x.startswith("#"), _records))
  _records = list(filter(lambda x: not x.startswith("END"), _records))
  # 改行文字削除
  _records = [_record.strip("\n") for _record in _records]
  _records = [_record.strip() for _record in _records]
  # 改行文字のみ
  valid_records = list(filter(lambda x: x != "", _records))
  return valid_records

def parse_tableB_into_dataframe(version: str=f"STD_0_{LATEST_MASTER_TABLE_VERSION:02}") -> pd.DataFrame:
  columns = ["F-XX-YYY", "SCALE", "REFERENCE_VALUE", "BIT_WIDTH", "UNIT", "MNEMONIC", "DESC_CODE", "ELEMENT_NAME"]
  
  bufrtab = os.path.join(os.path.dirname(__file__), f"./tables/bufrtab.TableB_{version:02}")
  valid_records = parse_bufrtab(bufrtab)
  # print(valid_records[-1])
  df = pd.DataFrame([re.split("[|;]", irecord.strip()) for irecord in valid_records])
  # 不要な文字を削除を削除
  df = df.apply(lambda x: x.str.strip())
  # ELEMENT_NAMEに;が含まれるカラムNoneのみの列を削除
  if (len(columns) + 1) == len(df.columns.values):
    # 最後の列のインデックスを取得
    last_col = df.columns[-1]
    df.loc[df[last_col].notnull(), df.columns[-2]] += ("; " + df[last_col])
    # df[df.iloc[:, -1] is not None].iloc[:, -2] = df.iloc[:, :-2]+"; "+df.iloc[:, :-1]
    df = df.iloc[:, :-1]
  df.columns = columns
  return df

def parse_tableD_into_dict(version: str=f"STD_0_{LATEST_MASTER_TABLE_VERSION:02}") -> list:
  bufrtab = os.path.join(os.path.dirname(__file__), f"./tables/bufrtab.TableD_{version:02}")
  valid_records = parse_bufrtab(bufrtab)
  data = dict()
  fxxyyy = r"^\d-\d{2}-\d{3}" # F-XX-YYY
  fxxyyy_notlast = r"^\d-\d{2}-\d{3} >" # F-XX-YYY >
  for irecord in valid_records:
    irec_list = [x.strip() for x in re.split("[|;]", irecord.strip())]
    # 1レコードで比較
    if re.match(fxxyyy, irecord):
      ielm_list = []
      iseq_list = irec_list
    else:
      jelm_list = irec_list
      # 2列目のF-XX-YYYで比較
      if re.match(fxxyyy_notlast, jelm_list[1]):
        # " >"を削除
        jelm_list[1] = jelm_list[1][:-2]
        ielm_list.append(dict(FXXYYY=jelm_list[1], NAME=jelm_list[2]))
      else:
        ielm_list.append(dict(FXXYYY=jelm_list[1], NAME=jelm_list[2]))
        data[iseq_list[0]] = dict(MNEMONIC=iseq_list[1], DCOD=iseq_list[2], NAME=iseq_list[3], SEQUENCE=ielm_list)
  return data

def parse_codeFlag_into_dict(version: str=f"STD_0_{LATEST_MASTER_TABLE_VERSION:02}") -> list:
  bufrtab = os.path.join(os.path.dirname(__file__), f"./tables/bufrtab.CodeFlag_{version:02}")
  valid_records = parse_bufrtab(bufrtab)
  data = dict()
  fxxyyy = r"^\d-\d{2}-\d{3}" # F-XX-YYY
  valBit_notlast = r"^\d+ >" # \d+ >
  for irecord in valid_records:
    irec_list = [x.strip() for x in re.split("[|;]", irecord.strip())]
    # 1レコードで比較
    if re.match(fxxyyy, irecord):
      ielm_dict = dict()
      dependency = None
      # F-XX-YYY, MNEMONIC, CODEFLAG
      # EXAMPLE: 0-01-003 | WMOR ; CODE
      iseq_list = irec_list
    else:
      jelm_list = irec_list
      # 2列目にDependencyがあるかを確認
      if "=" in jelm_list[1]:
        # "f-x1-yy1,f-x2-yy2=1,22,33"
        dependency = jelm_list[1]
      else:
        #   | 0 > | Antarctica
        if re.match(valBit_notlast, jelm_list[1]):
          # " >"を削除
          jelm_list[1] = jelm_list[1][:-2]
        if dependency is None:
          ielm_dict[jelm_list[1]] = jelm_list[2]
        else:
          # print(type(dependency), dependency, jelm_list)
          dependencies  = dependency.split("=")
          _fxxyyy_list = dependencies[0].split(",")
          # print(ielm_dict, type(ielm_dict), _fxxyyy_list[0], dependencies[1])
          # EXAMPLE: (f-x1-yy1, f-x2-yy2)
          for _fxxyyy in _fxxyyy_list:
            if _fxxyyy not in ielm_dict.keys():
              ielm_dict[_fxxyyy] = dict()
            # EXAMPLE: "1,22,33"
            for _idependency in dependencies[1].split(","):
              if _idependency not in ielm_dict[_fxxyyy].keys():
                ielm_dict[_fxxyyy][_idependency] = dict()
              # 0-01-034 | GSES ; CODE
              # ielm_dict["0-01-031"]["34"]["240"] = "Kiyose"
              ielm_dict[_fxxyyy][_idependency][jelm_list[1]] = jelm_list[2]
        if not re.match(valBit_notlast, jelm_list[1]):
          if dependency is None:
            data[iseq_list[0]] = dict(MNEMONIC=iseq_list[1], CODEFLAG=iseq_list[2], HAS_DEPENDENCY=False, VALBITS=ielm_dict)
          else:
            # print(dependency, ielm_dict)
            data[iseq_list[0]] = dict(MNEMONIC=iseq_list[1], CODEFLAG=iseq_list[2], HAS_DEPENDENCY=True, DEPENDENCY=dependency, VALBITS=ielm_dict)
  # print(data["0-01-034"])
  return data

class bufr:
  def __init__(self, file_path) -> None:
    self.file_path = file_path
    
    with open(self.file_path, 'rb') as f:
      self.binary = f.read()
    
    self.sec_len = {'sec0':8, 'sec1':22, 'sec5':4}
    
    self.sec_head = bufr_sec_head(self.binary, self.sec_len)
    self.sec_0 = bufr_sec_0(self.binary, self.sec_len)
    self.sec_1 = bufr_sec_1(self.binary, self.sec_len)
    if self.sec_1.sec1_10_optional_section_flag == False:
      self.sec_len['sec2'] = 0
    else:
      raise NotSupportedBufrError(file_path, f"第2節の長さが0ではない")
    self.sec_3 = bufr_sec_3(self.binary, self.sec_len, self.sec_1.sec1_use_master_table_version)
    self.sec_4 = bufr_sec_4(self.binary, self.sec_len, self.sec_1.sec1_use_master_table_version)
    self.sec_5 = bufr_sec_5(self.binary, self.sec_len)
    
  def get_data_description(self) -> list:
    return self.sec_3.sec3_data_desc_str_list
    
  def get_data_descriptors(self) -> list:
    return self.sec_3.sec3_data_desc_list
  
  def read_data(self) -> list:
    descriptors = self.get_data_descriptors()
    return self.sec_4.read_data(descriptors, self.sec_len)

class bufr_sec_head:
  def __init__(self, binary, sec_len) -> None:
    header = binary[0:12+1+8+1+6+1+3+4+1].decode()
    header_list = binary[0:12+1+8+1+6+1+3+4+1].decode().split(" ")
    # 指示コードなし
    if header_list[2][6:10] == "BUFR":
      sec_len['sec_head'] = len(header_list[0]) + 1 + len(header_list[1]) + 1 + 6
    # 指示コードあり
    else:
      sec_len['sec_head'] = len(header_list[0]) + 1 + len(header_list[1]) + 1 + 6 + 1 + 3
    logging.debug(f"sec0_start = {sec_len['sec_head']}")
    self.tlg_header = header[:sec_len['sec_head']]
    logging.debug(f"電文ヘッダ = {self.tlg_header}")

class bufr_sec_0:
  def __init__(self, binary, sec_len) -> None:
    # Section 0, Indicator section
    self.sec0_binary = binary[sec_len['sec_head']:sec_len['sec_head']+sec_len['sec0']]
    self.sec0_desc_en = "Section 0, Indicator section"
    self.sec0_desc_jp = "第0節(指示節)"
    self.sec0_01_04_bufr_str = self.sec0_binary[:4].decode()
    self.sec0_05_07_bufr_len = int.from_bytes(self.sec0_binary[4:7], "big")
    self.sec0_08_bufr_version = int.from_bytes(self.sec0_binary[7:], "big")
    logging.debug(f"{self.sec0_desc_jp} 1~4 32 国際アルファベットNo5による記述でBUFR = {self.sec0_01_04_bufr_str}")
    logging.debug(f"{self.sec0_desc_jp} 5~7 24 BUFR報全体の長さ = {self.sec0_05_07_bufr_len}")
    logging.debug(f"{self.sec0_desc_jp} 8   8  BUFR報の版番号 = {self.sec0_08_bufr_version}")

class bufr_sec_1:
  def __init__(self, binary, sec_len) -> None:
    # Section 1, Identification section
    self.sec1_desc_en = "Section 1, Identification section"
    self.sec1_desc_jp = "第1節(識別節)"
    self.latest_table_c = parse_codeFlag_into_dict()
    
    self.sec1_start = sec_len['sec_head'] + sec_len['sec0']
    sec_len['sec1'] = int.from_bytes(binary[self.sec1_start:self.sec1_start+3], "big")
    self.sec1_binary = binary[self.sec1_start:self.sec1_start+sec_len['sec1']]
    if sec_len['sec1'] != 22:
      raise NotSupportedBufrError(super(self.file_path), f"第1節の長さが22でない")
    self.sec1_04_master_table_version = int.from_bytes(self.sec1_binary[3:3+1], "big")
    self.sec1_05_06_create_station_code = int.from_bytes(self.sec1_binary[4:4+2], "big")
    self.sec1_05_06_create_station_name = self.latest_table_c["0-01-035"]["VALBITS"][f"{self.sec1_05_06_create_station_code}"]
    self.sec1_07_08_create_sub_station_code = int.from_bytes(self.sec1_binary[6:6+2], "big")
    self.sec1_09_created_sequence_number = int.from_bytes(self.sec1_binary[8:8+1], "big")
    self.sec1_10_optional_section_bit = format(int.from_bytes(self.sec1_binary[9:9+1], "big"), "08b")
    self.sec1_10_optional_section_flag = bool(int(format(int.from_bytes(self.sec1_binary[9:9+1], "big"), "08b")[0]))
    self.sec1_11_type_of_data_code = int.from_bytes(self.sec1_binary[10:10+1], "big")
    self.sec1_11_type_of_data = bufrtab_TableA.data_types[self.sec1_11_type_of_data_code]
    self.sec1_12_global_data_subcategory_code = int.from_bytes(self.sec1_binary[11:11+1], "big")
    self.sec1_12_global_data_subcategory = bufrtab_TableA.standard_subtypes[self.sec1_11_type_of_data_code][self.sec1_12_global_data_subcategory_code]
    self.sec1_13_local_data_subcategory_code = int.from_bytes(self.sec1_binary[12:12+1], "big")
    if self.sec1_13_local_data_subcategory_code in bufrtab_TableA.local_subtypes[self.sec1_11_type_of_data_code].keys():
      self.sec1_13_local_data_subcategory = bufrtab_TableA.local_subtypes[self.sec1_11_type_of_data_code][self.sec1_13_local_data_subcategory_code]
    elif self.sec1_13_local_data_subcategory_code == 0:
      self.sec1_13_local_data_subcategory = "defined in center station"
    else:
      self.sec1_13_local_data_subcategory = "not specified"
    self.sec1_14_master_table_version = int.from_bytes(self.sec1_binary[13:13+1], "big")
    if (self.sec1_14_master_table_version < OLDEST_MASTER_TABLE_VERSION):
      warnings.warn(NotSupportedOlderVersionMSWarning(self.sec1_14_master_table_version))
      self.sec1_use_master_table_version = OLDEST_MASTER_TABLE_VERSION
    elif (LATEST_MASTER_TABLE_VERSION < self.sec1_14_master_table_version):
      warnings.warn(NotSupportedNewerVersionMSWarning(self.sec1_14_master_table_version))
      self.sec1_use_master_table_version = LATEST_MASTER_TABLE_VERSION
    else:
      self.sec1_use_master_table_version = self.sec1_14_master_table_version
    self.sec1_15_local_table_version = int.from_bytes(self.sec1_binary[14:14+1], "big")
    self.sec1_16_17_data_created_year = int.from_bytes(self.sec1_binary[15:15+2], "big")
    self.sec1_18_data_created_month = int.from_bytes(self.sec1_binary[17:17+1], "big")
    self.sec1_19_data_created_day = int.from_bytes(self.sec1_binary[18:18+1], "big")
    self.sec1_20_data_created_hour = int.from_bytes(self.sec1_binary[19:19+1], "big")
    self.sec1_21_data_created_minute = int.from_bytes(self.sec1_binary[20:20+1], "big")
    self.sec1_22_data_created_second = int.from_bytes(self.sec1_binary[21:21+1], "big")
    
    logging.debug(f"{self.sec1_desc_jp} 1 ~ 3 24 第1節の長さ = {sec_len['sec1']}")
    logging.debug(f"{self.sec1_desc_jp} 4     8  BUFRマスター表 = {self.sec1_04_master_table_version}")
    logging.debug(f"{self.sec1_desc_jp} 5 ~ 6 16 作成中枢の識別 = {self.sec1_05_06_create_station_code} {self.sec1_05_06_create_station_name}")
    logging.debug(f"{self.sec1_desc_jp} 7 ~ 8 16 作成副中枢の識別 = {self.sec1_07_08_create_sub_station_code}")
    logging.debug(f"{self.sec1_desc_jp} 9     8  更新一連番号 = {self.sec1_09_created_sequence_number}")
    logging.debug(f"{self.sec1_desc_jp} 10    8  任意節の有無 = {self.sec1_10_optional_section_flag}")
    logging.debug(f"{self.sec1_desc_jp} 11    8  資料の種類 = {self.sec1_11_type_of_data_code} {self.sec1_11_type_of_data}")
    logging.debug(f"{self.sec1_desc_jp} 12    8  国際的な資料サブカテゴリ = {self.sec1_12_global_data_subcategory_code} {self.sec1_12_global_data_subcategory}")
    logging.debug(f"{self.sec1_desc_jp} 13    8  地域的な資料サブカテゴリ = {self.sec1_13_local_data_subcategory_code} {self.sec1_13_local_data_subcategory}")
    logging.debug(f"{self.sec1_desc_jp} 14    8  マスターテーブルのバージョン番号 = {self.sec1_14_master_table_version}")
    logging.debug(f"{self.sec1_desc_jp} 15    8  マスターテーブルに加えて使用したローカルテーブルのバージョン番号 = {self.sec1_15_local_table_version}")
    logging.debug(f"{self.sec1_desc_jp} 16~17 16 年(電文作成年月日時分秒) = {self.sec1_16_17_data_created_year}")
    logging.debug(f"{self.sec1_desc_jp} 18    8  月(電文作成年月日時分秒) = {self.sec1_18_data_created_month}")
    logging.debug(f"{self.sec1_desc_jp} 19    8  日(電文作成年月日時分秒) = {self.sec1_19_data_created_day}")
    logging.debug(f"{self.sec1_desc_jp} 20    8  時(電文作成年月日時分秒) = {self.sec1_20_data_created_hour}")
    logging.debug(f"{self.sec1_desc_jp} 21    8  分(電文作成年月日時分秒) = {self.sec1_21_data_created_minute}")
    logging.debug(f"{self.sec1_desc_jp} 22    8  秒(電文作成年月日時分秒) = {self.sec1_22_data_created_second}")

class bufr_sec_3:
  def __init__(self, binary, sec_len, mst_tbl_version) -> None:
    # Section 1, Identification section
    self.sec3_desc_en = "Section 3, Data description section"
    self.sec3_desc_jp = "第3節(資料記述節)"
    self.std_df_b = parse_tableB_into_dataframe(f"STD_0_{mst_tbl_version}")
    self.std_table_c = parse_codeFlag_into_dict(f"STD_0_{mst_tbl_version}")
    # self.std_table_d = parse_tableD_into_dict(f"STD_0_{mst_tbl_version}")
    self.loc_df_b_1 = parse_tableB_into_dataframe("LOC_0_7_1")
    self.loc_df_b_2 = parse_tableB_into_dataframe("ADD_1_0")
    
    self.sec3_start = 0
    for ikey in ('sec_head', 'sec0', 'sec1', 'sec2'):
      self.sec3_start += sec_len[ikey]
    sec_len['sec3'] = int.from_bytes(binary[self.sec3_start:self.sec3_start+3], "big")
    self.sec3_binary = binary[self.sec3_start:self.sec3_start+sec_len['sec3']]
    self.sec3_04_unused = int.from_bytes(self.sec3_binary[3:3+1], "big")
    self.sec3_05_06_num_of_data_subset = int.from_bytes(self.sec3_binary[4:4+2], "big")
    self.sec3_07_data_format_bit = format(int.from_bytes(self.sec3_binary[6:6+1], "big"), "08b")
    self.sec3_07_data_format = ""
    self.sec3_07_data_format += "観測でない&" if self.sec3_07_data_format_bit[0] == "0" else "観測&"
    self.sec3_07_data_format += "圧縮でない" if self.sec3_07_data_format_bit[1] == "0" else "圧縮"
    
    # 8オクテット目以降
    std_flag = True
    data_desc_list = []
    data_desc_str_list = []
    for _i in range(8, sec_len["sec3"]+1, 2):
      # 標準のBテーブルでマッチした場合
      _fxxyyy = _int_into_fxxyyy(int.from_bytes(self.sec3_binary[_i-1:_i+1], "big"))
      if std_flag:
        if len(self.std_df_b[self.std_df_b["F-XX-YYY"] == _fxxyyy]["ELEMENT_NAME"].values) == 1:
          logging.debug(f"{self.sec3_desc_jp} {_i} ~ {_i+1}  16 {self.std_df_b[self.std_df_b["F-XX-YYY"] == _fxxyyy]["ELEMENT_NAME"].values[0]} = {_fxxyyy}")
          data_desc_list.append([_fxxyyy, self.std_df_b[self.std_df_b["F-XX-YYY"] == _fxxyyy].values[0]])
          data_desc_str_list.append(self.std_df_b[self.std_df_b["F-XX-YYY"] == _fxxyyy].to_string(header=None, index=None))
        elif (_fxxyyy[:1] == "1") & (_fxxyyy[-3:] == "000"):
          logging.debug(f"{self.sec3_desc_jp} {_i} ~ {_i+1}  16 Delayed replication of {int(_fxxyyy[2:4])} descriptor = {_fxxyyy}")
          data_desc_list.append([_fxxyyy, f"Delayed replication of {int(_fxxyyy[2:4])} descriptor"])
          data_desc_str_list.append(f" {_fxxyyy}  0  0  0  NONE  NONE   Delayed replication of {int(_fxxyyy[2:4])} descriptor")
        elif _fxxyyy.startswith("2-06-"):
          logging.debug(f"{self.sec3_desc_jp} {_i} ~ {_i+1}  16 Local descriptor = {_fxxyyy}")
          std_flag = False
          data_desc_list.append([_fxxyyy, f"Local descriptor"])
          data_desc_str_list.append(f" {_fxxyyy}  0  0  0  NONE  NONE   Local descriptor")
        else:
          logging.debug(f"{self.sec3_desc_jp} {_i} ~ {_i+1}  16 {self.std_df_b[self.std_df_b["F-XX-YYY"] == _fxxyyy]["ELEMENT_NAME"].values} = {_fxxyyy}")
          data_desc_list.append([_fxxyyy, f"NO INFOMATION VARIABLE"])
          data_desc_str_list.append(f" {_fxxyyy}  0  0  0  NONE  NONE   NO INFOMATION VARIABLE")
      else:
        if len(self.loc_df_b_1[self.loc_df_b_1["F-XX-YYY"] == _fxxyyy]["ELEMENT_NAME"].values) == 1:
          logging.debug(f"{self.sec3_desc_jp} {_i} ~ {_i+1}  16 {self.loc_df_b_1[self.loc_df_b_1["F-XX-YYY"] == _fxxyyy]["ELEMENT_NAME"].values[0]} = {_fxxyyy}")
          data_desc_list.append([_fxxyyy, self.loc_df_b_1[self.loc_df_b_1["F-XX-YYY"] == _fxxyyy].values[0]])
          data_desc_str_list.append(self.loc_df_b_1[self.loc_df_b_1["F-XX-YYY"] == _fxxyyy].to_string(header=None, index=None))
        elif len(self.loc_df_b_2[self.loc_df_b_2["F-XX-YYY"] == _fxxyyy]["ELEMENT_NAME"].values) == 1:
          logging.debug(f"{self.sec3_desc_jp} {_i} ~ {_i+1}  16 {self.loc_df_b_2[self.loc_df_b_2["F-XX-YYY"] == _fxxyyy]["ELEMENT_NAME"].values[0]} = {_fxxyyy}")
          data_desc_list.append([_fxxyyy, self.loc_df_b_2[self.loc_df_b_2["F-XX-YYY"] == _fxxyyy].values[0]])
          data_desc_str_list.append(self.loc_df_b_2[self.loc_df_b_2["F-XX-YYY"] == _fxxyyy].to_string(header=None, index=None))
        else:
          logging.debug(f"{self.sec3_desc_jp} {_i} ~ {_i+1}  16 {self.std_df_b[self.std_df_b["F-XX-YYY"] == _fxxyyy]["ELEMENT_NAME"].values} = {_fxxyyy}")
          data_desc_list.append([_fxxyyy, f"NO INFOMATION VARIABLE"])
          data_desc_str_list.append(f" {_fxxyyy}  0  0  0  NONE  NONE   NO INFOMATION VARIABLE",)
        std_flag = True

    self.sec3_data_desc_list = data_desc_list
    self.sec3_data_desc_str_list = data_desc_str_list


class bufr_sec_4:
  def __init__(self, binary, sec_len, mst_tbl_version) -> None:
    # Section 4, Data section
    self.sec4_desc_en = "Section 4, Data section"
    self.sec4_desc_jp = "第4節(資料節)"
    
    self.sec4_start = 0
    for ikey in ('sec_head', 'sec0', 'sec1', 'sec2', 'sec3'):
      self.sec4_start += sec_len[ikey]
    sec_len['sec4'] = int.from_bytes(binary[self.sec4_start:self.sec4_start+3], "big")
    self.sec4_binary = binary[self.sec4_start:self.sec4_start+sec_len['sec4']]
    self.sec4_04_unused = int.from_bytes(self.sec4_binary[3:3+1], "big")
    logging.debug(f"{self.sec4_desc_jp} 1  ~ 3   24 第4節の長さ(オクテット単位) = {sec_len['sec4']}")
    
  def read_data(self, descriptors, sec_len):
    nrep = 0
    for idescriptor in descriptors:
      if type(idescriptor[1]) == str:
        if idescriptor[1].startswith("Delayed replication of"):
          nrep += 1
    raw_data = format(int.from_bytes(self.sec4_binary, "big"), f"0{sec_len['sec4']*8}b")
    start_rec = 32
    self.data_class = data_constructor(descriptors, raw_data, start_rec)
    return self.data_class.get_data()


class bufr_sec_5:
  def __init__(self, binary, sec_len) -> None:
    # Section 5, End section
    self.sec5_desc_en = "Section 5, Data section"
    self.sec5_desc_jp = "第5節(終端節)"
    
    self.sec5_start = 0
    for ikey in ('sec_head', 'sec0', 'sec1', 'sec2', 'sec3', 'sec4'):
      self.sec5_start += sec_len[ikey]
    self.sec5_binary = binary[self.sec5_start:self.sec5_start+sec_len['sec5']]
    if self.sec5_binary.decode() == "7777":
      logging.debug(f"{self.sec5_desc_jp} 1  ~ 4   32 BUFR報の終わりを指す = {self.sec5_binary.decode()}")
      logging.debug(f"BUFRの終端に到達しました。正常に読込が終了しました。")
    else:
      raise UnexpectedBufrError(f"BUFRの終端に到達しませんでした。ファイルが正常であるか確認してください。")


class data_constructor:
  def __init__(self, descriptors, raw_data, start_rec) -> None:
    self.descriptors = descriptors
    self.raw_data = raw_data
    self.irec = start_rec
    self.desc_idx = 0
    self.local_flag = False
    
    self._descriptor_converter()
    self.data = self._read_data_from_str_bin()
    
  def _descriptor_converter(self):
    _nlen = len(self.descriptors)
    _nests = np.zeros(len(self.descriptors), dtype=np.int8)
    for idx, idescriptor in enumerate(self.descriptors[::-1]):
      if type(idescriptor[1]) == str:
        if idescriptor[1].startswith("Delayed replication of"):
          logging.info(idescriptor[1])
          # get "N" descriptor
          _nvar = int(idescriptor[1].split(" ")[3])
          # 配列の長さ -1 - index + 2 から 後ろN個までについて可算
          # = 配列の長さ +1 - index
          _nests[_nlen+1-idx:_nlen+1-idx+_nvar] += 1
        elif idescriptor[1].startswith("Local descriptor"):
          logging.debug(idescriptor[1])
          pass
        else:
          raise UnexpectedBufrError(f"Encountered a supported descriptor.")
    self.nest_idx = _nests
    logging.info(f"self.nest_idx = {self.nest_idx}")
    for idx, _inest in enumerate(self.nest_idx):
      self.descriptors[idx].append(_inest)
  
  def _read_data_from_str_bin(self, idx=0, nest=0):
    logging.info(" ")
    _data = []
    for jdx, (fxxyy, descriptor, inest) in enumerate(self.descriptors[idx:]):
      logging.debug(descriptor, stack_info=False)
      if nest == inest:
        # 0: 要素記述子, 1: 反復記述子, 2: 操作記述子, 3: 集約記述子
        # 0: F-XX-YYY, 1: SCALE, 2: REFERENCE VALUE, 3: BIT WIDTH
        # 4: UNIT, 5: MNEMONIC, 6: DESC CODE, 7: ELEMENT NAME
        if type(descriptor) == str:
          if descriptor.startswith("Delayed replication of"):
            logging.info(descriptor, stack_info=False)
            _data.append(None)
          elif descriptor.startswith("Local descriptor"):
            logging.info(descriptor, stack_info=False)
            self.local_flag = True
            _data.append(None)
          else:
            logging.info(descriptor)
            raise UnexpectedBufrError(f"Encountered a supported descriptor.")
        else:
          # TODO:データ読み込み処理
          # CCITT IA5, Code table, Flag table, other(Numeric, m, Hz, etc) に分類して処理
          # 0-31-000, 0-31-001, 0-31-002については空リストを作成し、appendしていく形に
          if fxxyy in ("0-31-000", "0-31-001", "0-31-002"):
            nloop = int(self.raw_data[self.irec:self.irec+int(descriptor[3])], 2)
            self.irec += int(descriptor[3])
            _data.append(nloop)
            _loop_data = []
            logging.info(nloop)
            for _ in range(nloop):
              _loop_data.append(self._read_data_from_str_bin(idx=idx+jdx+1, nest=nest+1))
            _data.append(_loop_data)
          elif descriptor[4] in ("Flag table"):
            _data.append(self.raw_data[self.irec:self.irec+int(descriptor[3])])
            self.irec += int(descriptor[3])
          else:
            _data.append((int(self.raw_data[self.irec:self.irec+int(descriptor[3])], 2)+int(descriptor[2]))*10**int(descriptor[1]))
            self.irec += int(descriptor[3])
      else:
        # ループを抜ける
        break
    return _data
  
  def get_data(self):
    return self.data

  def _decode_data(self):
    return


def _int_into_fxxyyy(num: int) -> str:
  bits = format(num, "016b")
  # print(str(int(format(num, "016b")[-16:-14], 2))
  #         + "-" + str(int(format(num, "016b")[-14:-8], 2))
  #         + "-" + str(int(format(num, "016b")[-8:], 2)))
  return f"{int(bits[-16:-14], 2)}-{int(bits[-14:-8], 2):02}-{int(bits[-8:], 2):03}"

def old_print_bufr_info(file_path) -> None:
  with open(file_path, 'rb') as f:
    binary = f.read()
  
  df_b = parse_tableB_into_dataframe()
  loc_df_b_1 = parse_tableB_into_dataframe("LOC_0_7_1")
  loc_df_b_2 = parse_tableB_into_dataframe("ADD_1_0")
  table_c = parse_codeFlag_into_dict()
  table_d = parse_tableD_into_dict()
  loc_table_c_1 = parse_codeFlag_into_dict("LOC_0_7_1")
  loc_table_c_2 = parse_codeFlag_into_dict("ADD_1_0")
  
  len_ = {'sec0':8, 'sec1':22, 'sec3':55, 'sec5':4}
  
  header = binary[0:12+1+8+1+6+1+3+4+1].decode()
  header_list = binary[0:12+1+8+1+6+1+3+4+1].decode().split(" ")
  # 指示コードなし
  if header_list[2][6:10] == "BUFR":
    identify_code = "定時報"
    sec0_start = len(header_list[0]) + 1 + len(header_list[1]) + 1 + 6
    logging.debug(f"sec0_start = {sec0_start}")
  # 指示コードあり
  else:
    if header_list[3][6:].startswith("A"):
      identify_code = "修正報"
    elif header_list[3][6:].startswith("C"):
      identify_code = "訂正報"
    elif header_list[3][6:].startswith("R"):
      identify_code = "遅延報"
    sec0_start = len(header_list[0]) + 1 + len(header_list[1]) + 1 + 6 + 1 + 3
  logging.debug(f"identify_code : {identify_code}")
  logging.debug(f"電文ヘッダ = {header[:sec0_start]}")
  print(f"電文ヘッダ = {header[:sec0_start]}")
  
  # Section 0, Indicator section
  section_desc = "第0節(指示節)"
  sec0_binary = binary[sec0_start:sec0_start+len_['sec0']]
  print(f"{section_desc} 1~4 32 国際アルファベットNo5による記述でBUFR = {sec0_binary[:4].decode()}")
  print(f"{section_desc} 5~7 24 BUFR報全体の長さ = {int.from_bytes(sec0_binary[4:7], "big")}")
  print(f"{section_desc} 8   8  BUFR報の版番号 = {int.from_bytes(sec0_binary[7:], "big")}")
  
  # Section 1, Identification section
  section_desc = "第1節(識別節)"
  sec1_start = sec0_start + len_['sec0']
  len_['sec1'] = int.from_bytes(binary[sec1_start:sec1_start+3], "big")
  sec1_binary = binary[sec1_start:sec1_start+len_['sec1']]
  if int.from_bytes(sec1_binary[0:0+3], "big") != len_["sec1"]:
    raise NotSupportedBufrError(file_path, f"第1節の長さが{len_['sec1']}でない")
  else:
    print(f"{section_desc} 1~3 24 第1節の長さ = {int.from_bytes(sec1_binary[0:0+3], "big")}")
  # sec1_format = [["4",   8 , "BUFRマスター表(標準は0)"],
  #                ["5~8", 16, "作成中枢の識別"]]
  logging.info(f"{section_desc} 4   8  BUFRマスター表 = {int.from_bytes(sec1_binary[3:3+1], "big")}")
  logging.info(f"{section_desc} 5~6 16 作成中枢の識別 = {int.from_bytes(sec1_binary[4:4+2], "big")} {table_c["0-01-035"]["VALBITS"][f"{int.from_bytes(sec1_binary[4:4+2], "big")}"]}")
  logging.info(f"{section_desc} 7~8 16 作成副中枢の識別 = {int.from_bytes(sec1_binary[6:6+2], "big")}")
  logging.info(f"{section_desc} 9   8  更新一連番号 = {int.from_bytes(sec1_binary[8:8+1], "big")}")
  logging.info(f"{section_desc} 10  8  任意節の有無 = {bool(int(format(int.from_bytes(sec1_binary[9:9+1], "big"), "08b")[0]))}")
  logging.info(f"{section_desc} 11  8  資料の種類 = {int.from_bytes(sec1_binary[10:10+1], "big")} {bufrtab_TableA.data_types[int.from_bytes(sec1_binary[10:10+1], "big")]}")
  logging.info(f"{section_desc} 12  8  国際的な資料サブカテゴリ = {int.from_bytes(sec1_binary[11:11+1], "big")} {bufrtab_TableA.standard_subtypes[int.from_bytes(sec1_binary[10:10+1], "big")][int.from_bytes(sec1_binary[11:11+1], "big")]}")
  if int.from_bytes(sec1_binary[12:12+1], "big") in bufrtab_TableA.local_subtypes[int.from_bytes(sec1_binary[10:10+1], "big")].keys():
    logging.info(f"{section_desc} 13  8  地域的な資料サブカテゴリ = {int.from_bytes(sec1_binary[12:12+1], "big")} {bufrtab_TableA.local_subtypes[int.from_bytes(sec1_binary[10:10+1], "big")][int.from_bytes(sec1_binary[12:12+1], "big")]}")
  elif int.from_bytes(sec1_binary[12:12+1], "big") == 0:
    logging.info(f"{section_desc} 13  8  地域的な資料サブカテゴリ = {int.from_bytes(sec1_binary[12:12+1], "big")} 中枢で定義=0")
  else:
    logging.info(f"{section_desc} 13  8  地域的な資料サブカテゴリ = {int.from_bytes(sec1_binary[12:12+1], "big")} 不明")
  if (int.from_bytes(sec1_binary[13:13+1], "big") < OLDEST_MASTER_TABLE_VERSION):
    warnings.warn(NotSupportedOlderVersionMSWarning(int.from_bytes(sec1_binary[13:13+1], "big")))
  elif (LATEST_MASTER_TABLE_VERSION < int.from_bytes(sec1_binary[13:13+1], "big")):
    warnings.warn(NotSupportedNewerVersionMSWarning(int.from_bytes(sec1_binary[13:13+1], "big")))
  logging.info(f"{section_desc} 14  8  マスターテーブルのバージョン番号 = {int.from_bytes(sec1_binary[13:13+1], "big")}")
  logging.info(f"{section_desc} 15  8  マスターテーブルに加えて使用したローカルテーブルのバージョン番号 = {int.from_bytes(sec1_binary[14:14+1], "big")}")
  logging.info(f"{section_desc} 16~17  16 年(電文作成年月日時分秒) = {int.from_bytes(sec1_binary[15:15+2], "big")}")
  logging.info(f"{section_desc} 18  8  月(電文作成年月日時分秒) = {int.from_bytes(sec1_binary[17:17+1], "big")}")
  logging.info(f"{section_desc} 19  8  日(電文作成年月日時分秒) = {int.from_bytes(sec1_binary[18:18+1], "big")}")
  logging.info(f"{section_desc} 20  8  時(電文作成年月日時分秒) = {int.from_bytes(sec1_binary[19:19+1], "big")}")
  logging.info(f"{section_desc} 21  8  分(電文作成年月日時分秒) = {int.from_bytes(sec1_binary[20:20+1], "big")}")
  logging.info(f"{section_desc} 22  8  秒(電文作成年月日時分秒) = {int.from_bytes(sec1_binary[21:21+1], "big")}")
  
  # Section 2, Optional Section
  if format(int.from_bytes(sec1_binary[9:9+1], "big"), "08b")[0] != "0":
    raise NotSupportedBufrError(file_path, f"第2節の長さが0ではなく{int.from_bytes(sec1_binary[9:9+1], "big")}である")
  
  # Section 3, Data description section
  section_desc = "第3節(資料記述節)"
  sec3_start = sec1_start + len_["sec1"]
  len_["sec3"] = int.from_bytes(binary[sec3_start:sec3_start+3], "big")
  sec3_binary = binary[sec3_start:sec3_start+len_['sec3']]
  # not handle when section 2 exists
  if format(int.from_bytes(sec1_binary[9:9+1], "big"), "08b")[0] != "0":
    raise NotSupportedBufrError(file_path, f"第2節の長さが0ではなく{len_["sec3"]}")
  logging.info(f"{section_desc} 1 ~ 3  24 第3節の長さ(オクテット単位) = {len_["sec3"]}")
  logging.info(f"{section_desc} 4      8  保留 = {int.from_bytes(sec3_binary[3:3+1], "big")}")
  logging.info(f"{section_desc} 5 ~ 6  16 データサブセットの数 = {int.from_bytes(sec3_binary[4:4+2], "big")}")
  _data_type = ""
  _data_type_flag = format(int.from_bytes(sec3_binary[6:6+1], "big"), "08b")
  _data_type += "観測でない&" if _data_type_flag[0] == "0" else "観測&"
  _data_type += "圧縮でない" if _data_type_flag[1] == "0" else "圧縮"
  logging.info(f"{section_desc} 7      8  {_data_type} = {_data_type_flag}")
  
  # 8オクテット目以降
  std_flag = True
  variables = []
  for _i in range(8, len_["sec3"]+1, 2):
    # 標準のBテーブルでマッチした場合
    _fxxyyy = _int_into_fxxyyy(int.from_bytes(sec3_binary[_i-1:_i+1], "big"))
    if std_flag:
      if len(df_b[df_b["F-XX-YYY"] == _fxxyyy]["ELEMENT_NAME"].values) == 1:
        logging.info(f"{section_desc} {_i} ~ {_i+1}  16 {df_b[df_b["F-XX-YYY"] == _fxxyyy]["ELEMENT_NAME"].values[0]} = {_fxxyyy}")
        variables.append(df_b[df_b["F-XX-YYY"] == _fxxyyy].to_string(header=None, index=None))
      elif (_fxxyyy[:1] == "1") & (_fxxyyy[-3:] == "000"):
        logging.info(f"{section_desc} {_i} ~ {_i+1}  16 Delayed replication of {int(_fxxyyy[2:4])} descriptor = {_fxxyyy}")
        variables.append(f" {_fxxyyy}  0  0  0  NONE  NONE   Delayed replication of {int(_fxxyyy[2:4])} descriptor")
      elif _fxxyyy.startswith("2-06-"):
        logging.info(f"{section_desc} {_i} ~ {_i+1}  16 Local descriptor = {_fxxyyy}")
        std_flag = False
        variables.append(f" {_fxxyyy}  0  0  0  NONE  NONE   Local descriptor")
      else:
        logging.info(f"{section_desc} {_i} ~ {_i+1}  16 {df_b[df_b["F-XX-YYY"] == _fxxyyy]["ELEMENT_NAME"].values} = {_fxxyyy}")
        variables.append(f" {_fxxyyy}  0  0  0  NONE  NONE   NO INFOMATION VARIABLE")
    else:
      if len(loc_df_b_1[loc_df_b_1["F-XX-YYY"] == _fxxyyy]["ELEMENT_NAME"].values) == 1:
        logging.info(f"{section_desc} {_i} ~ {_i+1}  16 {loc_df_b_1[loc_df_b_1["F-XX-YYY"] == _fxxyyy]["ELEMENT_NAME"].values[0]} = {_fxxyyy}")
        variables.append(loc_df_b_1[loc_df_b_1["F-XX-YYY"] == _fxxyyy].to_string(header=None, index=None))
      elif len(loc_df_b_2[loc_df_b_2["F-XX-YYY"] == _fxxyyy]["ELEMENT_NAME"].values) == 1:
        logging.info(f"{section_desc} {_i} ~ {_i+1}  16 {loc_df_b_2[loc_df_b_2["F-XX-YYY"] == _fxxyyy]["ELEMENT_NAME"].values[0]} = {_fxxyyy}")
        variables.append(loc_df_b_2[loc_df_b_2["F-XX-YYY"] == _fxxyyy].to_string(header=None, index=None))
      else:
        logging.info(f"{section_desc} {_i} ~ {_i+1}  16 {df_b[df_b["F-XX-YYY"] == _fxxyyy]["ELEMENT_NAME"].values} = {_fxxyyy}")
        variables.append(f" {_fxxyyy}  0  0  0  NONE  NONE   NO INFOMATION VARIABLE",)
      std_flag = True
  
  # Section 4, Data section
  section_desc = "第4節(資料節)"
  sec4_start = sec3_start + len_["sec3"]
  len_["sec4"] = int.from_bytes(binary[sec4_start:sec4_start+3], "big")
  sec4_binary = binary[sec4_start:sec4_start+len_['sec4']]
  logging.info(f"{section_desc} 1  ~ 3   24 第4節の長さ(オクテット単位) = {len_["sec4"]}")
  
  # Section 5, End section
  section_desc = "第5節(終端節)"
  sec5_start = sec4_start + len_["sec4"]
  sec5_binary = binary[sec5_start:sec5_start+len_['sec5']]
  if sec5_binary.decode() == "7777":
    logging.info(f"{section_desc} 1  ~ 4   32 BUFR報の終わりを指す = {sec5_binary.decode()}")
    logging.info(f"BUFRの終端に到達しました。正常に読込が終了しました。")
  else:
    raise UnexpectedBufrError(f"BUFRの終端に到達しませんでした。ファイルが正常であるか確認してください。")
  
  print()
  print("Data descriptor infomation:")
  for iv in variables:
    print(iv)


if __name__=='__main__':
  # df_b = parse_tableB_into_dataframe()
  # print(df_b.head(50))
  # dict_d = parse_tableD_into_dict()
  # print(dict_d["3-40-026"])
  # dict_codeFlag = parse_codeFlag_into_dict()
  # print(dict_codeFlag["0-01-033"])
  # print(dict_codeFlag["0-01-034"])
  # dict_codeFlag = parse_codeFlag_into_dict("LOC_0_7_1")
  # print(dict_codeFlag)
  old_print_bufr_info(os.path.join(os.path.dirname(__file__), f"../../tests/data/bufr/print_bufr_info/IUPC41_RJTD_010000_202406010016132_001.send"))
  bufr_class = bufr(os.path.join(os.path.dirname(__file__), f"../../tests/data/bufr/print_bufr_info/IUPC41_RJTD_010000_202406010016132_001.send"))
  print()
  print("Data description:")
  for iv in bufr_class.get_data_description():
    print(iv)
  print()
  print("Data descriptor infomation:")
  for iv in bufr_class.get_data_descriptors():
    print(iv)
  print()
  
  # data = bufr_class.read_data()
  # print(data[8])
  # print(data[8][0])
  # print(data[8][0][9])
  # print(len(data[8]))