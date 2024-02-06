from Functions import *

#fetching file data
experiment = '4v_rescan7'

#notes from experiment
StartTimes      = [100.0, 400.0, 700.0, 1000.0, 1300.0, 1600.0, 1900.0, 2200.0, 2500.0, 2800.0, 3100.0, 3400.0, 3700.0, 4000.0, 4300.0, 4600.0, 4900.0, 5200.0, 5500.0, 5800.0, 6100.0, 6400.0, 6700.0, 7000.0, 7300.0, 7600.0]
EndTimes        = [300.0, 600.0, 900.0, 1200.0, 1500.0, 1800.0, 2100.0, 2400.0, 2700.0, 3000.0, 3300.0, 3600.0, 3900.0, 4200.0, 4500.0, 4800.0, 5100.0, 5400.0, 5700.0, 6000.0, 6300.0, 6600.0, 6900.0, 7200.0, 7500.0, 7800.0]
ReservoirHeight = [79.00, 88.60, 94.40, 103.00, 110.40, 118.50, 125.10, 131.90, 139.50, 146.90, 154.80, 162.80, 174.80, 176.70, 179.10, 182.10, 185.30, 189.40, 192.70, 195.50, 198.40, 202.60, 206.20, 210.20, 212.10, 213.00]
EntryPressure   = [68.00, 58.40, 52.80, 45.100, 38.600, 31.100, 25.100, 19.200, 12.200, 4.7000, -2.000, -11.00, -22.30, -24.20, -27.20, -29.60, -30.70, -30.70, -30.70, -30.70, -30.70, -30.70, -30.70, -30.70, -30.70, -30.70]
ExitPressure    = [69.10, 59.40, 53.90, 46.300, 39.800, 32.400, 26.400, 20.500, 13.400, 6.1000, -.4000, -9.500, -20.40, -22.40, -25.40, -27.80, -29.00, -29.00, -29.00, -29.00, -29.00, -29.00, -29.00, -29.00, -29.00, -29.00]

#seperating data from database
data = sql_data1(experiment)
pressure = data

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