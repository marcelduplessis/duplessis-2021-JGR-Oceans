import xarray as xr
import numpy as np
import matplotlib as plt
import glidertools as gt
import pandas as pd

pathSAZ = '/Users/marcel/Google Drive/Projects/buoyancy_flux_paper/data/SG542_SAZ_2019/*.nc'

names = [
    'ctd_depth',
    'ctd_time',
    'ctd_pressure',
    'salinity_raw',
    'temperature'
]

ds_dict = gt.load.seaglider_basestation_netCDFs(
    pathSAZ, names,
    return_merged=True,
    keep_global_attrs=False
)

dat_saz = ds_dict['ctd_data_point']

dat_saz = dat_saz.rename({
    'salinity_raw': 'salinity'
})
