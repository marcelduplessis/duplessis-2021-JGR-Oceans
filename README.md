# buoyancy_flux_paper
All code and data linked to the buoyancy_flux manuscript here.

Data used in this study:

- Ocean glider data from ROAM-MIZ and SOSCEx.
- EN4 data
- Sailbuoy data from ROAM-MIZ
- Thermosalinograph data from the S.A. Agulhas II
- Wind, precipitation, evaporation, heat fluxes from ERA5, JRA55 and CFSv2.

To do:

- Upload working glider processing code.
- Figure 1. Map and overview.
- Figure 2. Characterise meridional upper ocean structure from EN4.2.1 observations.
- Figure 3. Characterise 
- Figure 4.
- Figure 5.
- Figure 6.

Order of processing:

1. Run `read_saz_glider_data.py` and saved to netCDF
2. Run `process_seaglider_data_L1.py` which does a outlier despiking based on a 5-point rolling standard deviation.
