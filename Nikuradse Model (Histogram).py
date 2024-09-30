from Functions import *
from MainConfigurationFile import path


#Filtering through experiments to return only developed experiments
Excel = pd.read_excel(path)
DevelopedExperiments = Excel.loc[Excel['Developed'] == 'Yes']

#list of all experiments itterations that had a fully developed flow
DevelopedItteration = DevelopedExperiments['Experiment'].to_list()

#creating dictionary and array for all experiments
experiments = []
experimentsConfig = {"2v": { 'list': DevelopedItteration},}

#Creating list of all experiments based on configuration in experimentConfig dictionary
for a, b in experimentsConfig.items():
    for itt in b.get('list'):
        experiments.append(f'{a}_rescan{itt}')

#Calculating friction factor for all experiments
counter = len(experiments)
currentIndex = 0
a = pd.DataFrame()
reynolds = []
friction = []
while currentIndex < counter:
    experiment = experiments[currentIndex]
    Data = Process_ZeroShift_Experiment(experiment[:2], experiment[3:])['before'].reset_index()
    reynolds += Data['Reynolds Number'].tolist()
    friction += Data['Friction Factor'].tolist()
    currentIndex += 1

#creating dataframe for calculated experiments
allexperiments = pd.DataFrame()
allexperiments['Reynolds Number'] = reynolds
allexperiments['Friction Factor'] = friction

#filtering experiments that lay on the constant line
constant = allexperiments.loc[allexperiments['Reynolds Number'] >= 3.8].set_index('Reynolds Number')


#-------------------------------------------------------------------------------------------------------NIKURADSE
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

#creating dictionary to store nikuradse graphs
experimentResults = dict()
for experiment in experiments:
    experimentResults[experiment] = Process_ZeroShift_Experiment(experiment[:2], experiment[3:])
legendEntries = []


#Creating subplot graph and adding the histogram
fig, ax = plt.subplots(2, 1, figsize = (6,4))
constant['Friction Factor'].plot(kind = 'hist', density = True, bins= 10)
constant['Friction Factor'].plot(kind='kde')
ax[1].set_xlabel('Friction Factor')
ax[1].set_xlim(-1.135, -1.1)
ax[1].set_ylim(0,100)
ax[1].set_yticks([])
ax[1].tick_params(left=False, bottom=False)
plt.style.use("bmh")


#populating nikuradse plots
for experiment, experimentResult in experimentResults.items():
        before, actual, after = [experimentResult[x] for x in ['before', 'actual', 'after']]
        before = before.iloc[1:]
        ax[0].plot(before)
        legendEntries.append('Transducer (%s)' % experiment)



#adding nikuradse graph to subplot
ax[0].plot(tur)
ax[0].plot(lam)
ax[0].set_ylabel('Friction Factor')
ax[0].set_xlabel('Reynolds Number')
ax[0].grid()
ax[0].legend(legendEntries)
plt.show()