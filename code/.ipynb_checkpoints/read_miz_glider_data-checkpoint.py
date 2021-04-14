import xarray as xr
import numpy as np
import matplotlib as plt
import glidertools as gt
import pandas as pd

pathMIZ = '/Users/marcel/Google Drive/Projects/buoyancy_flux_paper/data/gliders/SG643/*.nc'

names = [
    'ctd_depth',
    'ctd_time',
    'ctd_pressure',
    'salinity_raw',
    'temperature_raw',
    'salinity_qc',
    'temperature_qc'
]

ds_dict = gt.load.seaglider_basestation_netCDFs(
    pathMIZ, names,
    return_merged=True,
    keep_global_attrs=False
)

dat_miz = ds_dict['ctd_data_point']

# dat_miz = dat_miz.rename({
#     'salinity_raw': 'salinity'
# })