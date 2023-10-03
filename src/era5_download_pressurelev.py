import cdsapi

c = cdsapi.Client()

c.retrieve(
    "reanalysis-era5-pressure-levels",
    {
        "product_type": "reanalysis",
        "format": "netcdf",
        "pressure_level": "700",
        "variable": [
            "geopotential",
            "temperature",
            "relative_humidity",
            "vertical_velocity",
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
        "area": [
            55,
            -90,
            0,
            0,
        ],
        "year": [
            "2020",
        ],
    },
    "download.nc",
)
