# Copyright (c) 2021, NakaMetPy Develoers.
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


