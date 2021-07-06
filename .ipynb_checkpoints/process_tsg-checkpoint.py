import pandas as pd

tsg = pd.read_excel('../data/agulhas_tsg/Agu035_odv.xlsx')

date = pd.to_datetime(tsg.Date+' '+tsg.Time)

tsg = tsg.drop(columns=['Date', 'Time', 'Unnamed: 12', 'Type', 'Cruise'])

tsg['date'] = date
tsg = tsg.set_index(['date'])

tsg = tsg.to_xarray()
i_nat = ~np.isnat(tsg.date) 
tsg = tsg.sel(date=slice(tsg.date[i_nat][0], tsg.date[i_nat][-1]))

tsg.attrs['cruise'] = 'Agu032'
tsg.attrs['ship']   = 'S.A. Agulhas II'
tsg.attrs['owner']  = 'Department of Environmental Affairs, South Africa'
tsg.attrs['instrument']   = 'Thermosalinograph'
tsg.attrs['contact']= 'Marcel van den Berg, marcel@oceanafrica.com'
tsg.attrs['processing'] = 'Level 1 by DEA'
tsg.attrs['time_coverage_start'] = '2018-11-30T13:31:07'
tsg.attrs['time_coverage_end']   = '2019-01-05T03:02:09'

import glidertools as gt

tsg = tsg.sel(date=slice(tsg.date[0], tsg.date[150000]))

s = gt.cleaning.rolling_window(tsg.s, func=np.median, window=100)
s = gt.cleaning.rolling_window(s, func=np.mean, window=100)

t = gt.cleaning.rolling_window(tsg.t2, func=np.median, window=100)
t = gt.cleaning.rolling_window(t, func=np.mean, window=100)

tsg['t_clean'] = (('date'), t)
tsg['s_clean'] = (('date'), s)

tsg_df = tsg.to_dataframe()

tsg_df.to_csv('tsg_df.csv')