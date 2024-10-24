# Copyright (c) 2024, NakaMetPy Develoers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

import pandas as pd
from .constants import LATEST_MASTER_TABLE_VERSION
from ._error import NotSupportedNewerVersionMSWarning, NotSupportedOlderVersionMSWarning,\
                    NotSupportedBufrError
import os
import re
import logging

# Change HERE when developing from INFO into DEBUG
# It will be help you.
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
# logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
# logging.disable(logging.CRITICAL)

def parse_bufrtab(file_path: str) -> list:
  with open(file_path, mode="r") as f:
    raw_text = f.readlines()[1:-1]
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

def get_bufr_info(file_path) -> None:
  with open(file_path, 'rb') as f:
    binary = f.read()
  
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
  logging.info(f"電文ヘッダ = {header[:sec0_start]}")
  
  # Section 0
  section_desc = "第0節(指示節)"
  sec0_binary = binary[sec0_start:sec0_start+len_['sec0']]
  logging.info(f"{section_desc} 1~4 32 国際アルファベットNo5による記述でBUFR = {sec0_binary[:4].decode()}")
  logging.info(f"{section_desc} 5~7 24 BUFR報全体の長さ = {int.from_bytes(sec0_binary[4:7], "big")}")
  logging.info(f"{section_desc} 8   8  BUFR報の版番号 = {int.from_bytes(sec0_binary[7:], "big")}")
  
  # Section 1
  section_desc = "第1節(識別節)"
  sec1_start = sec0_start + len_['sec0']
  sec1_binary = binary[sec1_start:sec1_start+len_['sec1']]
  if int.from_bytes(sec1_binary[0:0+3], "big") != len_["sec1"]:
    raise NotSupportedBufrError(file_path, f"第1節の長さが{len_['sec1']}でない")
  else:
    logging.info(f"{section_desc} 1~3 24 第1節の長さ = {int.from_bytes(sec1_binary[0:0+3], "big")}")
  


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
  get_bufr_info(os.path.join(os.path.dirname(__file__), f"../../tests/data/bufr/print_bufr_info/IUPC41_RJTD_010000_202406010016132_001.send"))