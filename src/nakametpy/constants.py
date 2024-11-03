# Copyright (c) 2021-2024, NakaMetPy Develoers.
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
Name                     Symbol            Short Name    Units                    Description
------------------------ ----------------- ------------- ------------------------- -------------------------------------------------------
pot_temp_ref_press       :math:`P_0`       P0            :math:`\text{Pa}`         Reference pressure for potential temperature
poisson_exponent         :math:`\kappa`    kappa         :math:`\text{None}`       Exponent in Poisson's equation (Rd/Cp_d)
dry_adiabatic_lapse_rate :math:`\gamma_d`  GammaD       :math:`\text{K km}^{-1}`  The dry adiabatic lapse rate
molecular_weight_ratio   :math:`\epsilon`  epsilon       :math:`\text{None}`       Ratio of molecular weight of water to that of dry air
absolute_temperature     :math:`K`         kelvin, Tabs  :math:`\text{K}`          Kelvin
======================== ================= ============= ========================= =======================================================
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

# bufr
LATEST_MASTER_TABLE_VERSION = 42
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