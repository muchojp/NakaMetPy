# Copyright (c) 2021, NakaMetPy Develoers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# Original source lisence:
# Copyright (c) 2009,2017,2018,2019 MetPy Developers.
#

#
# そもそものプログラム自体はMetPyのsource codeにあるため、自分はあくまでも
# metpy.unitsを用いないNumPyでの高速な計算を行うプログラムを作成することを目指す
# 入力データの単位に気をつけなければならない
# 単位はPa, K, RHは[0, 1]とする。
# 
# 更新日：2021/01/25 地衡風と非地衡風、相対渦度、気温減率、偽断熱減率、静的安定パラメタを求める関数の実装
#
import numpy as np
from .thermo import mixing_ratio_from_specific_humidity, potential_temperature, mixing_ratio_from_relative_humidity, virtual_temperature, saturation_mixing_ratio
from .constants import sat_pressure_0c, R, Cp, kappa, P0, epsilone, LatHeatC, g, Re, f0, GammaD



def distance_4d(lons, lats, lev_len = 37, t_len = 24):
    r'''
    各格子点間の距離を求める関数。次元は[時間、鉛直方向、緯度、経度]である。

    地球半径の値は6371229mを使用。
    '''
    # lons, latsが1次元の場合、2次元に変換する
    if lats.ndim == 1:
        lons, lats = np.meshgrid(lons, lats)
    # 時間、高度、緯度、経度の4次元のデータを計算するために、2次元の緯度経度を4次元にする
    lons = np.tile(lons.flatten(), lev_len*t_len).reshape(t_len, lev_len, lons.shape[0], lons.shape[1])
    lats = np.tile(lats.flatten(), lev_len*t_len).reshape(t_len, lev_len, lats.shape[0], lats.shape[1])
    radius = Re # m
    dlats_x = np.radians(np.diff(lats, axis=-1))
    dlats_y = np.radians(np.diff(lats, axis=-2))
    dlons_x = np.radians(np.diff(lons, axis=-1))
    dlons_y = np.radians(np.diff(lons, axis=-2))

    x_deg = np.sin(dlats_x/2) * np.sin(dlats_x/2) + np.cos(np.radians(lats[:, :, :, :-1])) \
        * np.cos(np.radians(lats[:, :, :, 1:])) * np.sin(dlons_x/2) * np.sin(dlons_x/2)
    x_rad = 2 * np.arctan2(np.sqrt(x_deg), np.sqrt(1-x_deg))
    dx = radius * x_rad
    
    y_deg = np.sin(dlats_y/2) * np.sin(dlats_y/2) + np.cos(np.radians(lats[:, :, :-1, :])) \
        * np.cos(np.radians(lats[:, :, 1:, :])) * np.sin(dlons_y/2) * np.sin(dlons_y/2)
    y_rad = 2 * np.arctan2(np.sqrt(y_deg), np.sqrt(1-y_deg))
    dy = radius * y_rad
    
    return dx, dy



def distance_3d(lons, lats, t_len = 24):
    # lons, latsが1次元の場合、2次元に変換する
    if lats.ndim == 1:
        lons, lats = np.meshgrid(lons, lats)
    # 時間、高度、緯度、経度の4次元のデータを計算するために、2次元の緯度経度を3次元にする
    # もし特定の時間に関する3次元データを扱う場合、t_lenをERAの場合37にする
    lons = np.tile(lons.flatten(), t_len).reshape(t_len, lons.shape[0], lons.shape[1])
    lats = np.tile(lats.flatten(), t_len).reshape(t_len, lats.shape[0], lats.shape[1])
    radius = Re # m
    dlats_x = np.radians(np.diff(lats, axis=-1))
    dlats_y = np.radians(np.diff(lats, axis=-2))
    dlons_x = np.radians(np.diff(lons, axis=-1))
    dlons_y = np.radians(np.diff(lons, axis=-2))

    x_deg = np.sin(dlats_x/2) * np.sin(dlats_x/2) + np.cos(np.radians(lats[:, :, :-1])) \
        * np.cos(np.radians(lats[:, :, 1:])) * np.sin(dlons_x/2) * np.sin(dlons_x/2)
    x_rad = 2 * np.arctan2(np.sqrt(x_deg), np.sqrt(1-x_deg))
    dx = radius * x_rad
    
    y_deg = np.sin(dlats_y/2) * np.sin(dlats_y/2) + np.cos(np.radians(lats[:, :-1, :])) \
        * np.cos(np.radians(lats[:, 1:, :])) * np.sin(dlons_y/2) * np.sin(dlons_y/2)
    y_rad = 2 * np.arctan2(np.sqrt(y_deg), np.sqrt(1-y_deg))
    dy = radius * y_rad
    
    return dx, dy



def distance_2d(lons, lats):
    if lats.ndim == 1:
        lons, lats = np.meshgrid(lons, lats)
    radius = Re # m
    dlats_x = np.radians(np.diff(lats, axis=-1))
    dlats_y = np.radians(np.diff(lats, axis=-2))
    dlons_x = np.radians(np.diff(lons, axis=-1))
    dlons_y = np.radians(np.diff(lons, axis=-2))

    x_deg = np.sin(dlats_x/2) * np.sin(dlats_x/2) + np.cos(np.radians(lats[:, :-1])) \
        * np.cos(np.radians(lats[:, 1:])) * np.sin(dlons_x/2) * np.sin(dlons_x/2)
    x_rad = 2 * np.arctan2(np.sqrt(x_deg), np.sqrt(1-x_deg))
    dx = radius * x_rad
    
    y_deg = np.sin(dlats_y/2) * np.sin(dlats_y/2) + np.cos(np.radians(lats[:-1, :])) \
        * np.cos(np.radians(lats[1:, :])) * np.sin(dlons_y/2) * np.sin(dlons_y/2)
    y_rad = 2 * np.arctan2(np.sqrt(y_deg), np.sqrt(1-y_deg))
    dy = radius * y_rad
    
    return dx, dy


"""def wrong_divergence(fx, fy, dx, dy):
    div = np.ma.zeros(fx.shape)
    diff_x = np.diff(fx, axis=-1)
    diff_y = np.diff(fy, axis=-2)
    div_x = np.diff(diff_x/dx)
    div_y = np.diff(diff_y/dy, axis=-2)
    div[:, 1:-1] += div_x
    div[1:-1, :] += div_y
    return div"""


def gradient_h_4d(var, dx, dy, wrfon=0):
    grad_shape = list(var.shape)
    grad_shape.insert(0, 2) # grad_xとgrad_yの2つの次元を追加
    grad = np.ma.zeros(grad_shape)
    grad_x_stag = np.diff(var, axis=-1)/dx
    grad_y_stag = (-1)**(wrfon-1)*np.diff(var, axis=-2)/dy
    # 境界条件を代入
    grad[0, :, :, :, 0] = grad_x_stag[:, :, :, 0]
    grad[0, :, :, :, -1] = grad_x_stag[:, :, :, -1]
    grad[1, :, :, 0, :] = grad_y_stag[:, :, 0, :]
    grad[1, :, :, -1, :] = grad_y_stag[:, :, -1, :]
    grad[0, :, :, :, 1:-1] = (grad_x_stag[:, :, :, 1:] + grad_x_stag[:, :, :, :-1])/2
    grad[1, :, :, 1:-1, :] = (grad_y_stag[:, :, 1:, :] + grad_y_stag[:, :, :-1, :])/2
    return grad


def gradient_h_3d(var, dx, dy, wrfon=0):
    grad_shape = list(var.shape)
    grad_shape.insert(0, 2) # grad_xとgrad_yの2つの次元を追加
    grad = np.ma.zeros(grad_shape)
    grad_x_stag = np.diff(var, axis=-1)/dx
    grad_y_stag = (-1)**(wrfon-1)*np.diff(var, axis=-2)/dy
    # 境界条件を代入
    grad[0, :, :, 0] = grad_x_stag[:, :, 0]
    grad[0, :, :, -1] = grad_x_stag[:, :, -1]
    grad[1, :, 0, :] = grad_y_stag[:, 0, :]
    grad[1, :, -1, :] = grad_y_stag[:, -1, :]
    grad[0, :, :, 1:-1] = (grad_x_stag[:, :, 1:] + grad_x_stag[:, :, :-1])/2
    grad[1, :, 1:-1, :] = (grad_y_stag[:, 1:, :] + grad_y_stag[:, :-1, :])/2
    return grad


def gradient_h_2d(var, dx, dy, wrfon=0):
    grad_shape = list(var.shape)
    grad_shape.insert(0, 2) # grad_xとgrad_yの2つの次元を追加
    grad = np.ma.zeros(grad_shape)
    grad_x_stag = np.diff(var, axis=-1)/dx
    grad_y_stag = (-1)**(wrfon-1)*np.diff(var, axis=-2)/dy
    # 境界条件を代入
    grad[0, :, 0] = grad_x_stag[:, 0]
    grad[0, :, -1] = grad_x_stag[:, -1]
    grad[1, 0, :] = grad_y_stag[0, :]
    grad[1, -1, :] = grad_y_stag[-1, :]
    grad[0, :, 1:-1] = (grad_x_stag[:, 1:] + grad_x_stag[:, :-1])/2
    grad[1, 1:-1, :] = (grad_y_stag[1:, :] + grad_y_stag[:-1, :])/2
    return grad


def divergence_2d(fx, fy, dx, dy, wrfon=0):
    div = np.ma.zeros(fx.shape)
    grad_x_stag = np.diff(fx, axis=-1)/dx
    grad_y_stag = (-1)**(wrfon-1)*np.diff(fy, axis=-2)/dy
    div[:, 0] = grad_x_stag[:, 0]
    div[:, -1] = grad_x_stag[:, -1]
    div[0, :] = grad_y_stag[0, :]
    div[-1, :] = grad_y_stag[-1, :]
    div[:, 1:-1] += (grad_x_stag[:, :-1]+grad_x_stag[:, 1:])/2
    div[1:-1, :] += (grad_y_stag[:-1, :]+grad_y_stag[1:, :])/2
    return div


def vert_grad_3d(variables, pres_3d, z_dim=0):
    if pres_3d.ndim == 1:
        pres_3d = np.tile(pres_3d, (variables.shape[-2]*variables.shape[-1])).reshape([variables.shape[-2], \
            variables.shape[-1], variables.shape[-3]]).transpose(2, 0, 1)
    vertical_grad = np.ma.zeros(variables.shape)
    diff_pres = np.diff(pres_3d, axis=z_dim)
    grad_var = np.diff(variables, axis=z_dim)/diff_pres
    vertical_grad[0] = grad_var[0]
    vertical_grad[-1] = grad_var[-1]
    diff_pres_sum = diff_pres[:-1] + diff_pres[1:]
    vertical_grad[1:-1] = grad_var[1:]/diff_pres_sum*diff_pres[:-1] + grad_var[:-1]/diff_pres_sum*diff_pres[1:]
    return vertical_grad


def vert_grad_4d(variables, pres_4d, z_dim=1):
    r'''
    気圧座標系における鉛直勾配を計算する関数。
    気圧の配列はtopからbottomの方向を想定している([..., 500, 600, 700, ...])。

    まずは1次元の気圧の配列を4次元に変換する。

    
    .. math:: GRAD_{n+1/2} &= \frac{\left(f(p_{n}) - f(p_{n+1})\right)}{-\left(p_{n} - p_{n+1}\right)} \
        &= \frac{\left(f(p_{n+1}) - f(p_{n})\right)}{-\left(p_{n+1} - p_{n}\right)}

    '''
    if pres_4d.ndim == 1:
        pres_4d = np.tile(pres_4d, (variables.shape[0]*variables.shape[-2]*variables.shape[-1])).reshape([variables.shape[-2], \
            variables.shape[-1], variables.shape[-3], variables.shape[0]]).transpose(2, 3, 0, 1)
    vertical_grad = np.ma.zeros(variables.shape)
    diff_pres = np.diff(pres_4d, axis=z_dim)
    grad_var = np.diff(variables, axis=z_dim)/diff_pres
    vertical_grad[:, 0, :, :] = grad_var[:, 0, :, :]
    vertical_grad[:, -1, :, :] = grad_var[:, -1, :, :]
    diff_pres_sum = diff_pres[:, :-1, :, :] + diff_pres[:, 1:, :, :]
    vertical_grad[:, 1:-1, :, :] = grad_var[:, 1:, :, :]/diff_pres_sum*diff_pres[:, :-1, :, :] + \
        grad_var[:, :-1, :, :]/diff_pres_sum*diff_pres[:, 1:, :, :]
    return vertical_grad


def advection_h_3d(var, wind_u, wind_v, dx, dy, wrfon=0):
    advs_shape = list(wind_u.shape)
    advs_shape.insert(0, 2) # grad_xとgrad_yの2つの次元を追加
    advs = np.ma.zeros(advs_shape)
    var_grad_x, var_grad_y = gradient_h_3d(var, dx, dy, wrfon=wrfon)
    advs[0] = -wind_u * var_grad_x
    advs[1] = -wind_v * var_grad_y
    return advs


def advection_h_4d(var, wind_u, wind_v, dx, dy, wrfon=0):
    advs_shape = list(wind_u.shape)
    advs_shape.insert(0, 2) # grad_xとgrad_yの2つの次元を追加
    advs = np.ma.zeros(advs_shape)
    var_grad_x, var_grad_y = gradient_h_4d(var, dx, dy, wrfon=wrfon)
    advs[0] = -wind_u * var_grad_x
    advs[1] = -wind_v * var_grad_y
    return advs



def q_1(temperature_1, temperature_2, temperature_3, wind_u, wind_v, p_velocity, pressure, dx, dy, time_step=3600, wrfon=0):
    r'''
    この関数は時間発展を計算する項が含まれているため、4次元の配列で計算が行われます。
    '''
    terms_shape = list(wind_u.shape)
    terms_shape.insert(0, 3) # grad_xとgrad_yの2つの次元を追加
    terms = np.ma.zeros(terms_shape)
    temperature = np.concatenate([temperature_1[-1:, :], temperature_2[:], temperature_3[:1, :]])
    time_evolv = np.diff(temperature, axis=0)
    terms[0] = Cp * (time_evolv[:-1] + time_evolv[1:]) / (2 * time_step)
    # grad_x_t, grad_y_t = gradient_h_4d(temperature_2, dx, dy)
    # term_2 = Cp * (wind_u * grad_x_t + wind_v * grad_y_t)
    advec_x, advec_y = -advection_h_4d(temperature_2, wind_u, wind_v, dx, dy, wrfon=wrfon)
    terms[1] = Cp * (advec_x + advec_y)
    terms[2] = Cp * ((pressure / P0) ** kappa) * p_velocity * vert_grad_4d(potential_temperature(pressure, temperature_2), pressure)
    return terms



def q_2_rh(temperature_1, temperature_2, temperature_3, rh_1, rh_2, rh_3, wind_u, wind_v, p_velocity, pressure, dx, dy, time_step=3600, wrfon=0):
    r'''
    この関数は時間発展を計算する項が含まれているため、4次元の配列で計算が行われます。
    '''
    terms_shape = list(wind_u.shape)
    terms_shape.insert(0, 3) # grad_xとgrad_yの2つの次元を追加
    terms = np.ma.zeros(terms_shape)
    temperature = np.concatenate([temperature_1[-1:, :], temperature_2[:], temperature_3[:1, :]])
    rh = np.concatenate([rh_1[-1:, :], rh_2[:], rh_3[:1, :]])
    pres_add = np.concatenate([pressure[0, :], pressure])
    terms[0] = -LatHeatC * np.diff(mixing_ratio_from_relative_humidity(rh, temperature, pres_add), axis=0) / time_step
    mix_2 = mixing_ratio_from_relative_humidity(rh_2, temperature_2, pressure)
    # grad_x_t, grad_y_t = gradient_h_4d(temperature_2, dx, dy)
    # term_2 = Cp * (wind_u * grad_x_t + wind_v * grad_y_t)
    advec_x, advec_y = -advection_h_4d(mix_2, wind_u, wind_v, dx, dy, wrfon=wrfon)
    terms[1] = -LatHeatC * (advec_x + advec_y)
    terms[2] = -LatHeatC * (p_velocity * vert_grad_4d(mix_2, pressure))
    return terms



def q_2_sh_mix(sh_1, sh_2, sh_3, wind_u, wind_v, p_velocity, pressure, dx, dy, time_step=3600, wrfon=0):
    r'''
    この関数は時間発展を計算する項が含まれているため、4次元の配列で計算が行われます。
    '''
    terms_shape = list(wind_u.shape)
    terms_shape.insert(0, 3) # grad_xとgrad_yの2つの次元を追加
    terms = np.ma.zeros(terms_shape)
    sh = np.concatenate([sh_1[-1:, :], sh_2[:], sh_3[:1, :]])
    time_evolv = np.diff(mixing_ratio_from_specific_humidity(sh), axis=0)
    terms[0] = -LatHeatC * (time_evolv[:-1] + time_evolv[1:]) / (2 * time_step)
    # terms[0] = -LatHeatC * np.diff(sh, axis=0) / time_step
    mix_2 = mixing_ratio_from_specific_humidity(sh_2)
    advec_x, advec_y = -advection_h_4d(mix_2, wind_u, wind_v, dx, dy, wrfon=wrfon)
    # advec_x, advec_y = -advection_h_4d(sh_2, wind_u, wind_v, dx, dy, wrfon=wrfon)
    terms[1] = -LatHeatC * (advec_x + advec_y)
    terms[2] = -LatHeatC * (p_velocity * vert_grad_4d(mix_2, pressure))
    # terms[2] = -LatHeatC * (p_velocity * vert_grad_4d(sh_2, pressure))
    return terms



def q_2_sh_sh(sh_1, sh_2, sh_3, wind_u, wind_v, p_velocity, pressure, dx, dy, time_step=3600, wrfon=0):
    r'''
    この関数は時間発展を計算する項が含まれているため、4次元の配列で計算が行われます。
    '''
    terms_shape = list(wind_u.shape)
    terms_shape.insert(0, 3) # grad_xとgrad_yの2つの次元を追加
    terms = np.ma.zeros(terms_shape)
    sh = np.concatenate([sh_1[-1:, :], sh_2[:], sh_3[:1, :]])
    # terms[0] = -LatHeatC * np.diff(mixing_ratio_from_specific_humidity(sh), axis=0) / time_step
    time_evolv = np.diff(sh, axis=0)
    terms[0] = -LatHeatC * (time_evolv[:-1] + time_evolv[1:]) / (2 * time_step)
    # mix_2 = mixing_ratio_from_specific_humidity(sh_2)
    # advec_x, advec_y = -advection_h_4d(mix_2, wind_u, wind_v, dx, dy, wrfon=wrfon)
    advec_x, advec_y = -advection_h_4d(sh_2, wind_u, wind_v, dx, dy, wrfon=wrfon)
    terms[1] = -LatHeatC * (advec_x + advec_y)
    # terms[2] = -LatHeatC * (p_velocity * vert_grad_4d(mix_2, pressure))
    terms[2] = -LatHeatC * (p_velocity * vert_grad_4d(sh_2, pressure))
    return terms


def pressure_4d(pres, time_dim=24, lat_dim=201, lon_dim=401):
    return np.tile(pres, time_dim*lat_dim*lon_dim).reshape(lon_dim, lat_dim, time_dim, len(pres)).transpose(2, 3, 1, 0)


def pressure_3d(pres, lat_dim=201, lon_dim=401):
    return np.tile(pres, lat_dim*lon_dim).reshape(lat_dim, lon_dim, len(pres)).transpose(2, 0, 1)



def vert_grad_4d_height(variables, height, z_dim=1):
    vertical_grad = np.ma.zeros(variables.shape)
    diff_pres = np.diff(height, axis=z_dim)
    grad_var = np.diff(variables, axis=z_dim)/diff_pres
    vertical_grad[:, 0, :, :] = grad_var[:, 0, :, :]
    vertical_grad[:, -1, :, :] = grad_var[:, -1, :, :]
    diff_pres_sum = diff_pres[:, :-1, :, :] + diff_pres[:, 1:, :, :]
    vertical_grad[:, 1:-1, :, :] = grad_var[:, 1:, :, :]/diff_pres_sum*diff_pres[:, :-1, :, :] + \
        grad_var[:, :-1, :, :]/diff_pres_sum*diff_pres[:, 1:, :, :]
    return vertical_grad


def vert_grad_3d_height(variables, height, z_dim=0):
    vertical_grad = np.ma.zeros(variables.shape)
    diff_pres = np.diff(height, axis=z_dim)
    grad_var = np.diff(variables, axis=z_dim)/diff_pres
    vertical_grad[0, :, :] = grad_var[0, :, :]
    vertical_grad[-1, :, :] = grad_var[-1, :, :]
    diff_pres_sum = diff_pres[:-1, :, :] + diff_pres[1:, :, :]
    vertical_grad[1:-1, :, :] = grad_var[1:, :, :]/diff_pres_sum*diff_pres[:-1, :, :] + \
        grad_var[:-1, :, :]/diff_pres_sum*diff_pres[1:, :, :]
    return vertical_grad


def vert_grad_2d_height(variables, height, z_dim=0):
    vertical_grad = np.ma.zeros(variables.shape)
    diff_pres = np.diff(height, axis=z_dim)
    grad_var = np.diff(variables, axis=z_dim)/diff_pres
    vertical_grad[0, :] = grad_var[0, :]
    vertical_grad[-1, :] = grad_var[-1, :]
    diff_pres_sum = diff_pres[:-1, :] + diff_pres[1:, :]
    vertical_grad[1:-1, :] = grad_var[1:, :]/diff_pres_sum*diff_pres[:-1, :] + \
        grad_var[:-1, :]/diff_pres_sum*diff_pres[1:, :]
    return vertical_grad

def richardson_number(temp, rh, height, pres, u, v):
    v_pt = potential_temperature(pressure_4d(pres), virtual_temperature(temp, mixing_ratio_from_relative_humidity(rh, temp, pres)))
    return g/v_pt(vert_grad_4d_height(v_pt, height))/(vert_grad_4d_height(u, height)**2+vert_grad_4d_height(v, height)**2)



def geostrophic_wind(geopotential, dx, dy, f0=f0):
    r'''
    地衡風を求める。
    ジオポテンシャルの水平微分を行い、コリオリパラメタで割った後、
    u成分にマイナスをかける。
    '''
    terms = gradient_h_4d(geopotential, dx, dy)/f0
    terms[0] = -terms[0]
    return terms


def ageostrophic_wind(geopotential, u_wind, v_wind, dx, dy, f0=f0):
    r'''
    非地衡風成分を求める。
    実際の風の東西・南北成分から地衡風成分を引く
    '''
    terms = geostrophic_wind(geopotential, dx, dy, f0)
    terms[0] -= u_wind
    terms[1] -= v_wind
    return terms


def relative_vorticity(u, v, dx, dy):
    v_x_comp, _ = gradient_h_4d(v, dx, dy)
    _, u_y_comp = gradient_h_4d(v, dx, dy)
    return v_x_comp - u_y_comp



def lapse_rate(pressure, temperature, height):
    r"""
    実際の断熱減率などの呼び方がある。
    詳しくはHolton 5th edition pp54
    """
    theta = potential_temperature(pressure, temperature)
    return GammaD-temperature/theta*vert_grad_4d_height(theta, height)


def pseudoadiabatic_lapse_rate(pressure, temperature):
    r"""
    偽断熱減率、湿潤断熱減率などの呼び方がある。
    詳しくはHolton 5th edition pp61
    """
    qs = saturation_mixing_ratio(pressure, temperature)
    numerator = 1 + LatHeatC*qs/(R*temperature)
    denominator = 1 + (epsilone*LatHeatC**2*qs)/(Cp*R*temperature**2)
    return GammaD*numerator/denominator


def static_stability(pressure, temperature):
    return -(R*temperature/pressure)*vert_grad_4d(np.log(potential_temperature(pressure, temperature)), pressure)

