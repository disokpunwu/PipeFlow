from Functions import *

#path = r'C:\Users\PipeFlow\Desktop\Research\20240517Rotation\20240802\Fully Developed Experiments.xlsx'
path = os.path.join(os.curdir, 'Fully Developed Experiments.xlsx')

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
    roughness = experiment[:2]
    iteration = experiment[3:]
    
    Data = Process_ZeroShift_Experiment(roughness, iteration)['before'].reset_index()
    reynolds += Data['Reynolds Number'].tolist()
    friction += Data['Friction Factor'].tolist()
    currentIndex += 1

#creating dataframe for calculated experiments
allexperiments = pd.DataFrame()
allexperiments['Reynolds Number'] = reynolds
allexperiments['Friction Factor'] = friction

#filtering experiments that lay on the constant line
constant = allexperiments.loc[allexperiments['Reynolds Number'] >= 3.8].set_index('Reynolds Number')


print(len(constant))


fig, ax = plt.subplots(2, 1, figsize = (6,4))
constant['Friction Factor'].plot(kind = 'hist', density = True, bins= 10)
constant['Friction Factor'].plot(kind='kde')
ax.set_xlabel('Friction Factor')
ax.set_xlim(-1.135, -1.1)
ax.set_ylim(0,100)
ax.set_yticks([])
ax.tick_params(left=False, bottom=False)
for ax, spine in ax.spines.items():
    spine.set_visible(False)
plt.style.use("bmh")
plt.show()