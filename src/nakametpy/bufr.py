# Copyright (c) 2024, NakaMetPy Develoers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

import pandas as pd
from nakametpy.constants import LATEST_MASTER_TABLE_VERSION, OLDEST_MASTER_TABLE_VERSION,\
                                convert_decimal_to_IA5character
from nakametpy.tables import bufrtab_TableA
from nakametpy._error import NotSupportedNewerVersionMSWarning, NotSupportedOlderVersionMSWarning,\
                    NotSupportedBufrError, UnexpectedBufrError,\
                    MayNotBeAbleToReadBufrWarning
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
  """Common method for parsing bufrtab file.

  Parameters
  ----------
  file_path : str
      path to bufrtab file

  Returns
  -------
  list
      striped readlines
  """
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
  """read master table B and get pandas DataFrame

  Parameters
  ----------
  version : str, optional
      Version of master table B, by default f"STD_0_{LATEST_MASTER_TABLE_VERSION:02}"<br>
      Format is "STD_0_??" / "LOC_0_7_1" / "ADD_1_0"<br>

  Returns
  -------
  pd.DataFrame
      master table B
  """
  columns = ['F-XX-YYY', "SCALE", "REFERENCE_VALUE", "BIT_WIDTH", "UNIT", "MNEMONIC", "DESC_CODE", 'ELEMENT_NAME']
  
  bufrtab = os.path.join(os.path.dirname(__file__), f"./tables/bufrtab.TableB_{version:02}")
  valid_records = parse_bufrtab(bufrtab)
  # print(valid_records[-1])
  df = pd.DataFrame([re.split("[|;]", irecord.strip()) for irecord in valid_records])
  # 不要な文字を削除を削除
  df = df.apply(lambda x: x.str.strip())
  #'ELEMENT_NAME';が含まれるカラムNoneのみの列を削除
  if (len(columns) + 1) == len(df.columns.values):
    # 最後の列のインデックスを取得
    last_col = df.columns[-1]
    df.loc[df[last_col].notnull(), df.columns[-2]] += ("; " + df[last_col])
    # df[df.iloc[:, -1] is not None].iloc[:, -2] = df.iloc[:, :-2]+"; "+df.iloc[:, :-1]
    df = df.iloc[:, :-1]
  df.columns = columns
  return df

def parse_tableD_into_dict(version: str=f"STD_0_{LATEST_MASTER_TABLE_VERSION:02}") -> dict:
  """read master table D and get dict

  Parameters
  ----------
  version : str, optional
      Version of master table D, by default f"STD_0_{LATEST_MASTER_TABLE_VERSION:02}"<br>
      Format is "STD_0_??" / "LOC_0_7_1" / "ADD_1_0"<br>

  Returns
  -------
  dict
      master table D
  """
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

def parse_codeFlag_into_dict(version: str=f"STD_0_{LATEST_MASTER_TABLE_VERSION:02}") -> dict:
  """read master table CODE/FLAG and get dict

  Parameters
  ----------
  version : str, optional
      Version of master table CODE/FLAG, by default f"STD_0_{LATEST_MASTER_TABLE_VERSION:02}"<br>
      Format is "STD_0_??" / "LOC_0_7_1" / "ADD_1_0"<br>

  Returns
  -------
  dict
      master table CODE/FLAG
  """
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
  def __init__(self, file_path: str, highest_priority_add_tbl: bool=False) -> None:
    """Read BUFR<br>
    BUFRを読むクラス<br>

    Parameters
    ----------
    file_path : str
        path to BUFR file.<br>
        BUFRファイルのパス
    highest_priority_add_tbl : bool, optional
        Set highest priority on additional table, by default False<br>
        追加テーブルを最優先で用いる際に設定するフラグ
    
    Notes
    -----
    This function does not support section 2

    Raises
    ------
    NotSupportedBufrError
        Raise when section 2 exist
    """
    self.file_path = file_path
    self.highest_priority_add_tbl = highest_priority_add_tbl
    
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
    self.sec_3 = bufr_sec_3(self.binary, self.sec_len, self.sec_1.sec1_use_master_table_version, self.highest_priority_add_tbl)
    logging.debug(f"サブセット数：{self.sec_3.sec3_05_06_num_of_data_subset}")
    logging.debug(self.sec_3.sec3_07_data_format)
    self.sec_4 = bufr_sec_4(self.binary, self.sec_len)
    self.sec_5 = bufr_sec_5(self.binary, self.sec_len)
  
  def get_data_descriptors(self) -> list:
    """get data descriptor in section 3

    Returns
    -------
    list
        data descriptor<br>
        f-xx-yyy, data descriptor<br>
        str, pd.DataFrame or str
    """
    return self.sec_3.sec3_data_desc_list
    
  def get_data_description(self) -> list:
    """get data description in section 3

    Returns
    -------
    list
        data description<br>
        str
    """
    return self.sec_3.sec3_data_desc_str_list
  
  def get_extracted_data_descriptors(self) -> list:
    """get data descriptor extracted F=3 descriptor

    Returns
    -------
    list
        data descriptor<br>
        f-xx-yyy, data descriptor, nest<br>
        str, pd.DataFrame or str, int
    """
    return self.sec_3.sec3_data_desc_extract_list
  
  def get_extracted_data_description(self) -> list:
    """get data description extracted F=3 descriptor

    Returns
    -------
    list
        data description<br>
        str
    """
    return self.sec_3.sec3_data_desc_str_extract_list
  
  def read_data(self) -> list:
    """get BUFR data in data section (section 4)<br>
    データ節 (セクション4) のデータを読み込む<br>

    Returns
    -------
    list
        data
    """
    descriptors = self.get_extracted_data_descriptors()
    return self.sec_4.read_data(descriptors, self.sec_len, self.sec_3.sec3_05_06_num_of_data_subset)

class bufr_sec_head:
  def __init__(self, binary: bytes, sec_len: dict) -> None:
    """read bufr header<br>
    BUFRのヘッダを読み込むクラス

    Parameters
    ----------
    binary : bytes
        binary data of BUFR<br>
        BUFRのバイナリデータ
    sec_len : dict
        length of sections<br>
        セクションの長さ
    """
    if binary[0:4].decode() == "BUFR":
      # print("This telegram has no header.")
      logging.info("This telegram has no header.")
      sec_len['sec_head'] = 0
    else:
      head = binary[0:12+1+8+1+6+1+3+4+1].lstrip(b"\n")
      head_list = binary[0:12+1+8+1+6+1+3+4+1].split()
      # TODO: ここのロジックは無駄があると思われる。
      # 指示コードなし or 改行済 且つ 末尾が指示コードから始まらない()
      if ((head_list[2][6:10].decode() == "BUFR") | (head_list[2][6:10].decode() == "")):
        if len(head_list) == 3:
          sec_len['sec_head'] = len(head_list[0]) + 1 + len(head_list[1]) + 1 + 6
        else:
          if not ((head_list[3].startswith(b"C") | head_list[3].startswith(b"R"))):
            sec_len['sec_head'] = len(head_list[0]) + 1 + len(head_list[1]) + 1 + 6
          else:
            sec_len['sec_head'] = len(head_list[0]) + 1 + len(head_list[1]) + 1 + 6 + 1 + 3
      # 指示コードあり
      else:
        sec_len['sec_head'] = len(head_list[0]) + 1 + len(head_list[1]) + 1 + 6 + 1 + 3
      logging.debug(f"sec0_start = {sec_len['sec_head']}")
      self.tlg_header = head[:sec_len['sec_head']].decode()
      logging.debug(f"電文ヘッダ = {self.tlg_header}")

class bufr_sec_0:
  def __init__(self, binary: bytes, sec_len: dict) -> None:
    """read bufr Indicator section (section 0)<br>
    BUFRの指示節(第0節)を読み込むクラス

    Parameters
    ----------
    binary : bytes
        binary data of BUFR<br>
        BUFRのバイナリデータ
    sec_len : dict
        length of sections<br>
        セクションの長さ
    """
    # Section 0, Indicator section
    # print(binary[sec_len['sec_head']:sec_len['sec_head']+1])
    # ヘッダと本文の間に改行がある場合
    if binary[sec_len['sec_head']:sec_len['sec_head']+1] in (b"\n", b"\r", b"\r\n"):
      self.sec0_binary = binary[sec_len['sec_head']+1:sec_len['sec_head']+sec_len['sec0']+1]
      sec_len["sec0"] += 1
    else:
      self.sec0_binary = binary[sec_len['sec_head']:sec_len['sec_head']+sec_len['sec0']]
    self.sec0_desc_en = "Section 0, Indicator section"
    self.sec0_desc_jp = "第0節(指示節)"
    # print(self.sec0_binary)
    self.sec0_01_04_bufr_str = self.sec0_binary[:4].decode()
    self.sec0_05_07_bufr_len = int.from_bytes(self.sec0_binary[4:7], "big")
    self.sec0_08_bufr_version = int.from_bytes(self.sec0_binary[7:], "big")
    logging.debug(f"{self.sec0_desc_jp} 1~4 32 国際アルファベットNo5による記述でBUFR = {self.sec0_01_04_bufr_str}")
    logging.debug(f"{self.sec0_desc_jp} 5~7 24 BUFR報全体の長さ = {self.sec0_05_07_bufr_len}")
    logging.debug(f"{self.sec0_desc_jp} 8   8  BUFR報の版番号 = {self.sec0_08_bufr_version}")

class bufr_sec_1:
  def __init__(self, binary: bytes, sec_len: dict) -> None:
    """read bufr Identification section (section 1)<br>
    BUFRの識別節(第1節)を読み込むクラス

    Parameters
    ----------
    binary : bytes
        binary data of BUFR<br>
        BUFRのバイナリデータ
    sec_len : dict
        length of sections<br>
        セクションの長さ
    """
    # Section 1, Identification section
    self.sec1_desc_en = "Section 1, Identification section"
    self.sec1_desc_jp = "第1節(識別節)"
    self.latest_table_c = parse_codeFlag_into_dict()
    
    self.sec1_start = sec_len['sec_head'] + sec_len['sec0']
    sec_len['sec1'] = int.from_bytes(binary[self.sec1_start:self.sec1_start+3], "big")
    self.sec1_binary = binary[self.sec1_start:self.sec1_start+sec_len['sec1']]
    logging.debug(f"{sec_len['sec1']}, {self.sec1_binary}")
    if sec_len['sec1'] != 22:
      warnings.warn(MayNotBeAbleToReadBufrWarning(f"第1節の長さが22ではなく、{sec_len['sec1']}"))
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
    # self.sec1_12_global_data_subcategory = bufrtab_TableA.standard_subtypes[self.sec1_11_type_of_data_code][self.sec1_12_global_data_subcategory_code]
    if self.sec1_12_global_data_subcategory_code in bufrtab_TableA.standard_subtypes[self.sec1_11_type_of_data_code].keys():
      if len(bufrtab_TableA.standard_subtypes[self.sec1_11_type_of_data_code]) > 1:
        self.sec1_12_global_data_subcategory = bufrtab_TableA.standard_subtypes[self.sec1_11_type_of_data_code][self.sec1_12_global_data_subcategory_code]
      else:
        self.sec1_12_global_data_subcategory = ""
    else:
      self.sec1_12_global_data_subcategory = ""
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
  def __init__(self, binary: bytes, sec_len: dict, mst_tbl_version: str, highest_priority_add_tbl: bool) -> None:
    """read bufr Data description section (section 3)<br>
    BUFRの資料記述節(第3節)を読み込むクラス

    Parameters
    ----------
    binary : bytes
        binary data of BUFR<br>
        BUFRのバイナリデータ
    sec_len : dict
        length of sections<br>
        セクションの長さ
    mst_tbl_version : str
        master table version<br>
        マスターテーブルのバージョン
    highest_priority_add_tbl : bool
        Set highest priority on additional table<br>
        追加テーブルを最優先で用いる際に設定するフラグ

    Raises
    ------
    UnexpectedBufrError
        raise when encountered unknown data descriptor<br>
        予期せぬ資料記述子があった場合に発生
    """
    # Section 1, Identification section
    self.sec3_desc_en = "Section 3, Data description section"
    self.sec3_desc_jp = "第3節(資料記述節)"
    self.std_df_b = parse_tableB_into_dataframe(f"STD_0_{mst_tbl_version}")
    self.std_table_c = parse_codeFlag_into_dict(f"STD_0_{mst_tbl_version}")
    self.std_table_d = parse_tableD_into_dict(f"STD_0_{mst_tbl_version}")
    self.loc_df_b_1 = parse_tableB_into_dataframe("LOC_0_7_1")
    self.loc_df_b_2 = parse_tableB_into_dataframe("ADD_1_0")
    self.loc_table_d_1 = parse_tableD_into_dict("LOC_0_7_1")
    
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
    no_f3_info = False
    data_desc_list = []
    data_desc_str_list = []
    for _i in range(8, sec_len["sec3"], 2):
      # 標準のBテーブルでマッチした場合
      _fxxyyy = _int_into_fxxyyy(int.from_bytes(self.sec3_binary[_i-1:_i+1], "big"))
      if highest_priority_add_tbl:
        if len(self.loc_df_b_2[self.loc_df_b_2['F-XX-YYY'] == _fxxyyy]['ELEMENT_NAME'].values) == 1:
          logging.debug(f"{self.sec3_desc_jp} {_i} ~ {_i+1}  16 {self.loc_df_b_2[self.loc_df_b_2['F-XX-YYY'] == _fxxyyy]['ELEMENT_NAME'].values[0]} = {_fxxyyy}")
          data_desc_list.append([_fxxyyy, self.loc_df_b_2[self.loc_df_b_2['F-XX-YYY'] == _fxxyyy].values[0]])
          data_desc_str_list.append(self.loc_df_b_2[self.loc_df_b_2['F-XX-YYY'] == _fxxyyy].to_string(header=None, index=None))
          continue
      if std_flag:
        if len(self.std_df_b[self.std_df_b['F-XX-YYY'] == _fxxyyy]['ELEMENT_NAME'].values) == 1:
          logging.debug(f"{self.sec3_desc_jp} {_i} ~ {_i+1}  16 {self.std_df_b[self.std_df_b['F-XX-YYY'] == _fxxyyy]['ELEMENT_NAME'].values[0]} = {_fxxyyy}")
          data_desc_list.append([_fxxyyy, self.std_df_b[self.std_df_b['F-XX-YYY'] == _fxxyyy].values[0]])
          data_desc_str_list.append(self.std_df_b[self.std_df_b['F-XX-YYY'] == _fxxyyy].to_string(header=None, index=None))
        elif (_fxxyyy[:1] == "1"):
          if (_fxxyyy[-3:] == "000"):
            logging.debug(f"{self.sec3_desc_jp} {_i} ~ {_i+1}  16 Delayed replication of {int(_fxxyyy[2:4])} descriptor = {_fxxyyy}")
            data_desc_list.append([_fxxyyy, f"Delayed replication of {int(_fxxyyy[2:4])} descriptor"])
            data_desc_str_list.append(f" {_fxxyyy}  0  0  0  NONE  NONE   Delayed replication of {int(_fxxyyy[2:4])} descriptor")
          else:
            logging.debug(f"{self.sec3_desc_jp} {_i} ~ {_i+1}  16 Replicate {int(_fxxyyy[2:4])} descriptors {int(_fxxyyy[5:8])} times = {_fxxyyy}")
            data_desc_list.append([_fxxyyy, f"Replicate {int(_fxxyyy[2:4])} descriptors {int(_fxxyyy[5:8])} times"])
            data_desc_str_list.append(f" {_fxxyyy}  0  0  0  NONE  NONE   Replicate {int(_fxxyyy[2:4])} descriptors {int(_fxxyyy[5:8])} times")
        elif _fxxyyy.startswith("2-06-"):
          logging.debug(f"{self.sec3_desc_jp} {_i} ~ {_i+1}  16 Local descriptor = {_fxxyyy}")
          std_flag = False
          data_desc_list.append([_fxxyyy, f"Local descriptor"])
          data_desc_str_list.append(f" {_fxxyyy}  0  0  0  NONE  NONE   Local descriptor")
        elif _fxxyyy.startswith("2-"):
          logging.debug(f"{self.sec3_desc_jp} {_i} ~ {_i+1}  16 Operate descriptor = {_fxxyyy}")
          data_desc_list.append([_fxxyyy, f"Operate descriptor"])
          data_desc_str_list.append(f" {_fxxyyy}  0  0  0  NONE  NONE   Operate descriptor")
        elif _fxxyyy.startswith("3-"):
          # print(_fxxyyy)
          if _fxxyyy in self.std_table_d.keys():
            logging.debug(f"{self.std_table_d[_fxxyyy]["MNEMONIC"]} {_i} ~ {_i+1}  16 {self.std_table_d[_fxxyyy]["NAME"]} = {_fxxyyy}")
            data_desc_list.append([_fxxyyy, self.std_table_d[_fxxyyy]])
            data_desc_str_list.append(f" {_fxxyyy}  0  0  0  NONE  NONE   {self.std_table_d[_fxxyyy]["NAME"]}")
          else:
            no_f3_info = True
        else:
          logging.debug(f"{self.sec3_desc_jp} {_i} ~ {_i+1}  16 {self.std_df_b[self.std_df_b['F-XX-YYY'] == _fxxyyy]['ELEMENT_NAME'].values} = {_fxxyyy}")
          data_desc_list.append([_fxxyyy, f"NO INFOMATION VARIABLE"])
          data_desc_str_list.append(f" {_fxxyyy}  0  0  0  NONE  NONE   NO INFOMATION VARIABLE")
      else:
        if len(self.loc_df_b_1[self.loc_df_b_1['F-XX-YYY'] == _fxxyyy]['ELEMENT_NAME'].values) == 1:
          logging.debug(f"{self.sec3_desc_jp} {_i} ~ {_i+1}  16 {self.loc_df_b_1[self.loc_df_b_1['F-XX-YYY'] == _fxxyyy]['ELEMENT_NAME'].values[0]} = {_fxxyyy}")
          data_desc_list.append([_fxxyyy, self.loc_df_b_1[self.loc_df_b_1['F-XX-YYY'] == _fxxyyy].values[0]])
          data_desc_str_list.append(self.loc_df_b_1[self.loc_df_b_1['F-XX-YYY'] == _fxxyyy].to_string(header=None, index=None))
        elif len(self.loc_df_b_2[self.loc_df_b_2['F-XX-YYY'] == _fxxyyy]['ELEMENT_NAME'].values) == 1:
          logging.debug(f"{self.sec3_desc_jp} {_i} ~ {_i+1}  16 {self.loc_df_b_2[self.loc_df_b_2['F-XX-YYY'] == _fxxyyy]['ELEMENT_NAME'].values[0]} = {_fxxyyy}")
          data_desc_list.append([_fxxyyy, self.loc_df_b_2[self.loc_df_b_2['F-XX-YYY'] == _fxxyyy].values[0]])
          data_desc_str_list.append(self.loc_df_b_2[self.loc_df_b_2['F-XX-YYY'] == _fxxyyy].to_string(header=None, index=None))
        elif _fxxyyy.startswith("3-"):
          if _fxxyyy in self.loc_table_d_1.keys():
            logging.debug(f"{self.loc_table_d_1[_fxxyyy]["MNEMONIC"]} {_i} ~ {_i+1}  16 {self.loc_table_d_1[_fxxyyy]["NAME"]} = {_fxxyyy}")
            data_desc_list.append([_fxxyyy, self.loc_table_d_1[_fxxyyy]])
            data_desc_str_list.append(f" {_fxxyyy}  0  0  0  NONE  NONE   {self.loc_table_d_1[_fxxyyy]["NAME"]}")
          else:
            no_f3_info = True
        else:
          logging.info(f"{self.sec3_desc_jp} {_i} ~ {_i+1}  16 {self.std_df_b[self.std_df_b['F-XX-YYY'] == _fxxyyy]['ELEMENT_NAME'].values} = {_fxxyyy}")
          data_desc_list.append([_fxxyyy, f"NO INFOMATION VARIABLE"])
          data_desc_str_list.append(f" {_fxxyyy}  0  0  0  NONE  NONE   NO INFOMATION VARIABLE",)
        std_flag = True
      if no_f3_info == True:
        data_desc_list.append([_fxxyyy, f"NO F=3 INFOMATION AVAILABLE"])
        data_desc_str_list.append(f" {_fxxyyy}  0  0  0  NONE  NONE   NO F=3 INFOMATION AVAILABLE",)
        no_f3_info = False

    self.sec3_data_desc_list = data_desc_list
    self.sec3_data_desc_str_list = data_desc_str_list
    # logging.info(f"self.sec3_data_desc_str_list = {self.sec3_data_desc_list}")
    
    # ネストの深さの特定およびF=3(集約記述子)を展開
    target_list = []
    while True:
      # loop関係のフラグ
      _f3_flag = False
      # df, table検索のフラグ
      std_flag = True
      no_f3_info = False
      if len(target_list) == 0:
        for ilist in self.sec3_data_desc_list:
          # F-XX-YYY, str or df_b, nnest, 遅延反復記述子確認フラグ
          target_list.append(ilist + [0, False])
      else:
        target_list = tmp_list
      # ネストの深さを特定
      _nlen = len(target_list)
      for idx, idescriptor in enumerate(target_list[::-1]):
        if type(idescriptor[1]) == str:
          logging.debug(f"{idescriptor} {idescriptor[1].startswith("Replicate")}", stack_info=False)
          if idescriptor[1].startswith("Delayed replication of"):
            if idescriptor[3] == False:
              logging.debug(idescriptor[1])
              # 遅延反復記述子確認済
              # logging.info(target_list[_nlen+1-idx])
              target_list[_nlen-1-idx][3] = True
              # get "N" descriptor
              _nvar = int(idescriptor[1].split(" ")[3])
              # 配列の長さ -1 - index + 2 から 後ろN個までについて可算
              # = 配列の長さ +1 - index
              for i in range(_nvar):
                target_list[_nlen+1-idx+i][2] += 1
          elif idescriptor[1].startswith("Replicate"):
            if idescriptor[3] == False:
              logging.debug(idescriptor[1])
              # 遅延反復記述子確認済
              # logging.info(target_list[_nlen+1-idx])
              target_list[_nlen-1-idx][3] = True
              # F-XX-YYY
              _, _nvar, _ = idescriptor[0].split("-")
              # 配列の長さ -1 - index + 2 から 後ろN個までについて可算
              # = 配列の長さ +1 - index
              for i in range(int(_nvar)):
                target_list[_nlen-idx+i][2] += 1
          elif idescriptor[1].startswith("Local descriptor"):
            logging.debug(idescriptor[1])
            pass
          elif idescriptor[1].startswith("Operate descriptor"):
            logging.debug(idescriptor[1])
            pass
          else:
            for itarget in target_list:
              logging.info(itarget)
            logging.info(f"Error descriptor: {idescriptor}")
            raise UnexpectedBufrError(f"Encountered an unsupported descriptor.")
      
      # F=3(集約記述子)を展開
      tmp_list = []
      for ilist in target_list:
        # F=0,1,2の場合
        if not ilist[0].startswith("3-"):
          tmp_list.append(ilist)
        # F=3の場合
        else:
          # 集約記述子内の遅延反復記述子のネスト確認が必要なためTrueとする
          _f3_flag = True
          for jlist in ilist[1]["SEQUENCE"]:
            logging.debug(jlist)
            _fxxyyy = jlist["FXXYYY"]
            if highest_priority_add_tbl:
              if len(self.loc_df_b_2[self.loc_df_b_2['F-XX-YYY'] == _fxxyyy]['ELEMENT_NAME'].values) == 1:
                logging.debug(f"{self.sec3_desc_jp} {_i} ~ {_i+1}  16 {self.loc_df_b_2[self.loc_df_b_2['F-XX-YYY'] == _fxxyyy]['ELEMENT_NAME'].values[0]} = {_fxxyyy}")
                tmp_list.append([_fxxyyy, self.loc_df_b_2[self.loc_df_b_2['F-XX-YYY'] == _fxxyyy].values[0], ilist[2], False])
                continue
            if std_flag:
              if len(self.std_df_b[self.std_df_b['F-XX-YYY'] == _fxxyyy]['ELEMENT_NAME'].values) == 1:
                logging.debug(f"{self.sec3_desc_jp} {_i} ~ {_i+1}  16 {self.std_df_b[self.std_df_b['F-XX-YYY'] == _fxxyyy]['ELEMENT_NAME'].values[0]} = {_fxxyyy}")
                tmp_list.append([_fxxyyy, self.std_df_b[self.std_df_b['F-XX-YYY'] == _fxxyyy].values[0], ilist[2], False])
              # elif (_fxxyyy[:1] == "1") & (_fxxyyy[-3:] == "000"):
              #   logging.debug(f"{self.sec3_desc_jp} {_i} ~ {_i+1}  16 Delayed replication of {int(_fxxyyy[2:4])} descriptor = {_fxxyyy}")
              #   tmp_list.append([_fxxyyy, f"Delayed replication of {int(_fxxyyy[2:4])} descriptor", ilist[2], False])
              elif (_fxxyyy[:1] == "1"):
                if (_fxxyyy[-3:] == "000"):
                  logging.debug(f"{self.sec3_desc_jp} {_i} ~ {_i+1}  16 Delayed replication of {int(_fxxyyy[2:4])} descriptor = {_fxxyyy}")
                  tmp_list.append([_fxxyyy, f"Delayed replication of {int(_fxxyyy[2:4])} descriptor", ilist[2], False])
                else:
                  logging.debug(f"{self.sec3_desc_jp} {_i} ~ {_i+1}  16 Replicate {int(_fxxyyy[2:4])} descriptors {int(_fxxyyy[5:8])} times = {_fxxyyy}")
                  tmp_list.append([_fxxyyy, f"Replicate {int(_fxxyyy[2:4])} descriptors {int(_fxxyyy[5:8])} times", ilist[2], False])
              elif _fxxyyy.startswith("2-06-"):
                logging.debug(f"{self.sec3_desc_jp} {_i} ~ {_i+1}  16 Local descriptor = {_fxxyyy}")
                std_flag = False
                tmp_list.append([_fxxyyy, f"Local descriptor", ilist[2], False])
              elif _fxxyyy.startswith("2-"):
                logging.debug(f"{self.sec3_desc_jp} {_i} ~ {_i+1}  16 Operate descriptor = {_fxxyyy}")
                tmp_list.append([_fxxyyy, f"Operate descriptor", ilist[2], False])
              elif _fxxyyy.startswith("3-"):
                # _f3_flag = True
                if _fxxyyy in self.std_table_d.keys():
                  logging.debug(f"{self.std_table_d[_fxxyyy]["MNEMONIC"]} {_i} ~ {_i+1}  16 {self.std_table_d[_fxxyyy]["NAME"]} = {_fxxyyy}")
                  tmp_list.append([_fxxyyy, self.std_table_d[_fxxyyy], ilist[2], False])
                else:
                  no_f3_info = True
              else:
                logging.debug(f"{self.sec3_desc_jp} {_i} ~ {_i+1}  16 {self.std_df_b[self.std_df_b['F-XX-YYY'] == _fxxyyy]['ELEMENT_NAME'].values} = {_fxxyyy}")
                tmp_list.append([_fxxyyy, f"NO INFOMATION VARIABLE", ilist[2], False])
            else:
              if len(self.loc_df_b_1[self.loc_df_b_1['F-XX-YYY'] == _fxxyyy]['ELEMENT_NAME'].values) == 1:
                logging.debug(f"{self.sec3_desc_jp} {_i} ~ {_i+1}  16 {self.loc_df_b_1[self.loc_df_b_1['F-XX-YYY'] == _fxxyyy]['ELEMENT_NAME'].values[0]} = {_fxxyyy}")
                tmp_list.append([_fxxyyy, self.loc_df_b_1[self.loc_df_b_1['F-XX-YYY'] == _fxxyyy].values[0], ilist[2], False])
              elif len(self.loc_df_b_2[self.loc_df_b_2['F-XX-YYY'] == _fxxyyy]['ELEMENT_NAME'].values) == 1:
                logging.debug(f"{self.sec3_desc_jp} {_i} ~ {_i+1}  16 {self.loc_df_b_2[self.loc_df_b_2['F-XX-YYY'] == _fxxyyy]['ELEMENT_NAME'].values[0]} = {_fxxyyy}")
                tmp_list.append([_fxxyyy, self.loc_df_b_2[self.loc_df_b_2['F-XX-YYY'] == _fxxyyy].values[0], ilist[2], False])
              elif _fxxyyy.startswith("3-"):
                # _f3_flag = True
                if _fxxyyy in self.loc_table_d_1.keys():
                  logging.debug(f"{self.loc_table_d_1[_fxxyyy]["MNEMONIC"]} {_i} ~ {_i+1}  16 {self.loc_table_d_1[_fxxyyy]["NAME"]} = {_fxxyyy}")
                  tmp_list.append([_fxxyyy, self.loc_table_d_1[_fxxyyy], ilist[2], False])
                else:
                  no_f3_info = True
              else:
                logging.debug(f"{self.sec3_desc_jp} {_i} ~ {_i+1}  16 {self.std_df_b[self.std_df_b['F-XX-YYY'] == _fxxyyy]['ELEMENT_NAME'].values} = {_fxxyyy}")
                tmp_list.append([_fxxyyy, f"NO INFOMATION VARIABLE", ilist[2], False])
              std_flag = True
            if no_f3_info == True:
              tmp_list.append([_fxxyyy, f"NO F=3 INFOMATION AVAILABLE", ilist[2], False])
              no_f3_info = False
      # Delete commentout in check descriptor
      # for i in tmp_list:
      #   print(i)
      # print("------------")
      # print()
      # 集約記述子が含まれていない場合、展開を終了
      if not _f3_flag:
        break
    # self.sec3_data_desc_extract_list = tmp_list
    # 遅延反復記述子確認フラグは以降使わないため削除
    self.sec3_data_desc_extract_list = [tmp[:3] for tmp in tmp_list]
    nest_idx = []
    for i in self.sec3_data_desc_extract_list:
      nest_idx.append(i[2])
      # print(*i)
    # ネストの深さを表示
    logging.debug(f"nest_idx = {nest_idx}")
    
    
    # 8オクテット目以降
    std_flag = True
    data_desc_str_extract_list = []
    for ilist in self.sec3_data_desc_extract_list:
      _fxxyyy = ilist[0]
      if highest_priority_add_tbl:
        if len(self.loc_df_b_2[self.loc_df_b_2['F-XX-YYY'] == _fxxyyy]['ELEMENT_NAME'].values) == 1:
          logging.debug(f"{self.sec3_desc_jp} {_i} ~ {_i+1}  16 {self.loc_df_b_2[self.loc_df_b_2['F-XX-YYY'] == _fxxyyy]['ELEMENT_NAME'].values[0]} = {_fxxyyy}")
          data_desc_str_extract_list.append(self.loc_df_b_2[self.loc_df_b_2['F-XX-YYY'] == _fxxyyy].to_string(header=None, index=None))
          continue
      if std_flag:
        if len(self.std_df_b[self.std_df_b['F-XX-YYY'] == _fxxyyy]['ELEMENT_NAME'].values) == 1:
          logging.debug(f"{self.sec3_desc_jp} {_i} ~ {_i+1}  16 {self.std_df_b[self.std_df_b['F-XX-YYY'] == _fxxyyy]['ELEMENT_NAME'].values[0]} = {_fxxyyy}")
          data_desc_str_extract_list.append(self.std_df_b[self.std_df_b['F-XX-YYY'] == _fxxyyy].to_string(header=None, index=None))
        elif (_fxxyyy[:1] == "1"):
          if (_fxxyyy[-3:] == "000"):
            logging.debug(f"{self.sec3_desc_jp} {_i} ~ {_i+1}  16 Delayed replication of {int(_fxxyyy[2:4])} descriptor = {_fxxyyy}")
            data_desc_str_extract_list.append(f" {_fxxyyy}  0  0  0  NONE  NONE   Delayed replication of {int(_fxxyyy[2:4])} descriptor")
          else:
            logging.debug(f"{self.sec3_desc_jp} {_i} ~ {_i+1}  16 Replicate {int(_fxxyyy[2:4])} descriptors {int(_fxxyyy[5:8])} times = {_fxxyyy}")
            data_desc_str_extract_list.append(f" {_fxxyyy}  0  0  0  NONE  NONE   Replicate {int(_fxxyyy[2:4])} descriptors {int(_fxxyyy[5:8])} times")
        elif _fxxyyy.startswith("2-06-"):
          logging.debug(f"{self.sec3_desc_jp} {_i} ~ {_i+1}  16 Local descriptor = {_fxxyyy}")
          std_flag = False
          data_desc_str_extract_list.append(f" {_fxxyyy}  0  0  0  NONE  NONE   Local descriptor")
        elif _fxxyyy.startswith("2-"):
          logging.debug(f"{self.sec3_desc_jp} {_i} ~ {_i+1}  16 Operate descriptor = {_fxxyyy}")
          data_desc_str_extract_list.append(f" {_fxxyyy}  0  0  0  NONE  NONE   Operate descriptor")
        else:
          logging.debug(f"{self.sec3_desc_jp} {_i} ~ {_i+1}  16 {self.std_df_b[self.std_df_b['F-XX-YYY'] == _fxxyyy]['ELEMENT_NAME'].values} = {_fxxyyy}")
          data_desc_str_extract_list.append(f" {_fxxyyy}  0  0  0  NONE  NONE   NO INFOMATION VARIABLE")
      else:
        if len(self.loc_df_b_1[self.loc_df_b_1['F-XX-YYY'] == _fxxyyy]['ELEMENT_NAME'].values) == 1:
          logging.debug(f"{self.sec3_desc_jp} {_i} ~ {_i+1}  16 {self.loc_df_b_1[self.loc_df_b_1['F-XX-YYY'] == _fxxyyy]['ELEMENT_NAME'].values[0]} = {_fxxyyy}")
          data_desc_str_extract_list.append(self.loc_df_b_1[self.loc_df_b_1['F-XX-YYY'] == _fxxyyy].to_string(header=None, index=None))
        elif len(self.loc_df_b_2[self.loc_df_b_2['F-XX-YYY'] == _fxxyyy]['ELEMENT_NAME'].values) == 1:
          logging.debug(f"{self.sec3_desc_jp} {_i} ~ {_i+1}  16 {self.loc_df_b_2[self.loc_df_b_2['F-XX-YYY'] == _fxxyyy]['ELEMENT_NAME'].values[0]} = {_fxxyyy}")
          data_desc_str_extract_list.append(self.loc_df_b_2[self.loc_df_b_2['F-XX-YYY'] == _fxxyyy].to_string(header=None, index=None))
        else:
          logging.debug(f"{self.sec3_desc_jp} {_i} ~ {_i+1}  16 {self.std_df_b[self.std_df_b['F-XX-YYY'] == _fxxyyy]['ELEMENT_NAME'].values} = {_fxxyyy}")
          data_desc_list.append([_fxxyyy, f"NO INFOMATION VARIABLE"])
          data_desc_str_extract_list.append(f" {_fxxyyy}  0  0  0  NONE  NONE   NO INFOMATION VARIABLE",)
        std_flag = True
    self.sec3_data_desc_str_extract_list = data_desc_str_extract_list


class bufr_sec_4:
  def __init__(self, binary: bytes, sec_len: str) -> None:
    """read bufr Data section (section 4)<br>
    BUFRの資料節(第4節)を読み込むクラス

    Parameters
    ----------
    binary : bytes
        binary data of BUFR<br>
        BUFRのバイナリデータ
    sec_len : dict
        length of sections<br>
        セクションの長さ
    """
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
    
  def read_data(self, descriptors: list, sec_len: dict, nsubset: list) -> list:
    """read bufr data<br>
    BUFRのデータを読み込む

    Parameters
    ----------
    descriptors : list
        data descriptor<br>
        資料記述子
    sec_len : dict
        length of sections<br>
        セクションの長さ
    nsubset : list
        number of data subset<br>
        データサブセットの数

    Returns
    -------
    data
        data
    """
    raw_data = format(int.from_bytes(self.sec4_binary, "big"), f"0{sec_len['sec4']*8}b")
    raw_data = format(int.from_bytes(self.sec4_binary, "big"), f"{sec_len['sec4']*8}b")
    # print(raw_data[-70:])
    self.data_class = data_constructor(descriptors, raw_data, sec_len, nsubset)
    return self.data_class.get_data()


class bufr_sec_5:
  def __init__(self, binary: bytes, sec_len: dict) -> None:
    """read bufr End section (section 5)<br>
    BUFRの終端節(第5節)を読み込むクラス

    Parameters
    ----------
    binary : bytes
        binary data of BUFR<br>
        BUFRのバイナリデータ
    sec_len : dict
        length of sections<br>
        セクションの長さ

    Raises
    ------
    UnexpectedBufrError
        raise when end of file is not "7777".<br>
        ファイルの終端が"7777"でない場合に発生
    """
    # Section 5, End section
    self.sec5_desc_en = "Section 5, End section"
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
  def __init__(self, descriptors: list, raw_data: str, sec_len: dict, nsubset: int) -> None:
    """read data section (section 4)<br>
    資料節(第4節)を読むクラス

    Parameters
    ----------
    descriptors : list
        data descriptor<br>
        資料記述子
    raw_data : str
        0/1 string data<br>
        0/1の文字列のデータ
    sec_len : dict
        length of sections<br>
        セクションの長さ
    nsubset : int
        number of subset<br>
        サブセットの数

    Raises
    ------
    UnexpectedBufrError
        raise when did not reach end of data section (section 4)<br>
        データを最後まで読み込めなかった場合に発生
    """
    self.descriptors = descriptors
    self.raw_data = raw_data
    self.irec = 32
    self.local_flag = False
    self.sec4_len = sec_len["sec4"]
    self.nsubset = nsubset
    self.operators = []
    
    self.data = []
    for _ in range(self.nsubset):
      self.data.append(self._read_data_from_str_bin())
      # if _ < 2:
      #   print(self.data[len(self.data)-1])
      #   print(f"---- {_}th subset end ----")
    
    # print(self.sec4_len, self.sec4_len*8)
    # print(self.irec)
    logging.debug(f"self.sec4_len = {self.sec4_len}, self.sec4_len*8 = {self.sec4_len*8}, self.irec = {self.irec}")
    # BUFR3の名残で、偶数オクテットに揃えているデータがある可能性を考慮し、正常読込完了にはゆとりを持たせる
    if (self.sec4_len*8-16 < self.irec) & (self.irec <= self.sec4_len*8):
      logging.debug('正常にデータを読み込みました')
    else:
      logging.error('データ読込が途中で終了しました。self.data[:3]までprintします。')
      for idata in self.data[:3]:
        print(idata)
      raise UnexpectedBufrError('データ読込が途中で終了しました')
  
  def _read_data_from_str_bin(self, idx: int=0, nest: int=0) -> list:
    """read data from 0/1 string<br>
    0/1の文字列からデータを読み込む

    Parameters
    ----------
    idx : int, optional
        descriptor of index, by default 0<br>
        資料記述子のインデックス
    nest : int, optional
        nest level, by default 0<br>
        ネストの階層

    Returns
    -------
    list
        data of a nest level depth<br>
        あるネストの階層に属するデータ

    Raises
    ------
    UnexpectedBufrError
        raise when encountered unknown data descriptor<br>
        予期せぬ資料記述子があった場合に発生
    """
    _data = []
    logging.debug(f'idx = {idx}, nest = {nest}', stack_info=False)
    for jdx, (fxxyyy, descriptor, inest) in enumerate(self.descriptors[idx:]):
      # logging.debug(f"{descriptor}", stack_info=False)
      # logging.info(f"jdx = {jdx}, descriptor = {descriptor}, inest = {inest}", stack_info=False)
      # logging.info(f"inest = {inest}", stack_info=False)
      if nest == inest:
        # 0: 要素記述子, 1: 反復記述子, 2: 操作記述子, 3: 集約記述子
        # 0: F-XX-YYY, 1: SCALE, 2: REFERENCE VALUE, 3: BIT WIDTH
        # 4: UNIT, 5: MNEMONIC, 6: DESC CODE, 7: ELEMENT NAME
        if type(descriptor) == str:
          if descriptor.startswith("Delayed replication of"):
            _data.append(None)
          elif descriptor.startswith("Replicate"): # F-XX-YYY = 1-XX-YYY, YYY != 000
            logging.debug(f"{jdx} {descriptor}", stack_info=False)
            _data.append(None)
            _loop_data = []
            _, _, nloop = fxxyyy.split("-")
            for iloop in range(int(nloop)):
              if nest == 0:
                logging.debug(f'idx = {idx}, nest = {nest}, irec = {self.irec}', stack_info=False)
              logging.debug(f"iloop = {iloop}", stack_info=False)
              logging.debug(f"       nest = {nest}", stack_info=False)
              _loop_data.append(self._read_data_from_str_bin(idx=idx+jdx+1, nest=nest+1))
            _data.append(_loop_data)
          elif descriptor.startswith("Local descriptor"):
            logging.debug(descriptor, stack_info=False)
            self.local_flag = True
            _data.append(None)
          elif descriptor.startswith("Operate descriptor"):
            logging.debug(descriptor, stack_info=False)
            _data.append(None)
            pattern = r"^2-0[1-57]-\d{3}" # F-XX-YYY
            pattern_000 = r"^2-0[1-57]-000" # F-XX-000
            if re.match(pattern, fxxyyy):
              if re.match(pattern_000, fxxyyy):
                for ope in self.operators:
                  if ope.startswith(fxxyyy[0:5]):
                    self.operators.remove(ope)
                    break
              else:
                self.operators.append(fxxyyy)
            else:
              logging.info(descriptor)
              raise UnexpectedBufrError(f"Encountered a supported descriptor.")
          else:
            logging.info(descriptor)
            raise UnexpectedBufrError(f"Encountered a supported descriptor.")
        else:
          # TODO:データ読み込み処理
          # CCITT IA5, Code table, Flag table, other(Numeric, m, Hz, etc) に分類して処理
          # 0-31-000, 0-31-001, 0-31-002については空リストを作成し、appendしていく形に
          if fxxyyy in ("0-31-000", "0-31-001", "0-31-002"):
            # logging.info(f'{self.raw_data[self.irec:self.irec+int(descriptor[3])]}', stack_info=False)
            nloop = int(self.raw_data[self.irec:self.irec+int(descriptor[3])], 2)
            # TODO: this can be bug
            # nloop = 0 if nloop == 255 else nloop
            self.irec += int(descriptor[3])
            # print(nloop)
            _data.append(nloop)
            _loop_data = []
            # logging.info(f'idx = {jdx}, nloop = {nloop}, {self.raw_data[self.irec-int(descriptor[3]):self.irec]}', stack_info=False)
            for iloop in range(nloop):
              if nest == 0:
                logging.debug(f'idx = {idx}, nest = {nest}, irec = {self.irec}', stack_info=False)
              logging.debug(f"iloop = {iloop}", stack_info=False)
              logging.debug(f"       nest = {nest}", stack_info=False)
              _loop_data.append(self._read_data_from_str_bin(idx=idx+jdx+1, nest=nest+1))
            _data.append(_loop_data)
            # logging.info(f"add _data.append({_loop_data})")
          elif descriptor[4] == "CCITT IA5":
            text = ""
            # 8ビットずつに分割
            text_bin_list = [self.raw_data[self.irec+i:self.irec+i+8] for i in range(0,int(descriptor[3]),8)]
            for text_bin in text_bin_list:
              decimal = int(text_bin, 2)
              if decimal in convert_decimal_to_IA5character.keys():
                text += convert_decimal_to_IA5character[decimal]
              else:
                text += "?"
            _data.append(text)
            self.irec += int(descriptor[3])
          elif descriptor[4] == "Flag table":
            _data.append(self.raw_data[self.irec:self.irec+int(descriptor[3])])
            self.irec += int(descriptor[3])
          elif descriptor[4] == "Code table":
            # logging.info(descriptor)
            # logging.info(self.raw_data[self.irec:self.irec+int(descriptor[3])])
            _data.append((int(self.raw_data[self.irec:self.irec+int(descriptor[3])], 2)+int(descriptor[2]))/10**int(descriptor[1]))
            self.irec += int(descriptor[3])
          else:
            # logging.info(f"fxxyyy, descriptor, inest = {fxxyyy}, {descriptor}, {inest}")
            # if descriptor[0] == "0-11-001":
              # logging.info(f"self.raw_data[self.irec:self.irec+int(descriptor[3]) = {self.raw_data[self.irec:self.irec+int(descriptor[3])]}")
              # logging.info(f"self.irec = {self.irec}")
            # 0: F-XX-YYY, 1: SCALE, 2: REFERENCE VALUE, 3: BIT WIDTH
            # 4: UNIT, 5: MNEMONIC, 6: DESC CODE, 7: ELEMENT NAME
            if len(self.operators) > 0:
              for ope in self.operators:
                if ope.startswith("2-01-"):
                  _data.append((int(self.raw_data[self.irec:self.irec+int(descriptor[3])+(int(ope[5:8])-128)], 2)+int(descriptor[2]))/10**int(descriptor[1]))
                  self.irec += int(descriptor[3])+int(ope[5:8])-128
                elif ope.startswith("2-02-"):
                  _data.append((int(self.raw_data[self.irec:self.irec+int(descriptor[3])], 2)+int(descriptor[2]))/10**(int(descriptor[1])+int(ope[5:8])-128))
                  self.irec += int(descriptor[3])
                elif ope.startswith("2-03-"):
                  # NOT SUPPORTED
                  pass
                elif ope.startswith("2-04-"):
                  # NOT SUPPORTED
                  pass
                elif ope.startswith("2-05-"):
                  text = ""
                  # 8ビットずつに分割
                  text_bin_list = [self.raw_data[self.irec+i:self.irec+i+8] for i in range(0,int(ope[5:8]),8)]
                  for text_bin in text_bin_list:
                    decimal = int(text_bin, 2)
                    if decimal in convert_decimal_to_IA5character.keys():
                      text += convert_decimal_to_IA5character[decimal]
                    else:
                      text += "?"
                  _data.append(text)
                  self.irec += int(ope[5:8])
                elif ope.startswith("2-07-"):
                  # logging.info(f"{ope}")
                  add_width = (10*int(ope[5:8])+2)//3
                  _data.append((int(self.raw_data[self.irec:self.irec+int(descriptor[3])+add_width], 2)+int(descriptor[2])*10**int(ope[5:8]))/10**(int(descriptor[1])+int(ope[5:8])))
                  self.irec += int(descriptor[3])+add_width
            else:
              # logging.info(f"{ope} {descriptor}")
              _data.append((int(self.raw_data[self.irec:self.irec+int(descriptor[3])], 2)+int(descriptor[2]))/10**int(descriptor[1]))
              self.irec += int(descriptor[3])
        logging.debug(f"self.irec = {self.irec}")
      else:
        # logging.info(f'idx = {idx}, jdx = {jdx}, fxxyyy = {fxxyyy}, nest = {nest}, inest = {inest}, irec = {self.irec}', stack_info=False)
        # 子ネストの場合、ループを抜ける
        if nest != 0:
          break
    return _data
  
  def get_data(self):
    return self.data

def _int_into_fxxyyy(num: int) -> str:
  bits = format(num, "016b")
  return f"{int(bits[-16:-14], 2)}-{int(bits[-14:-8], 2):02}-{int(bits[-8:], 2):03}"

if __name__=='__main__':
  # bufr_class = bufr(os.path.join(os.path.dirname(__file__), f"../../tests/data/bufr/bufr/IUPC41_RJTD_010000_202406010016132_001.send")) # ウィンドプロファイラ
  # bufr_class = bufr(os.path.join(os.path.dirname(__file__), f"../../tests/data/bufr/bufr/IUKC65_2018053109_bufr4_noheader.bin")) # 高分解能地上高層実況気象報
  # bufr_class = bufr(os.path.join(os.path.dirname(__file__), f"../../tests/data/bufr/bufr/ISCC01_RJTD_200000_202410200000311_001.send")) # CLIMAT
  # bufr_class = bufr(os.path.join(os.path.dirname(__file__), f"../../tests/data/bufr/bufr/IUKC80_RJTD_011200_202410011245310_001.send")) # 高分解能海上高層実況気象報
  bufr_class = bufr(os.path.join(os.path.dirname(__file__), f"../../tests/data/bufr/bufr/Z__C_RJTD_20241030000000_OBS_AMDS_Rjp_N1_bufr4.bin"), highest_priority_add_tbl=True)
  # bufr_class = bufr(os.path.join(os.path.dirname(__file__), f"../../tests/data/bufr/bufr/IUCC10_RJTD_300000_202410300004300_001_68680.send")) # 東京編集の気象衛星資料解析気象報
  # bufr_class = bufr(os.path.join(os.path.dirname(__file__), f"../../tests/data/bufr/bufr/IUKL01_RJTD_300000_202410300123114_001.send")) # 東京編集の地上高層実況気象報
  # bufr_class = bufr(os.path.join(os.path.dirname(__file__), f"../../tests/data/bufr/bufr/ISIC01_RJTD_300300_202410300319110_001.send")) # 東京編集の地上気象実況報（03,09,15,21UTC）(SYNOP)
  # bufr_class = bufr(os.path.join(os.path.dirname(__file__), f"../../tests/data/bufr/bufr/ISMC01_RJTD_300600_202410300619110_001.send")) # 東京編集の地上気象実況報（00,06,12,18UTC）(SYNOP)
  # bufr_class = bufr(os.path.join(os.path.dirname(__file__), f"../../tests/data/bufr/bufr/IUKN01_BABJ_300000_202410300231070_001.send")) # 北京編集の地上高層風実況気象報Ａ部 (PILOT)
  print("Data description:")
  for iv in bufr_class.get_data_description():
  # for iv in bufr_class.get_data_descriptors():
    print(iv)
  print()
  print("Extracted Data description:")
  for idx, iv in enumerate(bufr_class.get_extracted_data_description()):
  # for idx, iv in enumerate(bufr_class.get_extracted_data_descriptors()):
    print(f"{idx} {iv}")
  print()
  
  data = bufr_class.read_data()
  # print(data)