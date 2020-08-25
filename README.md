# buoyancy_flux_paper
All code and data linked to the buoyancy_flux manuscript here.

To do:

- Upload working glider processing code.
- Figure 1. Map and overview.
- Figure 2. 
- Figure 3. 
- Figure 4.
- Figure 5.
- Figure 6.

Order of processing:

1. Run `read_saz_glider_data.py` and saved to netCDF
2. Run `process_seaglider_data_L1.py` which does a outlier despiking based on a 5-point rolling standard deviation.