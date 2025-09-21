# Copyright (c) 2024, NakaMetPy Develoers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# Command Example1: python -m unittest tests/test_bufr.py -v
# Command Example2: python -m unittest tests.test_bufr -v
# Command Example3: python -m unittest tests.test_bufr.UtilTest.test_parse_tableB_into_dataframe_001 -v
# 
import unittest
from src.nakametpy.bufr import parse_tableB_into_dataframe, parse_tableD_into_dict,\
                        parse_codeFlag_into_dict, bufr
from src.nakametpy._error import MayNotBeAbleToReadBufrWarning
import os
import pandas as pd
import numpy as np

class UtilTest(unittest.TestCase):
  def test_parse_tableB_into_dataframe_001(self):
    """
    test case: test_parse_tableB_into_dataframe_001
    
    Method
    --------
      parse_tableB_into_dataframe
    Parameters
    --------
      version: `str`
    Notes
    --------
      `version`の指定なし
    """
    # print(self.test_parse_tableB_into_dataframe_001.__doc__)
    actual = parse_tableB_into_dataframe()
    actual_value = actual[actual["F-XX-YYY"] == "0-00-004"]["MNEMONIC"].values
    self.assertEqual(actual_value, "MTABL")
  
  def test_parse_tableB_into_dataframe_002(self):
    """
    test case: test_parse_tableB_into_dataframe_002
    
    Method
    --------
      parse_tableB_into_dataframe
    Parameters
    --------
      version: `str`
    Notes
    --------
      `version`の指定あり
    """
    # print(self.test_parse_tableB_into_dataframe_002.__doc__)
    for version, fxxyyy, expected in (("LOC_0_7_1", "0-01-195", "SACO"),
                                      ("STD_0_42", "0-01-024", "WSPDS")):
        with self.subTest(version=version, fxxyyy=fxxyyy, expected=expected):
          actual = parse_tableB_into_dataframe(version)
          # print(actual[actual["F-XX-YYY"] == fxxyyy])
          actual_value = actual[actual["F-XX-YYY"] == fxxyyy]["MNEMONIC"].values
          self.assertEqual(actual_value, expected)
  
  def test_parse_tableD_into_dict_001(self):
    """
    test case: test_parse_tableD_into_dict_001
    
    Method
    --------
      parse_tableD_into_dict
    Parameters
    --------
      version: `str`
    Notes
    --------
      `version`の指定なし
    """
    # print(self.test_parse_tableD_into_dict_001.__doc__)
    actual = parse_tableD_into_dict()
    self.assertEqual(actual["3-01-036"]["MNEMONIC"], "SHIPSEQ1")
    self.assertEqual(actual["3-01-036"]["NAME"], "Ship")
    self.assertEqual(actual["3-01-036"]["SEQUENCE"][2]["FXXYYY"], "3-01-011")
    self.assertEqual(actual["3-01-036"]["SEQUENCE"][2]["NAME"], "Year, month, day")

  def test_parse_tableD_into_dict_002(self):
    """
    test case: test_parse_tableD_into_dict_002
    
    Method
    --------
      parse_tableD_into_dict
    Parameters
    --------
      version: `str`
    Notes
    --------
      `version`の指定あり
    """
    # print(self.test_parse_tableD_into_dict_002.__doc__)
    for version, fxxyyy1, mnemonic, name1, fxxyyy2, name2 in (
      ("LOC_0_7_1", "3-52-003", "RCPTIM", "Report receipt time data", "0-04-204", "Receipt minute"),
      ("STD_0_30", "3-16-007", "FRONTSEQ", "Front", "0-31-001", "Delayed descriptor replication factor")):
      with self.subTest(version=version, fxxyyy1=fxxyyy1, mnemonic=mnemonic,
                        name1=name1, fxxyyy2=fxxyyy2, name2=name2):
        actual = parse_tableD_into_dict(version)
        self.assertEqual(actual[fxxyyy1]["MNEMONIC"], mnemonic)
        self.assertEqual(actual[fxxyyy1]["NAME"], name1)
        self.assertEqual(actual[fxxyyy1]["SEQUENCE"][5]["FXXYYY"], fxxyyy2)
        self.assertEqual(actual[fxxyyy1]["SEQUENCE"][5]["NAME"], name2)
  
  def test_parse_codeFlag_into_dict_001(self):
    """
    test case: test_parse_codeFlag_into_dict_001
    
    Method
    --------
      parse_codeFlag_into_dict
    Parameters
    --------
      version: `str`
    Notes
    --------
      `version`の指定なし
    """
    # print(self.test_parse_codeFlag_into_dict_001.__doc__)
    actual = parse_codeFlag_into_dict()
    # CODE, No dependency
    self.assertEqual(actual["0-01-007"]["MNEMONIC"], "SAID")
    self.assertEqual(actual["0-01-007"]["CODEFLAG"], "CODE")
    self.assertEqual(actual["0-01-007"]["HAS_DEPENDENCY"], False)
    self.assertEqual(actual["0-01-007"]["VALBITS"]["122"], "GCOM-W1")
    # FLAG, No dependency
    self.assertEqual(actual["0-02-002"]["MNEMONIC"], "TIWM")
    self.assertEqual(actual["0-02-002"]["CODEFLAG"], "FLAG")
    self.assertEqual(actual["0-02-002"]["HAS_DEPENDENCY"], False)
    self.assertEqual(actual["0-02-002"]["VALBITS"]["3"], "Originally measured in km h**-1")
    # CODE, has dependency
    self.assertEqual(actual["0-01-034"]["MNEMONIC"], "GSES")
    self.assertEqual(actual["0-01-034"]["CODEFLAG"], "CODE")
    self.assertEqual(actual["0-01-034"]["HAS_DEPENDENCY"], True)
    self.assertEqual(len(actual["0-01-034"]["VALBITS"].keys()), 3)
    self.assertEqual(len(actual["0-01-034"]["VALBITS"]["0-01-031"]["34"].keys()), 4)
    self.assertEqual(actual["0-01-034"]["VALBITS"]["0-01-031"]["34"]["240"], "Kiyose")
    self.assertEqual(actual["0-01-034"]["VALBITS"]["0-01-035"]["46"]["0"], "No sub-centre")
  
  def test_parse_codeFlag_into_dict_002(self):
    """
    test case: test_parse_codeFlag_into_dict_002
    
    Method
    --------
      parse_codeFlag_into_dict
    Parameters
    --------
      version: `str`
    Notes
    --------
      `version`の指定なし
    """
    # print(self.test_parse_codeFlag_into_dict_002.__doc__)
    actual = parse_codeFlag_into_dict("LOC_0_7_1")
    # CODE, No dependency
    self.assertEqual(actual["0-02-194"]["MNEMONIC"], "AUTO")
    self.assertEqual(actual["0-02-194"]["CODEFLAG"], "CODE")
    self.assertEqual(actual["0-02-194"]["HAS_DEPENDENCY"], False)
    self.assertEqual(actual["0-02-194"]["VALBITS"]["3"], "METAR/SPECI report with 'A01' found in report, but 'AUTO' not found in report")
    # FLAG, No dependency
    self.assertEqual(actual["0-33-200"]["MNEMONIC"], "WSEQC1")
    self.assertEqual(actual["0-33-200"]["CODEFLAG"], "FLAG")
    self.assertEqual(actual["0-33-200"]["HAS_DEPENDENCY"], False)
    self.assertEqual(actual["0-33-200"]["VALBITS"]["26"], "Rain flag based on TBs (or from SDR processor)")
    # CODE, has dependency
    self.assertEqual(actual["0-07-246"]["MNEMONIC"], "PQM")
    self.assertEqual(actual["0-07-246"]["CODEFLAG"], "CODE")
    self.assertEqual(actual["0-07-246"]["HAS_DEPENDENCY"], True)
    self.assertEqual(len(actual["0-07-246"]["VALBITS"].keys()), 1)
    self.assertEqual(len(actual["0-07-246"]["VALBITS"]["0-07-247"]["1"].keys()), 9)
    self.assertEqual(actual["0-07-246"]["VALBITS"]["0-07-247"]["1"]["15"], "Observation is flagged for non-use by analysis")
    self.assertEqual(actual["0-07-246"]["VALBITS"]["0-07-247"]["14"]["1"], "Good")
    
  def test_bufr_001(self):
    """
    Test for `Wind profiler`(BUFR)/`ウィンドプロファイラ`<br>
    Specification: 13601<br>
    Tech Info: 97,532<br>
    
    Class
    --------
      bufr
    Parameters
    --------
      file_path: `str`
    """
    # print(self.test_bufr_001.__doc__)
    for file_path in ("./data/bufr/bufr/IUPC41_RJTD_010000_202406010016132_001.send", # ウィンドプロファイラ
                      "./data/bufr/bufr/Z__C_RJTD_20200707000000_WPR_SEQ_RS-all_Pww_bufr4.bin", # ウィンドプロファイラ, ヘッダなし
                      ):
      with self.subTest(file_path=file_path):
        bufr_class = bufr(os.path.join(os.path.dirname(__file__), file_path))
        bufr_class.read_data()
    
  def test_bufr_002(self):
    """
    Test for `TEMP`(BUFR)/`高分解能地上高層実況気象報`<br>
    Specification: ----<br>
    Tech Info: 334,478<br>
    
    Class
    --------
      bufr
    Parameters
    --------
      file_path: `str`
    """
    # print(self.test_bufr_002.__doc__)
    for file_path in ("./data/bufr/bufr/IUKC65_2018053109_bufr4_noheader.bin", # 高分解能地上高層実況気象報, 100hPaまで
                      "./data/bufr/bufr/IUKC71_2018053109_bufr4_noheader.bin", # 高分解能地上高層実況気象報, 観測終了まで
                      "./data/bufr/bufr/IUSC65_2018053109_bufr4_noheader.bin", # 高分解能地上高層実況気象報, 100hPaまで
                      "./data/bufr/bufr/IUSC71_2018053109_bufr4_noheader.bin", # 高分解能地上高層実況気象報, 観測終了まで
                      ):
      with self.subTest(file_path=file_path):
        bufr_class = bufr(os.path.join(os.path.dirname(__file__), file_path))
        bufr_class.read_data()
    
  def test_bufr_003(self):
    """
    Test for `TEMP SHIP`(BUFR)/`高分解能海上高層実況気象報`<br>
    Specification: 30103<br>
    Tech Info: 618<br>
    
    Class
    --------
      bufr
    Parameters
    --------
      file_path: `str`
    """
    # print(self.test_bufr_003.__doc__)
    for file_path in ("./data/bufr/bufr/IUKC80_RJTD_011200_202410011245310_001.send", # 高分解能海上高層実況気象報, 100hPaまで, 凌風丸
                      "./data/bufr/bufr/IUKC81_RJTD_051200_202410051245312_001.send", # 高分解能海上高層実況気象報, 100hPaまで, 啓風丸
                      "./data/bufr/bufr/IUSC80_RJTD_011200_202410011345300_001.send", # 高分解能海上高層実況気象報, 観測終了まで, 凌風丸
                      "./data/bufr/bufr/IUSC81_RJTD_051200_202410051330311_001.send", # 高分解能海上高層実況気象報, 観測終了まで, 啓風丸
                      ):
      with self.subTest(file_path=file_path):
        bufr_class = bufr(os.path.join(os.path.dirname(__file__), file_path))
        bufr_class.read_data()
    
  def test_bufr_004(self):
    """
    Test for `CLIMAT`(BUFR)/`地上月気候統計値`<br>
    Specification: ----<br>
    Tech Info: 334<br>
    
    Class
    --------
      bufr
    Parameters
    --------
      file_path: `str`
    """
    # print(self.test_bufr_004.__doc__)
    for file_path in ("./data/bufr/bufr/ISCA01_LEMM_050000_202410051001020_001.send", # CLIMAT
                      "./data/bufr/bufr/ISCC01_RJTD_200000_202410200000311_001.send", # 東京編集の地上月気候統計値(CLIMAT)
                      ):
      with self.subTest(file_path=file_path):
        bufr_class = bufr(os.path.join(os.path.dirname(__file__), file_path))
        bufr_class.read_data()
    
  def test_bufr_005(self):
    """
    Test for `SAREP`(BUFR)/`気象衛星資料解析気象報`<br>
    Specification: 11905<br>
    Tech Info: 334<br>
    
    Class
    --------
      bufr
    Parameters
    --------
      file_path: `str`
    """
    # print(self.test_bufr_005.__doc__)
    for file_path in ("./data/bufr/bufr/IUCC10_RJTD_300000_202410300004300_001_68680.send", # 東京編集の気象衛星資料解析気象報★
                      ):
      with self.subTest(file_path=file_path):
        bufr_class = bufr(os.path.join(os.path.dirname(__file__), file_path))
        bufr_class.read_data()
    
  def test_bufr_006(self):
    """
    Test for `TEMP`(BUFR)/`地上高層実況気象報`<br>
    Specification: ----<br>
    Tech Info: 334<br>
    
    Class
    --------
      bufr
    Parameters
    --------
      file_path: `str`
    """
    # print(self.test_bufr_006.__doc__)
    for file_path in ("./data/bufr/bufr/IUKL01_RJTD_300000_202410300123114_001.send", # 東京編集の地上高層実況気象報
                      "./data/bufr/bufr/IUSC01_RJTD_300000_202410300123111_001.send", # 東京編集の地上高層実況気象報Ａ部
                      "./data/bufr/bufr/IUSC02_RJTD_300000_202410300123112_001.send", # 東京編集の地上高層実況気象報Ａ部
                      "./data/bufr/bufr/IUSC02_RJTD_300000_CCA_202410300157101_001.send", # 東京編集の地上高層実況気象報Ａ部 訂正報
                      "./data/bufr/bufr/IUSC03_RJTD_300000_202410300123113_001.send", # 東京編集の地上高層実況気象報Ａ部★
                      "./data/bufr/bufr/IUSC04_RJTD_300000_202410300125110_001.send", # 東京編集の地上高層実況気象報Ｂ部
                      "./data/bufr/bufr/IUSC04_RJTD_300000_CCA_202410300324110_001.send", # 東京編集の地上高層実況気象報Ｂ部 訂正報
                      "./data/bufr/bufr/IUSC05_RJTD_300000_202410300125120_001.send", # 東京編集の地上高層実況気象報Ｂ部
                      "./data/bufr/bufr/IUSC05_RJTD_300000_CCA_202410300324111_001.send", # 東京編集の地上高層実況気象報Ｂ部 訂正報
                      "./data/bufr/bufr/IUSC06_RJTD_300000_202410300125121_001.send", # 東京編集の地上高層実況気象報Ｂ部
                      "./data/bufr/bufr/IUSC06_RJTD_300000_CCA_202410300324112_001.send", # 東京編集の地上高層実況気象報Ｂ部 訂正報
                      "./data/bufr/bufr/IUSC07_RJTD_300000_202410300203111_001.send", # 東京編集の地上高層実況気象報Ｃ部
                      "./data/bufr/bufr/IUSC08_RJTD_300000_202410300203112_001.send", # 東京編集の地上高層実況気象報Ｃ部
                      "./data/bufr/bufr/IUSC09_RJTD_300000_202410300203113_001.send", # 東京編集の地上高層実況気象報Ｃ部
                      "./data/bufr/bufr/IUSC10_RJTD_300000_202410300212111_001.send", # 東京編集の地上高層実況気象Ｄ部
                      "./data/bufr/bufr/IUSC10_RJTD_300000_CCA_202410300405102_001.send", # 東京編集の地上高層実況気象Ｄ部 訂正報
                      "./data/bufr/bufr/IUSC11_RJTD_300000_202410300212112_001.send", # 東京編集の地上高層実況気象Ｄ部
                      "./data/bufr/bufr/IUSC12_RJTD_300000_202410300212113_001.send", # 東京編集の地上高層実況気象Ｄ部
                      ):
      with self.subTest(file_path=file_path):
        bufr_class = bufr(os.path.join(os.path.dirname(__file__), file_path))
        bufr_class.read_data()
    
  def test_bufr_007(self):
    """
    Test for `SYNOP`(BUFR)/`地上気象実況報`<br>
    Specification: 13401<br>
    Tech Info: 334,595<br>
    
    Class
    --------
      bufr
    Parameters
    --------
      file_path: `str`
    """
    # print(self.test_bufr_007.__doc__)
    for file_path in ("./data/bufr/bufr/ISIC01_RJTD_300300_202410300319110_001.send", # 東京編集の地上気象実況報（03,09,15,21UTC）
                      "./data/bufr/bufr/ISMC01_RJTD_300600_202410300619110_001.send", # 東京編集の地上気象実況報（00,06,12,18UTC）(SYNOP)
                      ):
      with self.subTest(file_path=file_path):
        bufr_class = bufr(os.path.join(os.path.dirname(__file__), file_path))
        bufr_class.read_data()
    
  def test_bufr_008(self):
    """
    Test for `PILOT`(BUFR)/`地上高層風実況気象報`<br>
    Specification: ----<br>
    Tech Info: 334<br>
    
    Class
    --------
      bufr
    Parameters
    --------
      file_path: `str`
    """
    # print(self.test_bufr_008.__doc__)
    import warnings
    with warnings.catch_warnings():
      # このテストは以下の警告が出るため、無視する
      # この関数ではこのファイルを正しく読むことが出来ないかもしれません.理由：第1節の長さが22ではなく、23
      warnings.filterwarnings("ignore", category=MayNotBeAbleToReadBufrWarning)
      for file_path in ("./data/bufr/bufr/IUWG01_WIIX_300600_202410300617189_001.send", # メルボルン編集の地上高層風実況気象報 (PILOT)
                        "./data/bufr/bufr/IUKN01_BABJ_300000_202410300231070_001.send", # 北京編集の地上高層風実況気象報Ａ部 (PILOT) 
                        ):
        with self.subTest(file_path=file_path):
          bufr_class = bufr(os.path.join(os.path.dirname(__file__), file_path))
          bufr_class.read_data()
    
  def test_bufr_009(self):
    """
    Test for `AMEDAS`(BUFR)/`地域気象観測(アメダス)`<br>
    Specification: 13301,13401<br>
    Tech Info: 273,595,623<br>
    
    Class
    --------
      bufr
    Parameters
    --------
      file_path: `str`
    """
    # print(self.test_bufr_009.__doc__)
    for file_path in ("./data/bufr/bufr/Z__C_RJTD_20241030000000_OBS_AMDS_Rjp_N1_bufr4.bin", # アメダス N1
                      "./data/bufr/bufr/Z__C_RJTD_20241030000000_OBS_AMDS_Rjp_N2_bufr4.bin", # アメダス N2
                      "./data/bufr/bufr/Z__C_RJTD_20241030010000_OBS_AMDSRR_Rjp_N1_bufr4.bin", # アメダス N1 遅延
                      ):
      with self.subTest(file_path=file_path):
        bufr_class = bufr(os.path.join(os.path.dirname(__file__), file_path), True)
        bufr_class.read_data()
    
  def test_bufr_010(self):
    """
    Test for `Tide`(BUFR)/`潮位観測報`<br>
    Specification: 30803<br>
    Tech Info: 551<br>
    
    Class
    --------
      bufr
    Parameters
    --------
      file_path: `str`
    """
    # print(self.test_bufr_009.__doc__)
    for file_path in ("./data/bufr/bufr/ISTC81_RJTD_282350.dat", # 潮位観測報 東日本
                      "./data/bufr/bufr/ISTC82_RJTD_282350.dat", # 潮位観測報 西日本
                      ):
      with self.subTest(file_path=file_path):
        bufr_class = bufr(os.path.join(os.path.dirname(__file__), file_path), True)
        bufr_class.read_data()
    
  def test_bufr_011(self):
    """
    Test for `SYNOP`(BUFR)/`地上気象実況報`<br>
    Specification: 13401<br>
    Tech Info: 595,637<br>
    
    Class
    --------
      bufr
    Parameters
    --------
      file_path: `str`
    """
    # print(self.test_bufr_007.__doc__)
    for file_path in ("./data/bufr/bufr/ISIC11_RJTD_090900_26830.bin", # 地上気象実況報（03,09,15,21UTC）
                      "./data/bufr/bufr/ISMC11_RJTD_100000_1671.bin", # 地上気象実況報（00,06,12,18UTC）(SYNOP)
                      "./data/bufr/bufr/ISNC11_RJTD_091400_13904.bin", # 地上気象実況報（主要時、中間時以外の時刻）(SYNOP)
                      ):
      with self.subTest(file_path=file_path):
        bufr_class = bufr(os.path.join(os.path.dirname(__file__), file_path))
        bufr_class.read_data()