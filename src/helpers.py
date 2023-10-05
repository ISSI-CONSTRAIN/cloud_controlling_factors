"""Functions to derieve cloud controling factors."""

import metpy
import metpy.constants as const
import numpy as np
import pint_xarray
from metpy.units import units

gamma_dew_default = units.Quantity(1.8, "K/km")
gamma_dry_default = units.Quantity(9.8, "K/km")


def temperature_advection(SST, u10, v10, lat, lon):
    """

    Input parameters:
    -----------------
    SST: sea surface temperature
    u10: zonal wind speed
    v10: meridional wind speed
    lat: latitude
    lon: longitude
    """
    Re = const.Re

    del_λ = np.gradient(lon)
    del_φ = np.gradient(lat)
    zonal_sst_grad = SST / del_λ
    meridional_sst_grad = SST.transpose("time", "longitude", "latitude") / del_φ

    zonal_adv = u10 / Re * zonal_sst_grad
    meridional_adv = v10 / (Re * np.cos(lat)) * meridional_sst_grad

    T_adv = -zonal_adv - meridional_adv
    return T_adv


def gamma_m(T, p):
    """Moist-adiabatic potential temperature gradient.

    following Wood and Bretherton (2006) Eq.5
    """
    g = const.earth_gravity
    cp = const.Cp_d
    Ra = const.Rd
    Rv = const.Rv
    Lv = const.Lv

    qs = metpy.calc.saturation_mixing_ratio(p, T)

    numerator = 1 + Lv * qs / (Ra * T)
    denumerator = 1 + Lv**2 * qs / (cp * Rv * T**2)
    gamma = g / cp * (1 - numerator / denumerator)
    gamma = gamma.pint.to("K/m")

    return gamma


def gamma_850(T0, T700):
    gamma = gamma_m((T0 + T700) / 2, units.Quantity(850, "hPa"))
    return gamma


def estimated_inversion_strength(T_sfc, T_700, p_sfc, gp_700, rh_sfc):
    gamma = gamma_850(T_sfc, T_700)
    theta_700 = metpy.calc.potential_temperature(units.Quantity(700, "hPa"), T_700)
    theta_sfc = metpy.calc.potential_temperature(p_sfc, T_sfc)
    z700 = metpy.calc.geopotential_to_height(gp_700)
    T_dew_sfc = metpy.calc.dewpoint_from_relative_humidity(T_sfc, rh_sfc)
    LCL = lifting_condensation_level(
        T_sfc, T_dew_sfc, method="simple"
    )  # should be GeorgakakosBras
    LTS = theta_700 - theta_sfc
    EIS = LTS - gamma * (z700 - LCL)
    return EIS


def lifting_condensation_level(
    T,
    T_dew,
    p_sfc=None,
    gamma_dry=gamma_dry_default,
    gamma_dew=gamma_dew_default,
    method="simple",
):
    """Caluclation of LCL.

    Methods
    -------
    simple : Formula of James Espy

    >>> LCL(units.Quantity(20, "degC"), units.Quantity(10, "degC"))
    """

    if method == "simple":
        h_LCL = (T - T_dew) / (gamma_dry - gamma_dew)
        h_LCL = h_LCL.pint.to("meter")
    elif method == "GeorgakakosBras":
        dewpoint_suppression = T - T_dew
        1 / (dewpoint_suppression / 223.15 + 1) ** 3.5 * p_sfc

    return h_LCL
