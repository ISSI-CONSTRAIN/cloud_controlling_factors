"""Derieve cloud-controlling factors and create a joint dataset."""

import argparse
import sys

import metpy
import xarray as xr
from metpy.units import units

sys.path.append("./src/")
import helpers as h  # noqa: E402

parser = argparse.ArgumentParser()
parser.add_argument(
    "--input_sfc",
    help="surface filename",
)
parser.add_argument(
    "--input_plev",
    help="pressure level filename",
)
parser.add_argument(
    "--output",
    help="output filename",
)
args = parser.parse_args()

output_vars = ["EIS", "w700", "t_adv", "sst", "skt", "rh700"]


ds_sfc = xr.open_dataset(args.input_sfc)
ds_plevel = xr.open_dataset(args.input_plev)
ds = xr.merge([ds_sfc, ds_plevel])

t_adv = h.temperature_advection(ds.sst, ds.u10, ds.v10, ds.latitude, ds.longitude)

wspd = metpy.calc.wind_speed(ds.u10, ds.v10)

t_sfc = ds.t2m.pint.quantify()
t_700 = ds.t.pint.quantify()
p_sfc = ds.sp.pint.quantify()
gp_700 = ds.z.pint.quantify()
EIS = h.estimated_inversion_strength(
    t_sfc, t_700, p_sfc, gp_700, units.Quantity(80, "percent")
)

ds["t_adv"] = t_adv
ds["EIS"] = EIS
ds["wsp"] = wspd
ds = ds.rename({"r": "rh700", "w": "w700"})

ds = ds.pint.dequantify()
ds[output_vars].to_zarr(args.output, mode="w")
