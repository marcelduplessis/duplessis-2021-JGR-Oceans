import xarray as xr
import numpy as np
import matplotlib as plt
import glidertools as gt
import pandas as pd
import gsw

from datetime import datetime
from datetime import timedelta
from scipy.interpolate import griddata

dat_apz = xr.open_dataset('/Users/Marcel/Google Drive/Projects/Regional Comparison/apz_slocum_processed_data.nc')

x, spikes = gt.cleaning.despike(dat_apz.temperature, window_size=5)
thres = np.nanstd(spikes)
spike_ind=(np.abs(spikes)>thres).values

dat_apz.temperature[spike_ind]=np.NaN
dat_apz.salinity[spike_ind]=np.NaN

x, spikes = gt.cleaning.despike(dat_apz.salinity, window_size=5)
thres = np.nanstd(spikes)
spike_ind=(np.abs(spikes)>thres).values

dat_apz.temperature[spike_ind]=np.NaN
dat_apz.salinity[spike_ind]=np.NaN

i = dat_apz.dives>84

dat_apz = dat_apz.where(i)

mask, fig = gt.cleaning.data_density_filter(dat_apz.salinity, dat_apz.ctd_pressure, min_count=200, conv_matrix=[2, 2])

dat_apz.salinity[mask] = np.NaN
dat_apz.temperature[mask] = np.NaN

dat_apz['dens_qc']=gt.physics.potential_density(dat_apz.salinity, dat_apz.temperature, 
                              dat_apz.ctd_pressure, dat_apz.lat, dat_apz.lon)

dat_apz['buoyancy']=-9.81*(dat_apz.dens_qc-1025)/1025

b_apz_grid = gt.grid_data(dat_apz.dives, dat_apz.ctd_pressure, dat_apz.buoyancy, how='median', bins=np.arange(0, 1001, 1))
t_apz_grid = gt.grid_data(dat_apz.dives, dat_apz.ctd_pressure, dat_apz.temperature, how='median', bins=np.arange(0, 1001, 1))
s_apz_grid = gt.grid_data(dat_apz.dives, dat_apz.ctd_pressure, dat_apz.salinity, how='median', bins=np.arange(0, 1001, 1))
d_apz_grid = gt.grid_data(dat_apz.dives, dat_apz.ctd_pressure, dat_apz.dens_qc, how='median', bins=np.arange(0, 1001, 1))
lon_apz_grid = gt.grid_data(dat_apz.dives, dat_apz.ctd_pressure, dat_apz.lon, how='median', bins=np.arange(0, 1001, 1))
lat_apz_grid = gt.grid_data(dat_apz.dives, dat_apz.ctd_pressure, dat_apz.lat, how='median', bins=np.arange(0, 1001, 1))
time_apz_grid = gt.grid_data(dat_apz.dives, dat_apz.ctd_pressure, date2num(dat_apz.time), how='median', bins=np.arange(0, 1001, 1))

N2_apz = -np.diff(b_apz_grid, axis=0)

time_apz = [time_apz_grid[:,i][~np.isnan(time_apz_grid[:,i])][0].values for i in range(len(time_apz_grid.T))]
lon_apz = [lon_apz_grid[:,i][~np.isnan(time_apz_grid[:,i])][0].values for i in range(len(time_apz_grid.T))]
lat_apz = [lat_apz_grid[:,i][~np.isnan(time_apz_grid[:,i])][0].values for i in range(len(time_apz_grid.T))]

date_apz = [datetime.fromordinal(int(val)) + timedelta(days=val%1) for i, val in enumerate(time_apz)]

