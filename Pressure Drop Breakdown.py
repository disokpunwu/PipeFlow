from Functions import *

#fetching file data
roughness = ''
experiment = ''
#Retrieve Data from Experiment
actualpath = getExperimentPath(roughness, experiment)
pressure = tdms_df(actualpath)

#notes from experiment
StartTimes      = []
EndTimes        = []
ReservoirHeight = []
EntryPressure   = []
ExitPressure    = []

#calculating reynolds number
reynolds = reynolds_number(pressure)
reynolds = reynolds.reset_index()
reynolds = reynolds.rename(columns={'Flow Rate Time':'Pressure Time'})
reynolds = reynolds.set_index('Pressure Time')
reynolds = reynolds.rolling(10).mean()

#defining the steps for the loop
Step = len(StartTimes)
itter = 1

#creating the lists for data to be stored in
rnumber = []
rms = []
pdrop = []
beforep = []
duringp = []
afterp = []

#loop
while itter <= Step:
    First= StartTimes[itter-1]
    Last = EndTimes[itter-1]
    reservoir = ReservoirHeight[itter-1]
    before = EntryPressure[itter-1]
    after = ExitPressure[itter-1]
    Start = ((First+Last)/2)-50
    End = Start+100

    reyslice = pressure_slice_df(reynolds, Start, End)
    reymean = reyslice.mean()
    reymean = reymean.astype(float)
    rnumber.append(reymean)

    rrms = (pow(((pow(reyslice.mean()-reyslice,2).sum())/len(reyslice)),.5))/reyslice.mean()
    rrms1 = rrms['Reynolds Number']*100
    rms.append(rrms1)

    totpdrop = tot_pressure_drop(reservoir)
    pdrop.append(totpdrop)

    drop = pressure_drop(reservoir, before, after)
    beforep.append(drop[1])
    duringp.append(drop[3])
    afterp.append(drop[5])

    itter = itter+1

#turning the lists into arrays
rnumberp = np.array(rnumber, dtype=int)
rmsp = np.array(rms).round(2)
pdropp = np.array(pdrop).round(2)
beforepp = np.array(beforep)
duringpp = np.array(duringp)
afterpp = np.array(afterp)

#creating dataframe
breakdown = pd.DataFrame()
breakdown['reynolds'] = rnumberp.tolist()
breakdown['rms'] = rmsp.tolist()
breakdown['pdrop'] = pdropp.tolist()
breakdown['before'] = beforepp.tolist()
breakdown['during'] = duringpp.tolist()
breakdown['after'] = afterpp.tolist()


#standard results graph
plot1 = breakdown[['rms']]
plot2 = breakdown[['pdrop']]

fig, ax = plt.subplots(2,1, sharex= True)
ax[0].plot(plot1)
ax[0].legend(["RMS"], loc='upper right')
ax[0].set_ylabel('RMS (%)')
ax[0].grid(True, which = 'both')
ax[0].set_title('Results')
ax[1].plot(plot2)
ax[1].legend(['Total Pressure Drop'], loc='upper right')
ax[1].set_ylabel('Pressure (mBarr)')
ax[1].grid(True, which = 'both')
ax[1].set_xlabel('Steps')

plt.show()

#creating graph for pressure breakdown 


# breakdown['section'] = breakdown['section'].astype('category')
# breakdown.describe(include='category')

# ax = sns.lmplot(x='reynolds', y='pdrop', hue='section', data=breakdown)
# ax.set_titles('Reynolds to Total Pressure Drop Relationship')
# ax.set_xlabels('Reynolds Number (Re)')
# ax.set_ylabels('Total Pressure Drop (percentage)')
# plt.show()