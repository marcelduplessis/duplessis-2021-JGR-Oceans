import xarray as xr
import numpy as np
import matplotlib as plt
import glidertools as gt
import pandas as pd

# define path of where the data is
pathSAZ = '../data/gliders/SG542_SAZ_2019/*.nc'

# define the variables to load
names = [
    'ctd_depth',
    'ctd_time',
    'ctd_pressure',
    'salinity_raw',
    'temperature_raw',
    'salinity_qc',
    'temperature_qc'
]

# load the data using glidertools
ds_dict = gt.load.seaglider_basestation_netCDFs(
    pathSAZ, names,
    return_merged=True,
    keep_global_attrs=False
)


dat_saz = ds_dict['ctd_data_point']

