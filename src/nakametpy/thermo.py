# Copyright (c) 2021, NakaMetPy Develoers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# Original source lisence:
# Copyright (c) 2008,2015,2016,2017,2018,2019 MetPy Developers.
#
# 
# そもそものプログラム自体はMetPyのsource codeにあるため、自分はあくまでも
# metpy.unitsを用いないNumPyでの高速な計算を行うプログラムを作成することを目指す
# 入力データの単位に気をつけなければならない
# 単位はPa, K, RHは[0, 1]とする。
#
# To Do:
# precipitable_waterなど、MetPyにはあってNakaMetPyにはない関数が複数ある。
# 時間を見つけて実装する。
#
#
import numpy as np
from .constants import sat_pressure_0c, R, Cp, kappa, P0, epsilone, LatHeatC, g, Re


def mixing_ratio_from_relative_humidity(relative_humidity, temperature, pressure):
    r"""Calculate the mixing ratio from relative humidity, temperature, and pressure.

    Parameters
    ----------
    relative_humidity: `numpy.ndarray`
        Relative Humidity
        相対湿度
        値は(0, 1]である必要がある
    temperature: `numpy.ndarray`
        Air temperature
        気温
    pressure: `numpy.ndarray`
        Total atmospheric pressure
        全圧

    Returns
    -------
    `numpy.ndarray`
        Dimensionless mixing ratio

    Notes
    -----
    Formula adapted from [Hobbs1977]_ pg. 74.

    .. math:: w = (RH)(w_s)

    * :math:`w` is mixing ratio
    * :math:`RH` is relative humidity as a unitless ratio
    * :math:`w_s` is the saturation mixing ratio

    See Also
    --------
    relative_humidity_from_mixing_ratio, saturation_mixing_ratio

    """
    return relative_humidity * saturation_mixing_ratio(pressure, temperature)



def saturation_mixing_ratio(tot_press, temperature):
    r"""Calculate the saturation mixing ratio of water vapor.

    This calculation is given total pressure and the temperature. The implementation
    uses the formula outlined in [Hobbs1977]_ pg.73.

    Parameters
    ----------
    tot_press: `numpy.ndarray`
        Total atmospheric pressure
    temperature: `numpy.ndarray`
        air temperature

    Returns
    -------
    `numpy.ndarray`
        The saturation mixing ratio, dimensionless

    """
    return mixing_ratio(saturation_vapor_pressure(temperature), tot_press)



# def mixing_ratio(part_press, tot_press, molecular_weight_ratio=mpconsts.epsilon):
def mixing_ratio(part_press, tot_press, molecular_weight_ratio=0.622):
    r"""Calculate the mixing ratio of a gas.

    This calculates mixing ratio given its partial pressure and the total pressure of
    the air. There are no required units for the input arrays, other than that
    they have the same units.

    Parameters
    ----------
    part_press : `numpy.ndarray`
        Partial pressure of the constituent gas
    tot_press : `numpy.ndarray`
        Total air pressure
    molecular_weight_ratio : `numpy.ndarray` or float, optional
        The ratio of the molecular weight of the constituent gas to that assumed
        for air. Defaults to the ratio for water vapor to dry air
        (:math:`\varepsilon\approx0.622`).
        水の分子量と空気の平均の分子量の比=18/28.8
    Returns
    -------
    `numpy.ndarray`
        The (mass) mixing ratio, dimensionless (e.g. Kg/Kg or g/g)

    Notes
    -----
    This function is a straightforward implementation of the equation given in many places,
    such as [Hobbs1977]_ pg.73:

    .. math:: r = \varepsilon \frac{e}{p - e}

    See Also
    --------
    saturation_mixing_ratio, vapor_pressure

    """
    return molecular_weight_ratio * part_press / (tot_press - part_press)


def mixing_ratio_from_specific_humidity(specific_humidity):
    r"""Calculate the mixing ratio from specific humidity.

    Parameters
    ----------
    specific_humidity: `numpy.ndarray`
        Specific humidity of air

    Returns
    -------
    `numpy.ndarray`
        Mixing ratio

    Notes
    -----
    Formula from [Salby1996]_ pg. 118.

    .. math:: w = \frac{q}{1-q}

    * :math:`w` is mixing ratio
    * :math:`q` is the specific humidity

    See Also
    --------
    mixing_ratio, specific_humidity_from_mixing_ratio

    """
    return specific_humidity / (1 - specific_humidity)




def saturation_vapor_pressure(temperature):
    r"""Calculate the saturation water vapor (partial) pressure.

    Parameters
    ----------
    temperature : `numpy.ndarray`
        air temperature

    Returns
    -------
    `numpy.ndarray`
        The saturation water vapor (partial) pressure

    See Also
    --------
    vapor_pressure, dewpoint

    Notes
    -----
    Instead of temperature, dewpoint may be used in order to calculate
    the actual (ambient) water vapor (partial) pressure.

    The formula used is that from [Bolton1980]_ for T in degrees Celsius:

    .. math:: 6.112 e^\frac{17.67T}{T + 243.5}

    下記の式は既にケルビンに直してある

    """
    # Converted from original in terms of C to use kelvin. Using raw absolute values of C in
    # a formula plays havoc with units support.
    return sat_pressure_0c * np.exp(17.67 * (temperature - 273.15) / (temperature - 29.65))


# ---------------------------------------------------------------------------------------


def dewpoint_from_relative_humidity(temperature, rh):
    r"""Calculate the ambient dewpoint given air temperature and relative humidity.

    Parameters
    ----------
    temperature : `numpy.ndarray`
        air temperature
    rh : `numpy.ndarray`
        relative humidity expressed as a ratio in the range 0 < rh <= 1

    Returns
    -------
    `numpy.ndarray`
        The dewpoint temperature

    See Also
    --------
    dewpoint, saturation_vapor_pressure

    """
    # if np.any(rh > 1.2):
    #     warnings.warn('Relative humidity >120%, ensure proper units.')
    return dewpoint(rh * saturation_vapor_pressure(temperature))

def dewpoint(e):
    r"""Calculate the ambient dewpoint given the vapor pressure.

    Parameters
    ----------
    e : `numpy.ndarray`
        Water vapor partial pressure

    Returns
    -------
    `numpy.ndarray`
        dewpoint temperature

    See Also
    --------
    dewpoint_from_relative_humidity, saturation_vapor_pressure, vapor_pressure

    Notes
    -----
    This function inverts the [Bolton1980]_ formula for saturation vapor
    pressure to instead calculate the temperature. This yield the following
    formula for dewpoint in degrees Celsius:

    .. math:: T = \frac{243.5 \log(e / 6.112)}{17.67 - \log(e / 6.112)}

    """
    val = np.log(e / sat_pressure_0c)
    return 243.5 * val / (17.67 - val) + 273.15


def dewpoint_from_specific_humidity(pressure, temperature, specific_humidity):
    r"""Calculate the dewpoint from specific humidity, temperature, and pressure.

    Parameters
    ----------
    pressure: `numpy.ndarray`
        Total atmospheric pressure

    temperature: `numpy.ndarray`
        Air temperature

    specific_humidity: `numpy.ndarray`
        Specific humidity of air

    Returns
    -------
    `numpy.ndarray`
        Dew point temperature


    .. versionchanged:: 1.0
       Changed signature from ``(specific_humidity, temperature, pressure)``

    See Also
    --------
    relative_humidity_from_mixing_ratio, dewpoint_from_relative_humidity

    """
    return dewpoint_from_relative_humidity(temperature,
                                           relative_humidity_from_specific_humidity(
                                               pressure, temperature, specific_humidity))


def equivalent_potential_temperature(pressure, temperature, dewpoint):
    r"""Calculate equivalent potential temperature.

    This calculation must be given an air parcel's pressure, temperature, and dewpoint.
    The implementation uses the formula outlined in [Bolton1980]_:

    First, the LCL temperature is calculated:

    .. math:: T_{L}=\frac{1}{\frac{1}{T_{D}-56}+\frac{ln(T_{K}/T_{D})}{800}}+56

    Which is then used to calculate the potential temperature at the LCL:

    .. math:: \theta_{DL}=T_{K}\left(\frac{1000}{p-e}\right)^\kappa
              \left(\frac{T_{K}}{T_{L}}\right)^{0.28r}

    Both of these are used to calculate the final equivalent potential temperature:

    .. math:: \theta_{E}=\theta_{DL}\exp\left[\left(\frac{3036.}{T_{L}}
                                              -1.78\right)\times r(1+0.448r)\right]

    Parameters
    ----------
    pressure: `numpy.ndarray`
        Total atmospheric pressure
    temperature: `numpy.ndarray`
        Temperature of parcel
    dewpoint: `numpy.ndarray`
        Dewpoint of parcel

    Returns
    -------
    `numpy.ndarray`
        The equivalent potential temperature of the parcel

    Notes
    -----
    [Bolton1980]_ formula for Theta-e is used, since according to
    [DaviesJones2009]_ it is the most accurate non-iterative formulation
    available.

    """
    t = temperature
    td = dewpoint
    p = pressure
    e = saturation_vapor_pressure(dewpoint)
    r = saturation_mixing_ratio(pressure, dewpoint)

    t_l = 56 + 1. / (1. / (td - 56) + np.log(t / td) / 800.) + 273.15
    th_l = t * (100000. / (p - e)) ** kappa * (t / t_l) ** (0.28 * r)
    th_e = th_l * np.exp((3036. / t_l - 1.78) * r * (1 + 0.448 * r))

    return th_e


def potential_temperature(pressure, temperature):
    r"""Calculate the potential temperature.

    Uses the Poisson equation to calculation the potential temperature
    given `pressure` and `temperature`.

    Parameters
    ----------
    pressure : `numpy.ndarray`
        total atmospheric pressure
    temperature : `numpy.ndarray`
        air temperature

    Returns
    -------
    `numpy.ndarray`
        The potential temperature corresponding to the temperature and
        pressure.

    See Also
    --------
    dry_lapse

    Notes
    -----
    Formula:

    .. math:: \Theta = T (P_0 / P)^\kappa

    """
    return temperature / exner_function(pressure)


def exner_function(pressure, reference_pressure=P0):
    r"""Calculate the Exner function.

    .. math:: \Pi = \left( \frac{p}{p_0} \right)^\kappa

    This can be used to calculate potential temperature from temperature (and visa-versa),
    since

    .. math:: \Pi = \frac{T}{\theta}

    Parameters
    ----------
    pressure : `numpy.ndarray`
        total atmospheric pressure
    reference_pressure : `numpy.ndarray`, optional
        The reference pressure against which to calculate the Exner function, defaults to
        metpy.constants.P0

    Returns
    -------
    `numpy.ndarray`
        The value of the Exner function at the given pressure

    See Also
    --------
    potential_temperature
    temperature_from_potential_temperature

    """
    return (pressure / reference_pressure)**kappa


def specific_humidity_from_mixing_ratio(mixing_ratio):
    r"""Calculate the specific humidity from the mixing ratio.

    Parameters
    ----------
    mixing_ratio: `numpy.ndarray`
        mixing ratio

    Returns
    -------
    `numpy.ndarray`
        Specific humidity

    Notes
    -----
    Formula from [Salby1996]_ pg. 118.

    .. math:: q = \frac{w}{1+w}

    * :math:`w` is mixing ratio
    * :math:`q` is the specific humidity

    See Also
    --------
    mixing_ratio, mixing_ratio_from_specific_humidity

    """
    return mixing_ratio / (1 + mixing_ratio)


def virtual_temperature(temperature, mixing_ratio, molecular_weight_ratio=epsilone):
    r"""Calculate virtual temperature.

    This calculation must be given an air parcel's temperature and mixing ratio.
    The implementation uses the formula outlined in [Hobbs2006]_ pg.80.

    Parameters
    ----------
    temperature: `numpy.ndarray`
        air temperature
    mixing_ratio : `numpy.ndarray`
        dimensionless mass mixing ratio
    molecular_weight_ratio : `numpy.ndarray` or float, optional
        The ratio of the molecular weight of the constituent gas to that assumed
        for air. Defaults to the ratio for water vapor to dry air.
        (:math:`\varepsilon\approx0.622`).

    Returns
    -------
    `numpy.ndarray`
        The corresponding virtual temperature of the parcel

    Notes
    -----
    .. math:: T_v = T \frac{\text{w} + \varepsilon}{\varepsilon\,(1 + \text{w})}

    """
    return temperature * ((mixing_ratio + molecular_weight_ratio)
                          / (molecular_weight_ratio * (1 + mixing_ratio)))


def density(pressure, temperature, mixing_ratio, molecular_weight_ratio=epsilone):
    r"""Calculate density.

    This calculation must be given an air parcel's pressure, temperature, and mixing ratio.
    The implementation uses the formula outlined in [Hobbs2006]_ pg.67.

    Parameters
    ----------
    pressure: `numpy.ndarray`
        Total atmospheric pressure
    temperature: `numpy.ndarray`
        air temperature
    mixing_ratio : `numpy.ndarray`
        dimensionless mass mixing ratio
    molecular_weight_ratio : `numpy.ndarray` or float, optional
        The ratio of the molecular weight of the constituent gas to that assumed
        for air. Defaults to the ratio for water vapor to dry air.
        (:math:`\varepsilon\approx0.622`).

    Returns
    -------
    `numpy.ndarray`
        The corresponding density of the parcel

    Notes
    -----
    .. math:: \rho = \frac{p}{R_dT_v}

    """
    virttemp = virtual_temperature(temperature, mixing_ratio, molecular_weight_ratio)
    return (pressure / (R * virttemp)) # 単位はkg m**-3


def relative_humidity_from_mixing_ratio(pressure, temperature, mixing_ratio):
    r"""Calculate the relative humidity from mixing ratio, temperature, and pressure.

    Parameters
    ----------
    pressure: `numpy.ndarray`
        Total atmospheric pressure

    temperature: `numpy.ndarray`
        Air temperature

    mixing_ratio: `numpy.ndarray`
        Dimensionless mass mixing ratio

    Returns
    -------
    `numpy.ndarray`
        Relative humidity

    Notes
    -----
    Formula based on that from [Hobbs1977]_ pg. 74.

    .. math:: RH = \frac{w}{w_s}

    * :math:`relative_humidity` is relative humidity as a unitless ratio
    * :math:`w` is mixing ratio
    * :math:`w_s` is the saturation mixing ratio


    See Also
    --------
    mixing_ratio_from_relative_humidity, saturation_mixing_ratio

    """
    return mixing_ratio / saturation_mixing_ratio(pressure, temperature)


def relative_humidity_from_specific_humidity(pressure, temperature, specific_humidity):
    r"""Calculate the relative humidity from specific humidity, temperature, and pressure.

    Parameters
    ----------
    pressure: `numpy.ndarray`
        Total atmospheric pressure

    temperature: `numpy.ndarray`
        Air temperature

    specific_humidity: `numpy.ndarray`
        Specific humidity of air

    Returns
    -------
    `numpy.ndarray`
        Relative humidity

    Notes
    -----
    Formula based on that from [Hobbs1977]_ pg. 74. and [Salby1996]_ pg. 118.

    .. math:: RH = \frac{q}{(1-q)w_s}

    * :math:`relative_humidity` is relative humidity as a unitless ratio
    * :math:`q` is specific humidity
    * :math:`w_s` is the saturation mixing ratio

    See Also
    --------
    relative_humidity_from_mixing_ratio

    """
    return (mixing_ratio_from_specific_humidity(specific_humidity)
            / saturation_mixing_ratio(pressure, temperature))


def k_index_3d(pressure, temperature, rh):
    r"""相対湿度、気温(およびリファレンスのための気圧)からK指数を計算する。

    Parameters
    ----------
    pressure: `numpy.ndarray`
        Pressure level value

    temperature: `numpy.ndarray`
        Air temperature

    rh: `numpy.ndarray`
        Dimensionless relative humidity

    Returns
    -------
    `numpy.ndarray`
        K index

    Notes
    -----
    Formula based on that from [George1960]

    .. math:: KI = T_{850} - T_{500} + Td_{850} - \left(T_{700} - Td_{700}\right)

    * :math:`KI` is K index  
    * :math:`T` is temperature  
    * :math:`Td` is dew-point temperature
    
    Subscript means its pressure level  

    """
    p500_idx = pressure[np.where(pressure == 500)[0][0]]
    p700_idx = pressure[np.where(pressure == 700)[0][0]]
    p850_idx = pressure[np.where(pressure == 850)[0][0]]
    return temperature[p850_idx, :] - temperature[p500_idx, :] + dewpoint_from_relative_humidity(temperature[p850_idx, :], rh[p850_idx, :]) \
        - (temperature[p700_idx, :] - dewpoint_from_relative_humidity(temperature[p700_idx, :], rh[p850_idx, :]))


def k_index_2d(t850, t700, t500, rh850, rh700):
    r"""相対湿度、気温(およびリファレンスのための気圧)からK指数を計算する。

    Parameters
    ----------
    pressure: `numpy.ndarray`
        Pressure level value

    temperature: `numpy.ndarray`
        Air temperature

    rh: `numpy.ndarray`
        Dimensionless relative humidity

    Returns
    -------
    `numpy.ndarray`
        K Index in Kelvin

    Notes
    -----
    Formula based on that from [George1960]

    .. math:: KI = T_{850} - T_{500} + Td_{850} - \left(T_{700} - Td_{700}\right)

    * :math:`KI` is K index  
    * :math:`T` is temperature  
    * :math:`Td` is dew-point temperature

    Subscript means its pressure level  

    """
    return t850 - t500 + dewpoint_from_relative_humidity(t850, rh850) - (t700 - dewpoint_from_relative_humidity(t700, rh700))


def showalter_stability_index(t850, t500, p850, p500):
    r'''
    500hPaにおける気温から850 hPaから500 hPaに断熱変化させた際の気温を引いた指数。
    この計算では乾燥断熱減率のみを考慮しているため、湿潤断熱変化も含めたSSIを
    求める方法が必要である。
    
    .. math:: SSI = T_{500} - T_{850\rightarrow 500}^*
    '''
    return t500 - potential_temperature(p850, t850)/exner_function(p500)


# def gradient_richardson_number(height, potential_temperature, u, v, vertical_dim=0):
#     r"""Calculate the gradient (or flux) Richardson number.

#     .. math::   Ri = (g/\theta) * \frac{\left(\partial \theta/\partial z\)}
#              {[\left(\partial u / \partial z\right)^2 + \left(\partial v / \partial z\right)^2}

#     See [Holton2004]_ pg. 121-122. As noted by [Holton2004]_, flux Richardson
#     number values below 0.25 indicate turbulence.

#     Parameters
#     ----------
#     height : `numpy.ndarray`
#         Atmospheric height

#     potential_temperature : `numpy.ndarray`
#         Atmospheric potential temperature

#     u : `numpy.ndarray`
#         X component of the wind

#     v : `numpy.ndarray`
#         y component of the wind

#     vertical_dim : int, optional
#         The axis corresponding to vertical, defaults to 0. Automatically determined from
#         xarray DataArray arguments.

#     Returns
#     -------
#     `numpy.ndarray`
#         Gradient Richardson number
#     """
#     dthetadz = first_derivative(potential_temperature, x=height, axis=vertical_dim)
#     dudz = first_derivative(u, x=height, axis=vertical_dim)
#     dvdz = first_derivative(v, x=height, axis=vertical_dim)

#     return (g / potential_temperature) * (dthetadz / (dudz ** 2 + dvdz ** 2))


# def first_derivative(f, axis=None, x=None, delta=None):
#     r"""Calculate the first derivative of a grid of values.

#     Works for both regularly-spaced data and grids with varying spacing.

#     Either `x` or `delta` must be specified, or `f` must be given as an `xarray.DataArray` with
#     attached coordinate and projection information. If `f` is an `xarray.DataArray`, and `x` or
#     `delta` are given, `f` will be converted to a `numpy.ndarray` and the derivative returned
#     as a `numpy.ndarray`, otherwise, if neither `x` nor `delta` are given, the attached
#     coordinate information belonging to `axis` will be used and the derivative will be returned
#     as an `xarray.DataArray`.

#     This uses 3 points to calculate the derivative, using forward or backward at the edges of
#     the grid as appropriate, and centered elsewhere. The irregular spacing is handled
#     explicitly, using the formulation as specified by [Bowen2005]_.

#     Parameters
#     ----------
#     f : array-like
#         Array of values of which to calculate the derivative
#     axis : int or str, optional
#         The array axis along which to take the derivative. If `f` is ndarray-like, must be an
#         integer. If `f` is a `DataArray`, can be a string (referring to either the coordinate
#         dimension name or the axis type) or integer (referring to axis number), unless using
#         implicit conversion to `numpy.ndarray`, in which case it must be an integer. Defaults
#         to 0. For reference, the current standard axis types are 'time', 'vertical', 'y', and
#         'x'.
#     x : array-like, optional
#         The coordinate values corresponding to the grid points in `f`
#     delta : array-like, optional
#         Spacing between the grid points in `f`. Should be one item less than the size
#         of `f` along `axis`.

#     Returns
#     -------
#     array-like
#         The first derivative calculated along the selected axis


#     .. versionchanged:: 1.0
#        Changed signature from ``(f, **kwargs)``

#     See Also
#     --------
#     second_derivative

#     """
#     n, axis, delta = _process_deriv_args(f, axis, x, delta)
#     take = make_take(n, axis)

#     # First handle centered case
#     slice0 = take(slice(None, -2))
#     slice1 = take(slice(1, -1))
#     slice2 = take(slice(2, None))
#     delta_slice0 = take(slice(None, -1))
#     delta_slice1 = take(slice(1, None))

#     combined_delta = delta[delta_slice0] + delta[delta_slice1]
#     delta_diff = delta[delta_slice1] - delta[delta_slice0]
#     center = (- delta[delta_slice1] / (combined_delta * delta[delta_slice0]) * f[slice0]
#               + delta_diff / (delta[delta_slice0] * delta[delta_slice1]) * f[slice1]
#               + delta[delta_slice0] / (combined_delta * delta[delta_slice1]) * f[slice2])

#     # Fill in "left" edge with forward difference
#     slice0 = take(slice(None, 1))
#     slice1 = take(slice(1, 2))
#     slice2 = take(slice(2, 3))
#     delta_slice0 = take(slice(None, 1))
#     delta_slice1 = take(slice(1, 2))

#     combined_delta = delta[delta_slice0] + delta[delta_slice1]
#     big_delta = combined_delta + delta[delta_slice0]
#     left = (- big_delta / (combined_delta * delta[delta_slice0]) * f[slice0]
#             + combined_delta / (delta[delta_slice0] * delta[delta_slice1]) * f[slice1]
#             - delta[delta_slice0] / (combined_delta * delta[delta_slice1]) * f[slice2])

#     # Now the "right" edge with backward difference
#     slice0 = take(slice(-3, -2))
#     slice1 = take(slice(-2, -1))
#     slice2 = take(slice(-1, None))
#     delta_slice0 = take(slice(-2, -1))
#     delta_slice1 = take(slice(-1, None))

#     combined_delta = delta[delta_slice0] + delta[delta_slice1]
#     big_delta = combined_delta + delta[delta_slice1]
#     right = (delta[delta_slice1] / (combined_delta * delta[delta_slice0]) * f[slice0]
#              - combined_delta / (delta[delta_slice0] * delta[delta_slice1]) * f[slice1]
#              + big_delta / (combined_delta * delta[delta_slice1]) * f[slice2])

#     return concatenate((left, center, right), axis=axis)


# def _process_deriv_args(f, axis, x, delta):
#     """Handle common processing of arguments for derivative functions."""
#     n = f.ndim
#     axis = normalize_axis_index(axis if axis is not None else 0, n)

#     if f.shape[axis] < 3:
#         raise ValueError('f must have at least 3 point along the desired axis.')

#     if delta is not None:
#         if x is not None:
#             raise ValueError('Cannot specify both "x" and "delta".')

#         delta = np.atleast_1d(delta)
#         if delta.size == 1:
#             diff_size = list(f.shape)
#             diff_size[axis] -= 1
#             delta_units = getattr(delta, 'units', None)
#             delta = np.broadcast_to(delta, diff_size, subok=True)
#             if not hasattr(delta, 'units') and delta_units is not None:
#                 delta = delta * delta_units
#         else:
#             delta = _broadcast_to_axis(delta, axis, n)
#     elif x is not None:
#         x = _broadcast_to_axis(x, axis, n)
#         delta = np.diff(x, axis=axis)
#     else:
#         raise ValueError('Must specify either "x" or "delta" for value positions.')

#     return n, axis, delta



