# duplessis-2021-SO-thermohaline
Analysis followed by du Plessis et al - The daily-resolved Southern Ocean mixed layer: regional contrasts assessed using glider observations

At the moment, to implement the code here you need to clone this repository to your local machine.
'git clone https://github.com/marcelduplessis/duplessis-2021-SO-thermohaline.git'

The data can be accessed via ftp. In your terminal,
ftp ssh.roammiz.com
Name: anonymous

No password is required.

The relevant folder is duPlessis_2021

Load this data into the same folder as the repository, ensuring that the folder is named 'data'

Order of processing:

1. Run `read_saz_glider_data.py` and saved to netCDF
2. Run `process_seaglider_data_L1.py` which does a outlier despiking based on a 5-point rolling standard deviation.
