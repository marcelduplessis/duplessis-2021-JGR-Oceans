import xarray as xr
import numpy as np

### read in the data

pathToFile = '/Volumes/GoogleDrive/My Drive/Projects/duplessis-2021-SO-thermohaline/data/seaice/AMSR2_daily/'

seaice = xr.open_mfdataset(pathToFile+'asi*.hdf',
                            concat_dim='time', combine='nested', engine='h5netcdf')


### do some reorganising to make life easier


seaice_lnlt = xr.open_dataset(pathToFile+'LongitudeLatitudeGrid-s6250-Antarctic.hdf', engine='h5netcdf')

seaice['time'] = (('time'), pd.date_range(start='2018-01-01', end='2019-03-31', freq='D'))

seaice = seaice.rename({'ASI Ice Concentration': 'si_conc'})
seaice = seaice.assign_coords(lon=(["x", "y"], np.array(seaice_lnlt.Longitudes)))
seaice = seaice.assign_coords(lat=(["x", "y"], np.array(seaice_lnlt.Latitudes)))
seaice = seaice.assign(si=(["time", "x", "y"], seaice.si_conc.values))
seaice = seaice.drop('si_conc')

### now do the gridding

seaice_subset = seaice.sel(time=slice('2018-07-01', '2019-03-31')) # define some dates you wish, try squeeze to only the dates you need

from scipy.interpolate import griddata as g
from tqdm import tqdm

X = np.arange(-180, 180.1, 0.1) # your longitudes you want to grid to
Y = np.arange(-70, -49.9, 0.1) # your latitudies you want to grid to

x, y = np.meshgrid(X,Y)

sic_new = np.ndarray([len(seaice_subset.si), len(Y), len(X)]) # setting a new sic array

x_, y_ = np.ravel(seaice_subset.lon), np.ravel(seaice_subset.lat)
x_[x_>180] = x_[x_>180]-360

for i in tqdm(range(len(seaice_subset.si))):

    si = np.ravel(seaice_subset.si[i, :, :].values)
    sic_new[i, :, :] = g((y_, x_), si, (y, x), method='nearest')
     
sic_new[sic_new==0] = np.NaN
sic_new = np.ma.masked_invalid(sic_new)

sic = xr.Dataset(data_vars={'sic' : (('time', 'lat', 'lon'), sic_new)},
                 coords={'time' : seaice_subset.time, 
                         'lat'  : Y, 
                         'lon'  : X})

path = '/Volumes/GoogleDrive/My Drive/Projects/duplessis-2021-SO-thermohaline/data/seaice/'
sic.to_netcdf(path+'sic_interp.nc')