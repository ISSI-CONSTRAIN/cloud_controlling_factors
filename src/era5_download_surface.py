import argparse
import os

import cdsapi

parser = argparse.ArgumentParser()
parser.add_argument(
    "--output",
    help="output filename",
)
args = parser.parse_args()

if not os.path.exists(os.path.dirname(args.output)):
    os.makedirs(os.path.dirname(args.output))

c = cdsapi.Client()

c.retrieve(
    "reanalysis-era5-single-levels",
    {
        "product_type": "reanalysis",
        "variable": [
            "10m_u_component_of_wind",
            "10m_v_component_of_wind",
            "2m_temperature",
            "sea_surface_temperature",
            "skin_temperature",
            "surface_pressure",
        ],
        "year": [
            "2020",
        ],
        "month": [
            "12",
        ],
        "day": [
            "28",
            "29",
            "30",
            "31",
        ],
        "time": [
            "00:00",
            "01:00",
            "02:00",
            "03:00",
            "04:00",
            "05:00",
            "06:00",
            "07:00",
            "08:00",
            "09:00",
            "10:00",
            "11:00",
            "12:00",
            "13:00",
            "14:00",
            "15:00",
            "16:00",
            "17:00",
            "18:00",
            "19:00",
            "20:00",
            "21:00",
            "22:00",
            "23:00",
        ],
        "format": "netcdf",
        "area": [
            55,
            -90,
            5,
            0,
        ],
    },
    args.output,
)
