from scipy import interpolate
import xarray as xr
import numpy as np
import glidertools as gt


def adjust_lon_xr_dataset(ds, lon_name='lon'):
    
    # whatever name is in the data - lon_name = 'lon'  

    # Adjust lon values to make sure they are within (-180, 180)
    ds['_longitude_adjusted'] = xr.where(
        ds[lon_name] > 180,
        ds[lon_name] - 360,
        ds[lon_name])
    
    # reassign the new coords to as the main lon coords
    # and sort DataArray using new coordinate values
    ds = (
        ds
        .swap_dims({lon_name: '_longitude_adjusted'})
        .sel(**{'_longitude_adjusted': sorted(ds._longitude_adjusted)})
        .drop(lon_name))
    
    ds = ds.rename({'_longitude_adjusted': lon_name})
    
    return ds



def convert_era5_to_Wm2(ds, var_name):
    
    # converts the era5 data, which comes in J m-2 to a W m02
    
    for var in var_name:
        
        ds[var] = (('time', 'latitude', 'longitude'), ds[var]/3600)
        
    return ds


def interp_glider_era5(glider_data, era5_data, var, kind='linear'):

    era5_gl = era5_data.sel(time=glider_data.time)

    x = era5_data.longitude.values
    y = era5_data.latitude.values
        
    for i, val in enumerate(glider_data.time):
         
        z = era5_gl[var].sel(time=val)
        f = interpolate.interp2d(x, y, z, kind=kind)
    
        xnew = glider_data.sel(time=val, depth=0).lon
        ynew = glider_data.sel(time=val, depth=0).lat
        
        if i==0:
            znew = f(xnew, ynew)
        
        if i>0:
            znew = np.append(znew, f(xnew, ynew))
            
    return znew



def dens(salt, temp, depth, lat, lon, time):
    
    dens0  = np.ndarray(np.shape(salt))
    
    for i in range(len(time)):
        
        dens0[:,i] = gt.physics.potential_density(salt[:, i], temp[:, i], depth, np.tile(lat[i], len(depth)), np.tile(lon[i], len(depth)))

    return dens0



def mld(dens, depth, time, thresh=0.03):
    
    mld = np.ndarray(np.shape(time))
    
    for i in range(len(time)):

            mld[i]  = gt.physics.mixed_layer_depth(np.tile(0, len(depth)), depth, dens[:, i], thresh=thresh)

    return mld


def calc_mld(var, dpt, den_lim=0.03, ref_dpt=10):

    """Calculate the mixed layer depth from the density/temperature difference method

    Args:
      var: temperature or density data file
      dpt: depth data

    Return:
        time series of the mixed layer depth

    Dependencies:
        numpy

    """
    import numpy as np

    mld = []
    for i, prof in enumerate(np.arange(len(var))):

        try:
            ref_dpt_ind = np.nanargmin(np.abs(dpt - ref_dpt))
            rho_diff = np.abs(var[prof, ref_dpt_ind:] - var[prof, ref_dpt_ind])
            x = rho_diff - den_lim
            x = np.squeeze(np.where(x > 0))[0]
            mld_ind = x + ref_dpt_ind
            mld += dpt[mld_ind],

        except:
            mld += np.NaN,
            print('MLD not calculated: profile ' + str(i) + '. Setting to NaN')

    return mld