import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] = (18,10)
plt.rcParams['ytick.direction'] = 'out'
plt.rcParams['xtick.direction'] = 'out'

font = {'family' : 'Arial',
        'weight' : 'ultralight',
        'size'   : 16}

plt.rc('font', **font)

plt.rc('ytick.major', size=6)
plt.rc('xtick.major', size=6)
plt.rc('ytick.minor', size=4)
plt.rc('xtick.minor', size=4)
plt.rc('lines', linewidth=2)