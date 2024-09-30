from Functions import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from MainConfigurationFile import experimentConfig, experiments

for k, v in experimentConfig.items():
    if v.get('first') and v.get('last'):
        for ind in range(v.get('first'), v.get('last')+1):
            experiments.append(f'{k}_rescan{ind}')
    elif v.get('list'):
        for ind in v.get('list'):
            experiments.append(f'{k}_rescan{ind}')
    else:
        print(f'Experiment {k} does not have a first and last index, or a list')


#-----------------------------------------------------------------------------------------------64/re & Blasius
#reynolds range
num = np.arange(100,31600,100)
num1 = np.arange(1200,31600,100)

#64/re line
lam = pd.DataFrame(num, columns=['Reynolds Number'])
lam['64/re'] = 64/lam['Reynolds Number']
lam = np.log10(lam)
lam = lam.set_index('Reynolds Number')

#Blasius line
tur = pd.DataFrame(num1, columns=['Reynolds Number'])
tur['blasius'] = .316/(tur['Reynolds Number']**.25)
tur = np.log10(tur)
tur = tur.set_index('Reynolds Number')

#-----------------------------------------------------------------------------------------------Graph

results = dict()
for experiment in experiments:
    results[experiment] = Process_ZeroShift_Experiment(experiment[:2], experiment[3:])
print(results)
legendEntries = []
for experiment, result in results.items():
    before, actual, after = [result[x] for x in ['before', 'actual', 'after']]
    # plt.plot(smooth)
    # legendEntries.append("Smooth (%s)" % experiment)
    plt.plot(before)
    legendEntries.append('Rough (%s)' % experiment)

legendEntries.append('64/Re')
legendEntries.append('Blasius')
print(before)
plt.plot(lam)
plt.plot(tur)
plt.xlabel('log Re')
plt.ylabel('log f')
plt.legend(legendEntries)
plt.grid() 
plt.show()