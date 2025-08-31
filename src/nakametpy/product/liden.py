# Copyright (c) 2025, NakaMetPy Develoers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

# import os
# import sys
# sys.path.append(os.getcwd())
# from .._error import NotSupportedNewerVersionMSWarning, NotSupportedOlderVersionMSWarning,\
#                     NotSupportedBufrError, UnexpectedBufrError,\
#                     MayNotBeAbleToReadBufrWarning
import struct
import os
import re
import logging
import warnings

# Change HERE when developing from INFO into DEBUG
# It will be help you.
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
# logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
# logging.disable(logging.CRITICAL)

class liden:
  def __init__(self, file_path: str) -> None:
    r"""Read LIDEN

    LIDENを読むクラス

    Parameters
    ----------
    file_path : `str`
      path to LIDEN file.

      LIDENファイルのパス
    """
    self.file_path = file_path
    with open(self.file_path, 'rb') as f:
      self.binary = f.read()
    
    # MESSAGE HEADER
    logging.info("==============================")
    logging.info("======= JMA SOCKET HEADER ====")
    logging.info("==============================")
    jma_socket_header = self.binary[0:10]
    jma_socket_header_str = format(int.from_bytes(jma_socket_header, "big"), f"0{10*8}b")
    logging.info(f"jma_socket_header bit length：{len(jma_socket_header_str)}")
    logging.info(f"row bit：{jma_socket_header_str}")
    
    bch = self.binary[10:30]
    bch_str = format(int.from_bytes(bch, "big"), f"0{20*8}b")
    
    logging.info("==============================")
    logging.info("======= MESSAGE HEADER =======")
    logging.info("==============================")
    logging.info(f"bch bit length：{len(bch_str)}")
    logging.info(f"row bit：{bch_str}")
    logging.info(f"バージョンNO：{int(bch_str[0:4], 2)}")
    logging.info(f"情報サイズ：{int(bch_str[4:8], 2)}")
    logging.info(f"電文順序番号：{int(bch_str[12:32], 2)}")
    logging.info(f"中間種別：{int(bch_str[32:33], 2)}")
    logging.info(f"地震フラグ：{int(bch_str[33:34], 2)}")
    logging.info(f"予備：{int(bch_str[34:35], 2)}")
    logging.info(f"テストフラグ：{int(bch_str[35:36], 2)}")
    logging.info(f"XMLフラグ：{int(bch_str[36:38], 2)}")
    logging.info(f"データ機密度(未使用)：{int(bch_str[38:40], 2)}")
    logging.info(f"データ属性：{int(bch_str[40:44], 2)}")
    logging.info(f"気象庁内配信情報：{int(bch_str[44:48], 2)}")
    logging.info(f"データ種別：{int(bch_str[48:56], 2)}")
    logging.info(f"未使用：{int(bch_str[56:64], 2)}")
    logging.info(f"再送フラグ：{int(bch_str[64:65], 2)}")
    logging.info(f"データ属性：{int(bch_str[65:68], 2)}")
    logging.info(f"データ種別：{int(bch_str[68:72], 2)}")
    logging.info(f"A/N桁数：{int(bch_str[72:80], 2)}")
    logging.info(f"QCチェックサム：{int(bch_str[80:96], 2)}")
    logging.info(f"(発信官署)大分類：{int(bch_str[96:98], 2)}")
    logging.info(f"(発信官署)該当システムビット：{bch_str[98:112]}")
    logging.info(f"(発信官署)各システムの管理する端末の番号：{int(bch_str[112:128], 2)}")
    logging.info(f"(受信官署)大分類：{int(bch_str[128:130], 2)}")
    logging.info(f"(受信官署)該当システムビット：{bch_str[130:144]}")
    logging.info(f"(受信官署)各システムの管理する端末の番号：{int(bch_str[144:160], 2)}")
    
    logging.info("==============================")
    logging.info("======= TELEGRAM HEADER ======")
    logging.info("==============================")
    tele_header = self.binary[31:49]
    logging.info(f"電文ヘッダ：{tele_header}")
    self.tele_header_list = tele_header.decode("utf-8").split(" ")
    ttaaii, loc, yygggg = self.tele_header_list
    logging.info(f"TTAAii：{ttaaii}")
    logging.info(f"地点：{loc}")
    logging.info(f"YYGGgg：{yygggg}")
    
    # HEADER
    header = self.binary[49:65]
    logging.info("==============================")
    logging.info("======= TELEGRAM BODY ========")
    logging.info("==============================")
    yyyy = struct.unpack_from('>H', header, 0)[0]
    mmdd = struct.unpack_from('>H', header, 2)[0]
    hhmm = struct.unpack_from('>H', header, 4)[0]
    second = struct.unpack_from('>H', header, 6)[0]
    interval = struct.unpack_from('>H', header, 8)[0]
    ndata = struct.unpack_from('>H', header, 10)[0]
    logging.info(f"年：{yyyy}")
    logging.info(f"月、日：{mmdd}")
    logging.info(f"時、分：{hhmm}")
    logging.info(f"秒：{second}")
    logging.info(f"データ送信秋期（秒）：{interval}")
    logging.info(f"トータルの放電データ数：N：{ndata}")
    self.header_data = [yyyy, mmdd, hhmm, second, interval, ndata]
    
    # BODY
    body = self.binary[65:]
    self.data = []
    for i in range(ndata):
      detail_sec = struct.unpack_from('>H', body, 0+i*10)[0]
      lat = struct.unpack_from('>H', body, 2+i*10)[0]
      lon = struct.unpack_from('>H', body, 4+i*10)[0]
      mmtt = f"{struct.unpack_from('>H', body, 6+i*10)[0]:4}"
      mm, tt = mmtt[0:2], mmtt[2:4]
      logging.info(f"詳細時刻：{detail_sec}")
      logging.info(f"緯度（x10-3 度）：{lat}")
      logging.info(f"経度（x10-3 度-100 度）：{lon}")
      logging.info(f"MMTT：{mmtt}")
      logging.info(f"雷多重度：{mm}")
      logging.info(f"放電種別：{tt}")
      self.data.append([detail_sec, lat, lon, mm, tt])
      
  def get_telegram_header(self) -> list:
    r"""get telegram header

    Returns
    -------
    list
      telegram header
    """
    return self.tele_header_list
      
  def get_header_data(self) -> list:
    r"""get header data

    Returns
    -------
    list
      header data
    """
    return self.header_data
      
  def get_data(self) -> list:
    r"""get data

    Returns
    -------
    list
      data
    """
    return self.data

if __name__=='__main__':
  liden_class = liden(os.path.join(os.path.dirname(__file__), "../../../tests/data/product/liden/20160415_LIDEN_Sample.bin"))