#importing functions
from Functions import *

#fetching file data
experiment = '10p_ReScan44'

Start = 450
End = 550
data = sql_data(experiment)
pressure = data[0]
laser1 = data[1]
laser2 = data[2]

sliceddata = pressure.reset_index()
a = sliceddata['Flow Rate Time'] > (Start)
b = sliceddata.where(a)
d = b['Flow Rate Time'] < (End)
e = b.where(d)
f = e[['Flow Rate Time', 'Flow Rate']]
flowrate = f.dropna()
flowrate = flowrate.set_index('Flow Rate Time')
print(flowrate.mean())
flows = flowrate
flows['Speed'] = (flows['Flow Rate']/60000)/((math.pi*pow(.011,2))/4)*2
speed = flows.drop('Flow Rate', axis=1)
mov0 = pd.DataFrame()
mov0['rolling'] = speed.rolling(10).mean()
mov0 = mov0.dropna()



laser1 = laser_snr_filter(laser1, 2.0)
laser1 = laser_df_for_graph(laser1)
laser1 = laser_interpolate(laser1)
laser1 = laser_slice_df(laser1, Start, End)
mov1 = pd.DataFrame()
mov1['rolling'] = laser1.rolling(10).mean()
mov1 = mov1.dropna()




laser2 = laser_snr_filter(laser2, 2.0)
laser2 = laser_df_for_graph(laser2)
laser2 = laser_interpolate(laser2)
laser2 = laser_slice_df(laser2, Start, End)
mov2 = pd.DataFrame()
mov2['rolling'] = laser2.rolling(10).mean()
mov2 = mov2.dropna()



mov01 = pow(mov0,2)
mov02 = mov01.mean()
mov03 = pow(mov02,.5)
print(mov03)
print(mov0.mean())

mov11 = pow(mov1,2)
mov12 = mov11.mean()
mov13 = pow(mov12,.5)
print(mov13)
print(mov1.mean())


mov21 = pow(mov2,2)
mov22 = mov21.mean()
mov23 = pow(mov22,.5)
print(mov23)
print(mov2.mean())

fig, ax = plt.subplots(2,1, sharex=True)
ax[0].plot(mov1)
ax[0].plot(mov0)
ax[0].legend(["Laser1", "Flow Rate Speed"], loc='upper right')
ax[0].set_ylabel('m/sec')
ax[0].grid(True, which = 'both')
ax[0].set_title('Results')
ax[1].plot(mov2)
ax[1].plot(mov0)
ax[1].legend(["Laser2", "Flow Rate Speed"], loc='upper right')
ax[1].set_ylabel('Speed (m/sec)')
ax[1].grid(True, which = 'both')

plt.show()