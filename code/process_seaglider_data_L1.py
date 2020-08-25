def process_seaglider_data_L1(dat_glider):

    import glidertools as gt
    import xarray as xr
    import numpy as np
    from datetime import datetime
    from datetime import timedelta
    import matplotlib.dates as dates

    # despike based on temperature values larger than the standard deviation for 5 points in a row
    x, spikes = gt.cleaning.despike(dat_glider.temperature, window_size=5)
    thres = np.nanstd(spikes)
    spike_ind=(np.abs(spikes)>thres).values

    dat_glider.temperature[spike_ind]=np.NaN
    dat_glider.salinity[spike_ind]=np.NaN

    # despike based on salinity values larger than the standard deviation for 5 points in a row
    x, spikes = gt.cleaning.despike(dat_glider.salinity, window_size=5)
    thres = np.nanstd(spikes)
    spike_ind=(np.abs(spikes)>thres).values

    dat_glider.temperature[spike_ind]=np.NaN
    dat_glider.salinity[spike_ind]=np.NaN
    
    # remove unrealistically low salinity values
    dat_glider.salinity[dat_glider.salinity<33.8] = np.NaN
    dat_glider.temperature[dat_glider.salinity<33.8] = np.NaN
    
    # # data den
    # mask, fig = gt.cleaning.data_density_filter(dat_glider.salinity, dat_glider.ctd_depth, min_count=6, conv_matrix=[3,3])
    # dat_glider.salinity[mask] = np.NaN
    # dat_glider.temperature[mask] = np.NaN

    # dat_glider['dens_qc']=gt.physics.potential_density(dat_glider.salinity, dat_glider.temperature, 
    #                           dat_glider.ctd_depth, dat_glider.latitude, dat_glider.longitude)

    # calculate glider buoyancy
    # dat_glider['buoyancy']=-9.81*(dat_glider.dens_qc-1025)/1025
    
    # grid to 1m depth intervals
    t_grid    = gt.grid_data(dat_glider.dives, dat_glider.ctd_depth, dat_glider.temperature,                   how='median', bins=np.arange(0, 1001, 1))
    s_grid    = gt.grid_data(dat_glider.dives, dat_glider.ctd_depth, dat_glider.salinity,                      how='median', bins=np.arange(0, 1001, 1))
    lon_grid  = gt.grid_data(dat_glider.dives, dat_glider.ctd_depth, dat_glider.longitude,                     how='median', bins=np.arange(0, 1001, 1))
    lat_grid  = gt.grid_data(dat_glider.dives, dat_glider.ctd_depth, dat_glider.latitude,                      how='median', bins=np.arange(0, 1001, 1))
    time_grid = gt.grid_data(dat_glider.dives, dat_glider.ctd_depth, dates.date2num(dat_glider.ctd_time_dt64), how='median', bins=np.arange(0, 1001, 1))

    time = [time_grid[:,i][~np.isnan(time_grid[:,i])][0].values for i in range(len(time_grid.T))]
    lon  = [lon_grid[:,i] [~np.isnan(time_grid[:,i])][0].values for i in range(len(time_grid.T))]
    lat  = [lat_grid[:,i] [~np.isnan(time_grid[:,i])][0].values for i in range(len(time_grid.T))]

    date = [datetime.fromordinal(int(val)) + timedelta(days=val%1) for i, val in enumerate(time)]
    date = np.array(date)

    dat = xr.Dataset(data_vars={'temp' : (('depth', 'time'), t_grid),
                                'salt' : (('depth', 'time'), s_grid)},
        coords={'depth': np.arange(1000), 
                'time' : date,
                'lat'  : lat,
                'lon'  : lon})

    return dat

