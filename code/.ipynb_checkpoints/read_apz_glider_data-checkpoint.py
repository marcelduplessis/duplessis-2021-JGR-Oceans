import xarray as xr
import numpy as np
import matplotlib as plt
import gsw

dat_apz = xr.open_dataset('/Users/marcel/Google Drive/Projects/buoyancy_flux_paper/data/gliders/apz_slocum_processed_data.nc')

# i = dat_apz.dives>84
# dat_apz = dat_apz.where(i)

# dat_apz['ctd_depth'] = (('time'), np.abs(gsw.z_from_p(dat_apz.ctd_pressure, dat_apz.lat)))
dat_apz = dat_apz.rename({'lon': 'longitude','lat': 'latitude'})



