# Copyright (c) 2025, NakaMetPy Develoers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

import struct
import os
import logging

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
    logging.debug("==============================")
    logging.debug("======= JMA SOCKET HEADER ====")
    logging.debug("==============================")
    jma_socket_header = self.binary[0:10]
    jma_socket_header_str = format(int.from_bytes(jma_socket_header, "big"), f"0{10*8}b")
    logging.debug(f"jma_socket_header bit length：{len(jma_socket_header_str)}")
    logging.debug(f"row bit：{jma_socket_header_str}")
    
    bch = self.binary[10:30]
    bch_str = format(int.from_bytes(bch, "big"), f"0{20*8}b")
    
    logging.debug("==============================")
    logging.debug("======= MESSAGE HEADER =======")
    logging.debug("==============================")
    logging.debug(f"bch bit length：{len(bch_str)}")
    logging.debug(f"row bit：{bch_str}")
    logging.debug(f"バージョンNO：{int(bch_str[0:4], 2)}")
    logging.debug(f"情報サイズ：{int(bch_str[4:8], 2)}")
    logging.debug(f"電文順序番号：{int(bch_str[12:32], 2)}")
    logging.debug(f"中間種別：{int(bch_str[32:33], 2)}")
    logging.debug(f"地震フラグ：{int(bch_str[33:34], 2)}")
    logging.debug(f"予備：{int(bch_str[34:35], 2)}")
    logging.debug(f"テストフラグ：{int(bch_str[35:36], 2)}")
    logging.debug(f"XMLフラグ：{int(bch_str[36:38], 2)}")
    logging.debug(f"データ機密度(未使用)：{int(bch_str[38:40], 2)}")
    logging.debug(f"データ属性：{int(bch_str[40:44], 2)}")
    logging.debug(f"気象庁内配信情報：{int(bch_str[44:48], 2)}")
    logging.debug(f"データ種別：{int(bch_str[48:56], 2)}")
    logging.debug(f"未使用：{int(bch_str[56:64], 2)}")
    logging.debug(f"再送フラグ：{int(bch_str[64:65], 2)}")
    logging.debug(f"データ属性：{int(bch_str[65:68], 2)}")
    logging.debug(f"データ種別：{int(bch_str[68:72], 2)}")
    logging.debug(f"A/N桁数：{int(bch_str[72:80], 2)}")
    logging.debug(f"QCチェックサム：{int(bch_str[80:96], 2)}")
    logging.debug(f"(発信官署)大分類：{int(bch_str[96:98], 2)}")
    logging.debug(f"(発信官署)該当システムビット：{bch_str[98:112]}")
    logging.debug(f"(発信官署)各システムの管理する端末の番号：{int(bch_str[112:128], 2)}")
    logging.debug(f"(受信官署)大分類：{int(bch_str[128:130], 2)}")
    logging.debug(f"(受信官署)該当システムビット：{bch_str[130:144]}")
    logging.debug(f"(受信官署)各システムの管理する端末の番号：{int(bch_str[144:160], 2)}")
    
    logging.debug("==============================")
    logging.debug("======= TELEGRAM HEADER ======")
    logging.debug("==============================")
    tele_header = self.binary[31:49]
    logging.debug(f"電文ヘッダ：{tele_header}")
    self.tele_header_list = tele_header.decode("utf-8").split(" ")
    ttaaii, loc, yygggg = self.tele_header_list
    logging.debug(f"TTAAii：{ttaaii}")
    logging.debug(f"地点：{loc}")
    logging.debug(f"YYGGgg：{yygggg}")
    
    # HEADER
    header = self.binary[49:65]
    logging.debug("==============================")
    logging.debug("======= TELEGRAM BODY ========")
    logging.debug("==============================")
    yyyy = struct.unpack_from('>H', header, 0)[0]
    mmdd = struct.unpack_from('>H', header, 2)[0]
    hhmm = struct.unpack_from('>H', header, 4)[0]
    second = struct.unpack_from('>H', header, 6)[0]
    interval = struct.unpack_from('>H', header, 8)[0]
    ndata = struct.unpack_from('>H', header, 10)[0]
    logging.debug(f"年：{yyyy}")
    logging.debug(f"月、日：{mmdd}")
    logging.debug(f"時、分：{hhmm}")
    logging.debug(f"秒：{second}")
    logging.debug(f"データ送信秋期（秒）：{interval}")
    logging.debug(f"トータルの放電データ数：N：{ndata}")
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
      logging.debug(f"詳細時刻：{detail_sec}")
      logging.debug(f"緯度（x10-3 度）：{lat}")
      logging.debug(f"経度（x10-3 度-100 度）：{lon}")
      logging.debug(f"MMTT：{mmtt}")
      logging.debug(f"雷多重度：{mm}")
      logging.debug(f"放電種別：{tt}")
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