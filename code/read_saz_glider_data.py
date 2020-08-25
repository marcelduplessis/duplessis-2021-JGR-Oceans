import xarray as xr
import numpy as np
import matplotlib as plt
import glidertools as gt
import pandas as pd
import gsw

from datetime import datetime
from datetime import timedelta
from scipy.interpolate import griddata

# dat_saz = xr.open_dataset('/Users/Marcel/Google Drive/Projects/Regional Comparison/saz_sg_processed_data.nc')

pathSAZ = '/Users/marcel/Google Drive/Projects/Regional Comparison/Data/SG542_SAZ_2019/*.nc'

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

x, spikes = gt.cleaning.despike(dat_saz.temperature, window_size=5)
thres = np.nanstd(spikes)
spike_ind=(np.abs(spikes)>thres).values

dat_saz.temperature[spike_ind]=np.NaN
dat_saz.salinity[spike_ind]=np.NaN

x, spikes = gt.cleaning.despike(dat_saz.salinity, window_size=5)
thres = np.nanstd(spikes)
spike_ind=(np.abs(spikes)>thres).values

dat_saz.temperature[spike_ind]=np.NaN
dat_saz.salinity[spike_ind]=np.NaN

dat_saz.salinity[dat_saz.salinity<33.8] = np.NaN
dat_saz.temperature[dat_saz.salinity<33.8] = np.NaN

mask, fig = gt.cleaning.data_density_filter(dat_saz.salinity, dat_saz.ctd_depth, min_count=6, conv_matrix=[3,3])
dat_saz.salinity[mask] = np.NaN
dat_saz.temperature[mask] = np.NaN

dat_saz['dens_qc']=gt.physics.potential_density(dat_saz.salinity, dat_saz.temperature, 
                              dat_saz.ctd_depth, dat_saz.latitude, dat_saz.longitude)

dat_saz['buoyancy']=-9.81*(dat_saz.dens_qc-1025)/1025

b_saz_grid = gt.grid_data(dat_saz.dives, dat_saz.ctd_depth, dat_saz.buoyancy, how='median', bins=np.arange(0, 1001, 1))
t_saz_grid = gt.grid_data(dat_saz.dives, dat_saz.ctd_depth, dat_saz.temperature, how='median', bins=np.arange(0, 1001, 1))
s_saz_grid = gt.grid_data(dat_saz.dives, dat_saz.ctd_depth, dat_saz.salinity, how='median', bins=np.arange(0, 1001, 1))
d_saz_grid = gt.grid_data(dat_saz.dives, dat_saz.ctd_depth, dat_saz.dens_qc, how='median', bins=np.arange(0, 1001, 1))
lon_saz_grid = gt.grid_data(dat_saz.dives, dat_saz.ctd_depth, dat_saz.longitude, how='median', bins=np.arange(0, 1001, 1))
lat_saz_grid = gt.grid_data(dat_saz.dives, dat_saz.ctd_depth, dat_saz.latitude, how='median', bins=np.arange(0, 1001, 1))
time_saz_grid = gt.grid_data(dat_saz.dives, dat_saz.ctd_depth, date2num(dat_saz.ctd_time_dt64), how='median', bins=np.arange(0, 1001, 1))

N2_saz = -np.diff(b_saz_grid, axis=0)

time_saz = [time_saz_grid[:,i][~np.isnan(time_saz_grid[:,i])][0].values for i in range(len(time_saz_grid.T))]
lon_saz = [lon_saz_grid[:,i][~np.isnan(time_saz_grid[:,i])][0].values for i in range(len(time_saz_grid.T))]
lat_saz = [lat_saz_grid[:,i][~np.isnan(time_saz_grid[:,i])][0].values for i in range(len(time_saz_grid.T))]

date_saz = [datetime.fromordinal(int(val)) + timedelta(days=val%1) for i, val in enumerate(time_saz)]
