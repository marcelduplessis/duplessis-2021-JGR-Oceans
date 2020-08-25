import xarray as xr
import numpy as np
import matplotlib as plt
import glidertools as gt
import pandas as pd
import gsw

from datetime import datetime
from datetime import timedelta
from scipy.interpolate import griddata

pathMIZ = '/Users/marcel/Google Drive/Projects/buoyancy_flux_paper/data/SG643/*.nc'

names = [
    'ctd_depth',
    'ctd_time',
    'ctd_pressure',
    'salinity',
    'temperature'
]

ds_dict = gt.load.seaglider_basestation_netCDFs(
    pathMIZ, names,
    return_merged=True,
    keep_global_attrs=False
)

dat_miz = ds_dict['ctd_data_point']

# dat_miz = xr.open_dataset('/Users/Marcel/Google Drive/Projects/Regional Comparison/miz_sg_processed_data.nc')

x, spikes = gt.cleaning.despike(dat_miz.temperature, window_size=5)
thres = np.nanstd(spikes)
spike_ind=(np.abs(spikes)>thres).values

dat_miz.temperature[spike_ind]=np.NaN
dat_miz.salinity[spike_ind]=np.NaN

x, spikes = gt.cleaning.despike(dat_miz.salinity, window_size=5)
thres = np.nanstd(spikes)
spike_ind=(np.abs(spikes)>thres).values

dat_miz.temperature[spike_ind]=np.NaN
dat_miz.salinity[spike_ind]=np.NaN

mask, fig = gt.cleaning.data_density_filter(dat_miz.salinity, dat_miz.ctd_depth, min_count=20, conv_matrix=[2, 2])
dat_miz.salinity[mask] = np.NaN
dat_miz.temperature[mask] = np.NaN

dat_miz['dens_qc']=gt.physics.potential_density(dat_miz.salinity, dat_miz.temperature, 
                              dat_miz.ctd_depth, dat_miz.latitude, dat_miz.longitude)

dat_miz['buoyancy']=-9.81*(dat_miz.dens_qc-1025)/1025

b_miz_grid = gt.grid_data(dat_miz.dives, dat_miz.ctd_depth, dat_miz.buoyancy, how='median', bins=np.arange(0, 1001, 1))
t_miz_grid = gt.grid_data(dat_miz.dives, dat_miz.ctd_depth, dat_miz.temperature, how='median', bins=np.arange(0, 1001, 1))
s_miz_grid = gt.grid_data(dat_miz.dives, dat_miz.ctd_depth, dat_miz.salinity, how='median', bins=np.arange(0, 1001, 1))
d_miz_grid = gt.grid_data(dat_miz.dives, dat_miz.ctd_depth, dat_miz.dens_qc, how='median', bins=np.arange(0, 1001, 1))
lon_miz_grid = gt.grid_data(dat_miz.dives, dat_miz.ctd_depth, dat_miz.longitude, how='median', bins=np.arange(0, 1001, 1))
lat_miz_grid = gt.grid_data(dat_miz.dives, dat_miz.ctd_depth, dat_miz.latitude, how='median', bins=np.arange(0, 1001, 1))
time_miz_grid = gt.grid_data(dat_miz.dives, dat_miz.ctd_depth, date2num(dat_miz.ctd_time_dt64), how='median', bins=np.arange(0, 1001, 1))

N2_miz = -np.diff(b_miz_grid, axis=0)

time_miz = [time_miz_grid[:,i][~np.isnan(time_miz_grid[:,i])][0].values for i in range(len(time_miz_grid.T))]
lon_miz = [lon_miz_grid[:,i][~np.isnan(time_miz_grid[:,i])][0].values for i in range(len(time_miz_grid.T))]
lat_miz = [lat_miz_grid[:,i][~np.isnan(time_miz_grid[:,i])][0].values for i in range(len(time_miz_grid.T))]

date_miz = [datetime.fromordinal(int(val)) + timedelta(days=val%1) for i, val in enumerate(time_miz)]
