import matplotlib.dates as mdates
import matplotlib
days = mdates.DayLocator(interval=1)  # every month
years = mdates.YearLocator()   # every year
months = mdates.MonthLocator(interval=1)  # every month
weeks = mdates.WeekdayLocator(interval=1)
yearsFmt = mdates.DateFormatter("%d.%m")

matplotlib.rcParams['figure.figsize'] = (18,10)
matplotlib.rcParams['ytick.direction'] = 'in'
matplotlib.rcParams['xtick.direction'] = 'in'

font = {'family' : 'Arial',
        'weight' : 'ultralight',
        'size'   : 14}

matplotlib.rc('font', **font)

matplotlib.rc('ytick.major', size=6)
matplotlib.rc('xtick.major', size=6)
matplotlib.rc('ytick.minor', size=4)
matplotlib.rc('xtick.minor', size=4)
matplotlib.rc('lines', linewidth=2.5)