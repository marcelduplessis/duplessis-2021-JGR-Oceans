import datetime

def datenum_to_datetime(datenum):
    """
    Convert Matlab datenum into Python datetime.
    :param datenum: Date in datenum format
    :return:        Datetime object corresponding to datenum.
    """
    days = datenum % 1
    return datetime.datetime.fromordinal(int(datenum)) \
           + datetime.timedelta(days=days) \
           - datetime.timedelta(days=366)


import scipy.io

SB_mat = scipy.io.loadmat('/Users/marcel/Google Drive/Projects/buoyancy_flux_paper/data/sailbuoy/marcel_SB_transects.mat')
sb_date = [datenum_to_datetime(d.squeeze()) for d in SB_mat['date'].squeeze()]

sb_data = xr.Dataset(
                 data_vars={'lat' : (('time'), SB_mat['lat'].squeeze()),
                            'lon' : (('time'), SB_mat['lon'].squeeze()),
                            's_ml' : (('time'), SB_mat['salt_filt_movm'].squeeze()),
                            't_ml' : (('time'), SB_mat['temp_filt_movm'].squeeze())},
                 coords={'time': sb_date})


sb_data.to_netcdf('sailbuoy_data.nc')