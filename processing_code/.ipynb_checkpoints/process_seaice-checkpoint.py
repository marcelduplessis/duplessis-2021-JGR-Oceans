import xarray as xr
from tqdm import tqdm_notebook
import pandas as pd

import sys
sys.path.append('../') # note here that this path is directed to where the seaice_func.py file is
import seaice_funcs as si

def process(dataPath='/Volumes/GoogleDrive/My Drive/Projects/duplessis-2021-SO-thermohaline/data/seaice/AMSR2_daily/'): # choose the datapath where the files currently are sitting
        
    # read in the AMSR2 sea ice data
    seaice = si.read_AMSR2_seaice(dataPath)
    
    # regrid the curvilinear grid to linear
    sic = si.regrid_linear(seaice)
    
    # save the sic data to netcdf so that you don't have to go through this slow process again
    sic.to_netcdf('/Volumes/GoogleDrive/My Drive/Projects/duplessis-2021-SO-thermohaline/data/seaice/sic_interp.nc')
    
    return