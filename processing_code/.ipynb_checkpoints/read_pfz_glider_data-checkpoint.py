import xarray as xr
import numpy as np
import matplotlib as plt
import gsw

dat_pfz = xr.open_dataset('../data/gliders/pfz_slocum_processed_data.nc')

dat_pfz = dat_pfz.rename({'lon': 'longitude','lat': 'latitude'})



