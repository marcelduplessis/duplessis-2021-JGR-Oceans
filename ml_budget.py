import scipy
import numpy as np
import xarray as xr
import glidertools as gt
import gsw

def heatflux(Q, mld, rho=1027, Cp=3850):
    return (Q / (rho * Cp * mld)) # units of C/s


def freshwaterflux(E, P, mld, S):
    return (( (E-P) * S ) / mld) # units psu/s


def ekman_transport(dat, dt, grad, rho0=1027):

    f    = np.abs(gsw.f(dat['lat'])) # coriolis s-1
    taux = dat['taux']               # wind stress
    h    = dat['xld_est']            # mixing layer depth
    u10  = dat['u10']                # u-component of the wind
    
    taux[u10<0] = -taux[u10<0]       # make the u-wind stress negative when the wind is blowing westward
    
    dat['ek_vel_v'] = taux / (rho0 * h * f) # caluclate ekman velocity in units of m s-1
    
    dat['ek_trans_dS'] =  (( dat['ek_vel_v'] * dat['dS_'+grad].values)) # mutiply the ekman anomaly (m) to the gradients (g kg-1 m-1) to get g kg-1
    dat['ek_trans_dT'] =  (( dat['ek_vel_v'] * dat['dT_'+grad].values)) # degC
    
    return dat


def entrainment(dat, mld, xld, dt):
    
    mld = gt.cleaning.rolling_window(mld, func=np.mean, window=4) # smoothing window over mld
    xld = gt.cleaning.rolling_window(xld, func=np.mean, window=4) # smoothing window over xld
    
    d_mld = xld-mld # difference between xld and mld
    dh    = np.append(np.array(0), np.diff(mld)).astype(int) # rate of xld deepening in units m, positive = deepening
    
    we = dh/dt    # entrainment velocity is the rate of xld deepening in m/s
    we[we<0]=0    # if the entrainment vel is negative, there is no entrainment
    we[d_mld<0]=0 # if the entrainment vel is negative, there is no entrainment
    
    xld = xld.astype(int).values # make the xld and mld integers
    mld = mld.astype(int).values # make the xld and mld integers

    T_xld = [np.mean([dat.temp.values[i, val], dat.temp.values[i, mld[i]]]) for i, val in enumerate(xld)] # get the mean temperature between the xld and mld
    S_xld = [np.mean([dat.salt.values[i, val], dat.salt.values[i, mld[i]]]) for i, val in enumerate(xld)] # get the mean salinity between the xld and mld

    S_mld = [dat.salt.values[i, val] for i, val in enumerate(mld)] # get the salinity at the mld
    T_mld = [dat.temp.values[i, val] for i, val in enumerate(mld)] # get the temperature at the mld
    
    S_mld_15m = [dat.salt.values[i, val+15] for i, val in enumerate(mld)] # get the salinity 5m below the mld
    T_mld_15m = [dat.temp.values[i, val+15] for i, val in enumerate(mld)] # get the temperature 5m below the mld
    
    S_xld=np.array(S_xld)
    S_mld=np.array(S_mld)
    
    T_xld=np.array(T_xld)
    T_mld=np.array(T_mld)
    
    ent_S = (we*(S_mld_15m - S_mld))/xld 
    ent_T = (we*(T_mld_15m - T_mld))/xld
    
    dat['ent_dS'] = (('time'), ent_S)
    dat['ent_dT'] = (('time'), ent_T)
    
    return dat