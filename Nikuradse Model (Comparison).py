from Functions import *
from os.path import exists

#Creating dictionary for all experiments
experiments = []
experimentConfig = {
    "2v": { 'list': [87, 88]},
    # "4v": { 'list': [1,2,3]},
    # "8v": { 'list': [1,2,3]},
}

#Creating list of all experiments based on configuration in experimentConfig dictionary
for k, v in experimentConfig.items():
    for exp in v.get('list'):
        experiments.append(f'{k}_rescan{exp}')

#Creating dictionary to search for zeroshift experiments
ZeroshiftSearch = dict()
location = r"C:\Users\PipeFlow\Desktop\Experiments\Data\New\Valley"
for experiment in experiments:
    ZeroshiftSearch[experiment] = (f"{location}\{experiment[:2]}\{experiment[3:]}\{'before'}.tdms")

#putting zeroshift experiments in a list and creating dictionary to search for excel experiments
ExcelSearch = dict()
Zeroshifts = []
for k, v in ZeroshiftSearch.items():
    if exists(v):
        Zeroshifts.append(k)
    else:
        for experiment in experiments:
            ExcelSearch[experiment] = f'{location}\{experiment[:2]}\{experiment[3:]}\{experiment[3:]}.xlsx' 

#putting excel experiments in a list
Excels = []
for k, v in ExcelSearch.items():
    if exists(v):
        Excels.append(k)
    else:
        continue

# #putting remaining experiments in a list
# Remainder = [x for x in experiments if x not in Zeroshifts]
# Regular = [x for x in Remainder if x not in Excels]

#------------------------------64/re & Blasius
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
#-----------------------------------------------------Graph

#Plots for zeroshift experiments
if Zeroshifts:
    ZeroShiftResults = dict()
    for Zeroshift in Zeroshifts:
        ZeroShiftResults[Zeroshift] = Process_ZeroShift_Experiment(Zeroshift[:2], Zeroshift[3:])
        ZeroShiftResults[Zeroshift] = ZeroShiftResults[Zeroshift]
    print(ZeroShiftResults)
    legendEntries = []
    for Zeroshift, ZeroShiftResults in ZeroShiftResults.items():
        before, actual, after = [ZeroShiftResults[x] for x in ['before', 'actual', 'after']]
        before = before.iloc[1:]
        plt.plot(before)
        legendEntries.append('Transducer (%s)' % Zeroshift)
else:
    print("No zeroshift experiments found.")

#Plots for excel experiments
if Excels:
    ExcelResults = dict()
    for Excel in Excels:
        ExcelResults[Excel] = Process_Excel_Experiemnt(Excel[:2], Excel[3:])
    print(ExcelResults)
    for Excel, ExcelResults in ExcelResults.items():
        Friction = [ExcelResults[x] for x in ['Friction']]
        plt.plot(ExcelResults)
        legendEntries.append('Monometer (%s)' % Excel)
else:
    print("No excel experiments found.")

legendEntries.append('64/Re')
legendEntries.append('Blasius')


plt.plot(lam)
plt.plot(tur)
plt.xlabel('log Re')
plt.ylabel('log f')
plt.legend(legendEntries)
plt.grid() 
plt.show()