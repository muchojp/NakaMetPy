# Copyright (c) 2021-2025, NakaMetPy Develoers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# Original source lisence: 
# Copyright (c) 2008,2015,2016,2018 MetPy Developers.
#
r"""A collection of meteorologically significant constant and thermophysical property values.

Earth
-----
======================== =============== ====================== ========================== ===================================
Name                     Symbol          Short Name             Units                      Description
------------------------ --------------- ---------------------- -------------------------- -----------------------------------
earth_avg_radius         :math:`R_e`     Re                     :math:`\text{m}`           Avg. radius of the Earth
earth_gravity            :math:`g`       g, g0, g_acceralation  :math:`\text{m s}^{-2}`    Avg. gravity acceleration on Earth
earth_avg_angular_vel    :math:`\Omega`  Omega                  :math:`\text{rad s}^{-1}`  Avg. angular velocity of Earth
======================== =============== ====================== ========================== ===================================

General Meteorology Constants
-----------------------------
======================== ================= ============= ========================= =======================================================
Name                     Symbol            Short Name    Units                     Description
------------------------ ----------------- ------------- ------------------------- -------------------------------------------------------
pot_temp_ref_press       :math:`P_0`       P0            :math:`\text{Pa}`         Reference pressure for potential temperature
poisson_exponent         :math:`\kappa`    kappa         :math:`\text{None}`       Exponent in Poisson's equation (Rd/Cp_d)
dry_adiabatic_lapse_rate :math:`\gamma_d`  GammaD        :math:`\text{K km}^{-1}`  The dry adiabatic lapse rate
molecular_weight_ratio   :math:`\epsilon`  epsilon       :math:`\text{None}`       Ratio of molecular weight of water to that of dry air
absolute_temperature     :math:`K`         kelvin, Tabs  :math:`\text{K}`          Kelvin
======================== ================= ============= ========================= =======================================================

cmaps
-----
MPL_DEFAULT_COLOR_LIST: `numpy.ndarray`
  Matplotlibのデフォルトカラーのリスト

bufr
----
LATEST_MASTER_TABLE_VERSION: `int`
  NakaMetPyが対応しているBUFRのマスターテーブルの一番新しいバージョン
  
OLDEST_MASTER_TABLE_VERSION: `int`
  NakaMetPyが対応しているBUFRのマスターテーブルの一番古いバージョン

convert_decimal_to_IA5character: `dict`
  CCIAA IA5での数字と文字の辞書形式の対応表
"""

# kinematics
g0 = 9.81 # 重力加速度 m/s**2
g = g0
g_acceralation = g0 # 重力加速度 m/s**2
Re = 6371.229 * 1000 # m
P0 = 100000 # Pa
PI = 3.141592653589793
Omega = 7.2921159 * 1E-5

# thermodynamics
sat_pressure_0c = 611.2 # units : Pa
R = 287 # J/K
Cp = 1004 # J/K
kappa = R / Cp
epsilone = 0.622 # (水：18/乾燥空気：28.8)
LatHeatC = 2.5*10**6 # J/kg
f0 = 1E-4
GammaD = g/Cp
Kelvin = 273.15
Tabs = Kelvin
GasC = R

# cmaps
MPL_DEFAULT_COLOR_LIST = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

# bufr
LATEST_MASTER_TABLE_VERSION = 44
OLDEST_MASTER_TABLE_VERSION = 13

# CCIAA IA5
# URL: https://www.techabulary.com/a/ascii/
convert_decimal_to_IA5character = {
  0  : "[NUL]",
  1  : "[SOH]",
  2  : "[STX]",
  3  : "[ETX]",
  4  : "[EOT]",
  5  : "[ENQ]",
  6  : "[ACK]",
  7  : "[BEL]",
  8  : "[BS]",
  9  : "[HT]",
  10 : "[LF]",
  11 : "[VT]",
  12 : "[FF]",
  13 : "[CR]",
  14 : "[SO]",
  15 : "[SI]",
  16 : "[DLE]",
  17 : "[DC1]",
  18 : "[DC2]",
  19 : "[DC3]",
  20 : "[DC4]",
  21 : "[NAK]",
  22 : "[SYN]",
  23 : "[ETB]",
  24 : "[CAN]",
  25 : "[EM]",
  26 : "[SUB]",
  27 : "[ESC]",
  28 : "[FS]",
  29 : "[GS]",
  30 : "[RS]",
  31 : "[US]",
  32 : "␣",
  33 : "!",
  34 : '"',
  35 : "#",
  36 : "$",
  37 : "%",
  38 : "&",
  39 : "'",
  40 : "(",
  41 : ")",
  42 : "*",
  43 : "+",
  44 : ",",
  45 : "-",
  46 : ".",
  47 : "/",
  48 : "0",
  49 : "1",
  50 : "2",
  51 : "3",
  52 : "4",
  53 : "5",
  54 : "6",
  55 : "7",
  56 : "8",
  57 : "9",
  58 : ":",
  59 : ";",
  60 : "<",
  61 : "=",
  62 : ">",
  63 : "?",
  64 : "@",
  65 : "A",
  66 : "B",
  67 : "C",
  68 : "D",
  69 : "E",
  70 : "F",
  71 : "G",
  72 : "H",
  73 : "I",
  74 : "J",
  75 : "K",
  76 : "L",
  77 : "M",
  78 : "N",
  79 : "O",
  80 : "P",
  81 : "Q",
  82 : "R",
  83 : "S",
  84 : "T",
  85 : "U",
  86 : "V",
  87 : "W",
  88 : "X",
  89 : "Y",
  90 : "Z",
  91 : "[",
  92 : "\\",
  93 : "]",
  94 : "^",
  95 : "_",
  96 : "`",
  97 : "a",
  98 : "b",
  99 : "c",
  100: "d",
  101: "e",
  102: "f",
  103: "g",
  104: "h",
  105: "i",
  106: "j",
  107: "k",
  108: "l",
  109: "m",
  110: "n",
  111: "o",
  112: "p",
  113: "q",
  114: "r",
  115: "s",
  116: "t",
  117: "u",
  118: "v",
  119: "w",
  120: "x",
  121: "y",
  122: "z",
  123: "{",
  124: "|",
  125: "}",
  126: "~",
  127: "DEL",
}
convert_format_to_size = {
  "c": 1,
  "b": 1,
  "B": 1,
  "?": 1,
  "h": 2,
  "H": 2,
  "i": 4,
  "I": 4,
  "l": 4,
  "L": 4,
  "q": 8,
  "Q": 8,
  "e": 2,
  "f": 4,
  "d": 8,
}

available_flag = {
  0: "正常/数値/観測・統計値の品質は正常である",
  2: "正常/現象なし/観測・統計値の品質は正常である",
  8: "やや疑わしい/数値/観測・統計結果にやや疑問がある、または統計対象となる資料の一部が許容する範囲内で欠けている",
  10: "やや疑わしい/現象なし/観測・統計結果にやや疑問がある、または統計対象となる資料の一部が許容する範囲内で欠けている",
  32: "観測値は期間内で資料数が不足している/数値/統計対象となる資料の一部が許容する範囲内を超えて欠けている",
  34: "観測値は期間内で資料数が不足している/現象なし/統計対象となる資料の一部が許容する範囲内を超えて欠けている",
  16: "かなり疑わしい/数値/観測・統計結果にかなり疑問がある",
  18: "かなり疑わしい/現象なし/観測・統計結果にかなり疑問がある",
  24: "利用に適さない/数値/休止や測器の故障等により観測・統計値が得られない、または誤差が大きく明らかに間違いだと判断される",
  26: "利用に適さない/現象なし/休止や測器の故障等により観測・統計値が得られない、または誤差が大きく明らかに間違いだと判断される",
  40: "点検又は計画休止のため欠測/-/-",
  42: "点検又は計画休止のため欠測/-/-",
  48: "障害のため欠測/-/-",
  50: "障害のため欠測/-/-",
  56: "この要素は観測していない/-/この要素は観測していない",
  58: "この要素は観測していない/-/この要素は観測していない",
  127: "データなし/-/-",
}

current_weather_code = {
  0 : "重要な天気が観測されない。",
  4 : "煙霧又は煙、又はちりが浮遊している（視程1km以上）",
  5 : "煙霧又は煙、又はちりが浮遊している（視程1km未満）",
  10: "もや",
  20: "霧があった",
  21: "降水があった",
  22: "霧雨又は霧雪（snow grains）があった",
  23: "雨があった",
  24: "雪があった",
  25: "着氷性の霧雨(freezing drizzle)又は着氷性の雨(freezing rain)があった",
  30: "霧",
  31: "ところどころ濃霧又は氷霧",
  32: "霧又は氷霧、観測時前1時間内にうすくなった",
  33: "霧又は氷霧、観測時前1時間内に変化はなかった",
  34: "霧又は氷霧、観測時前1時間内に始まった又は濃くなった",
  40: "降水",
  41: "降水、弱又は並",
  42: "降水、強",
  50: "霧雨",
  51: "霧雨、弱",
  52: "霧雨、並",
  53: "霧雨、強",
  54: "着氷性の霧雨(freezing drizzle)、弱",
  55: "着氷性の霧雨(freezing drizzle)、並",
  56: "着氷性の霧雨(freezing drizzle)、強",
  60: "雨",
  61: "雨、弱",
  62: "雨、並",
  63: "雨、強",
  64: "着氷性の雨(freezing rain)、弱",
  65: "着氷性の雨(freezing rain)、並",
  66: "着氷性の雨(freezing rain)、強",
  67: "みぞれ又は霧雨と雪、弱",
  68: "みぞれ又は霧雨と雪、並又は強",
  70: "雪",
  71: "雪、弱",
  72: "雪、並",
  73: "雪、強",
  80: "しゅう雨性の降水",
  81: "しゅう雨、弱",
  82: "しゅう雨、並",
  83: "しゅう雨、強",
  84: "しゅう雨、激しい",
  85: "しゅう雪、弱",
  86: "しゅう雪、並",
  87: "しゅう雪、強",
  89: "ひょう(hail)",
  2147483647: "データなし",
}