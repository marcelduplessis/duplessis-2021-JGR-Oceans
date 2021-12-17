def process_seaglider_data_L1(dat):

    import glidertools as gt
    import xarray as xr
    import numpy as np
    from datetime import datetime
    from datetime import timedelta
    import matplotlib.dates as dates
    import gsw
    from scipy.interpolate import griddata

    dat = dat.isel(ctd_data_point=np.arange(len(dat.ctd_data_point))[dat.ctd_depth<300])
    
    # despike based on temperature values larger than the standard deviation for 5 points in a row
    x, spikes = gt.cleaning.despike(dat.temperature_raw, window_size=5)
    thres = np.nanstd(spikes)
    spike_ind=(np.abs(spikes)>thres).values

    dat.temperature_raw[spike_ind]=np.NaN
    dat.salinity_raw[spike_ind]=np.NaN

    # despike based on salinity values larger than the standard deviation for 5 points in a row
    x, spikes = gt.cleaning.despike(dat.salinity_raw, window_size=5)
    thres = np.nanstd(spikes)
    spike_ind=(np.abs(spikes)>thres).values

    dat.temperature_raw[spike_ind]=np.NaN
    dat.salinity_raw[spike_ind]=np.NaN
    
    # remove unrealistically low salinity values
    dat.salinity_raw[dat.salinity_raw<33.8] = np.NaN
    dat.temperature_raw[dat.salinity_raw<33.8] = np.NaN
    
    # convert the raw temperature and salinity to conservative temperature and absolute salinity
    dat['salinity']    = (('ctd_data_point'), gsw.SA_from_SP(dat.salinity_raw, dat.ctd_pressure, dat.longitude, dat.latitude))
    dat['temperature'] = (('ctd_data_point'), gsw.CT_from_t(dat.salinity_raw , dat.temperature_raw , dat.ctd_pressure))
    
    # grid the data and interpolate the vertical grid to 5m
    depth = dat.ctd_depth
    dives = dat.dives
    temp  = dat.temperature
    salt  = dat.salinity
    
    new_dpt = np.arange(0, 305, 5)
    
    t_grid = gt.grid_data(dives, depth, temp, bins=new_dpt, how='median')
    s_grid = gt.grid_data(dives, depth, salt, bins=new_dpt, how='median')
    
    # interpolate to 1m depth intervals and run a 5m running mean
    dat=dat.set_coords(names='dives')
    dat=dat.swap_dims({'ctd_data_point': 'dives'})
    
    dives = np.unique(dat.dives)
    depth = np.arange(0,1000,1)

    salt = np.ndarray([len(depth), len(dives)])
    temp = np.ndarray([len(depth), len(dives)])
    time = []
    lon  = []
    lat  = []
    
    for i, val in enumerate(dives):
        
        dive = dat.sel(dives=val)
        
        x = t_grid.ctd_depth
        t = t_grid[:,i]
        s = s_grid[:,i]
        
        x = x[~np.isnan(t)]
        s = s[~np.isnan(t)]
        t = t[~np.isnan(t)]
        
        x = x[~np.isnan(s)]
        t = t[~np.isnan(s)]
        s = s[~np.isnan(s)]
        
        temp[:,i] = gt.cleaning.rolling_window(griddata(x, t, depth, method='linear'), func=np.mean, window=5)
        salt[:,i] = gt.cleaning.rolling_window(griddata(x, s, depth, method='linear'), func=np.mean, window=5)
        
        if val % 1 == 0:
            t  = dive.ctd_time_dt64.values
            t  = t[~np.isnan(t)][0]
        
            ln = dive.longitude.values
            ln = ln[~np.isnan(ln)][0]
        
            lt = dive.latitude.values
            lt = lt[~np.isnan(lt)][0]
            
        if val % 1 == 0.5:
            t  = dive.ctd_time_dt64.values
            t  = t[~np.isnan(t)][-1]
        
            ln = dive.longitude.values
            ln = ln[~np.isnan(ln)][-1]
        
            lt = dive.latitude.values
            lt = lt[~np.isnan(lt)][-1]
        
        time += t,
        lon  += ln,
        lat  += lt,
        
    time = np.array(time)
    lon  = np.array(lon)
    lat  = np.array(lat)
    
    dat_L1 = xr.Dataset(data_vars={'temp' : (('depth', 'time'), temp),
                                   'salt' : (('depth', 'time'), salt),
                                   'lat'  : (('time'), lat),
                                   'lon'  : (('time'), lon)},
                            coords={'depth': depth, 
                                    'time' : time})

    return dat_L1

