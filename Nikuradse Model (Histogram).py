from Functions import *

#function to calulate friction factor
def Process_ZeroShift_Experiment(roughness, itteration):
    # locating file data
    location = r"C:\Users\PipeFlow\Desktop\Experiments\Data\New\Valley"
    experiment = (f"{roughness}_{itteration}")
    beforepath = (f"{location}\{roughness}\{itteration}\{'before'}.tdms")
    path = (f"{location}\{roughness}\{itteration}\{itteration}.tdms")
    afterpath = (f"{location}\{roughness}\{itteration}\{'after'}.tdms")
    # calculating mean zero-shift before and after experiment
    before = tdms_df(beforepath)
    before = before['Validyne 6-32'].mean()
    after = tdms_df(afterpath)
    after = after['Validyne 6-32'].mean()
    #applying the zeroshift to the data
    beforezeroshift = process_experiment(experiment, zeroshift= before)
    beforezeroshift = beforezeroshift['rough']
    beforezeroshift = beforezeroshift.reset_index()
    nozeroshift = process_experiment(experiment)
    nozeroshift = nozeroshift['rough']
    afterzeroshift = process_experiment(experiment, zeroshift= after)
    afterzeroshift = afterzeroshift['rough']
    result = beforezeroshift

    return result

#path to excel file with developed status of experiments
path = r'C:\Users\PipeFlow\Desktop\Research\20240517Rotation\20240802\Fully Developed Experiments.xlsx'

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
    Data = Process_ZeroShift_Experiment(experiment[:2], experiment[3:])
    reynolds.append(Data['Reynolds Number'].tolist())
    friction.append(Data['Friction Factor'].tolist())
    currentIndex += 1
reynoldsnumber = [item for sublist in reynolds for item in sublist]
reynoldsnumber = np.array(reynoldsnumber)
reynoldsnumber = reynoldsnumber.flatten()
frictionfactor = [item for sublist in friction for item in sublist]
frictionfactor = np.array(frictionfactor)
frictionfactor = frictionfactor.flatten()

#creating dataframe for calculated experiments
allexperiments = pd.DataFrame()
allexperiments['Reynolds Number'] = reynoldsnumber
allexperiments['Friction Factor'] = frictionfactor

#filtering experiments that lay on the constant line
constant = allexperiments.loc[allexperiments['Reynolds Number'] >= 3.8].set_index('Reynolds Number')

#constant = constant['Friction Factor'].round(2)
print(constant)


fig, ax = plt.subplots(figsize = (6,4))
constant['Friction Factor'].plot(kind = 'hist', density = True, bins= 10)
constant['Friction Factor'].plot(kind='kde')
ax.set_xlabel('Friction Factor')
ax.set_xlim(-1.135, -1.1)
#ax.set_ylabel('Frequency')
ax.set_ylim(0,100)
ax.set_yticks([])
ax.tick_params(left=False, bottom=False)
for ax, spine in ax.spines.items():
    spine.set_visible(False)
plt.style.use("bmh")
plt.show()