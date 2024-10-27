# Copyright (c) 2024, NakaMetPy Develoers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

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

def _int_into_fxxyyy(num: int) -> str:
  bits = format(num, "016b")
  # print(str(int(format(num, "016b")[-16:-14], 2))
  #         + "-" + str(int(format(num, "016b")[-14:-8], 2))
  #         + "-" + str(int(format(num, "016b")[-8:], 2)))
  return f"{int(bits[-16:-14], 2)}-{int(bits[-14:-8], 2):02}-{int(bits[-8:], 2):03}"

def print_bufr_info(file_path) -> None:
  with open(file_path, 'rb', encoding="utf-8") as f:
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
        logging.info(f"{section_desc} {_i} ~ {_i+1}  16 Local discriptor = {_fxxyyy}")
        std_flag = False
        variables.append(f" {_fxxyyy}  0  0  0  NONE  NONE   Local discriptor")
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
  print_bufr_info(os.path.join(os.path.dirname(__file__), f"../../tests/data/bufr/print_bufr_info/IUPC41_RJTD_010000_202406010016132_001.send"))