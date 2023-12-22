#importing functions
from Functions import *

#function to slice 2x speed data
def x2speed_slice_df(formatted_data, Start, End):
    sliceddata = formatted_data
    sliceddata = sliceddata.reset_index()
    a = sliceddata['Flow Rate Time'] > (Start-.1)
    b = sliceddata.where(a)
    c = b.dropna()
    d = c['Flow Rate Time'] < (End+.1)
    e = c.where(d)
    sliceddata = e.dropna()
    sliceddata = sliceddata.set_index('Flow Rate Time')
    return sliceddata 

#fetching file data
experiment = '4v_rescan3'
Step = 2

StartTimes = [100, 400, 700, 1000, 1300, 1600]
EndTimes =   [300, 600, 900, 1200, 1500, 1800]
ReservoirHeight = [79, 92.8, 105.8, 120.4, 139.9, 158]
EntryPressure = [107.4, 102.3, 96.3, 88.6, 79, 73.1]
ExitPressure = [114.6, 110.9, 107.4, 102.8, 98.4, 99]


#seperating data
data = sql_data(experiment)
pressure = data[0]
laser1 = data[1]
laser2 = data[2]


#creating the dataframes
#smooth pressure
spressure = pressure_df_smooth(pressure)

#rough pressure
rpressure = pressure_df_rough(pressure)

#laser1
ldv1 = laser_snr_filter(laser1, 2.0)
ldv1 = laser_df_for_graph(ldv1)
ldv1 = laser_interpolate(ldv1)
slaser = pd.DataFrame()
slaser['rolling'] = ldv1.rolling(10).mean()

#laser2
ldv2 = laser_snr_filter(laser2, 2.0)
ldv2 = laser_df_for_graph(ldv2)
ldv2 = laser_interpolate(ldv2)
rlaser = pd.DataFrame()
rlaser['rolling'] = ldv2.rolling(10).mean()

#reynolds number
reynolds = reynolds_number(pressure)
reynolds = reynolds.reset_index()
reynolds = reynolds.rename(columns={'Flow Rate Time':'Pressure Time'})
reynolds = reynolds.set_index('Pressure Time')
reynolds = reynolds.rolling(10).mean()

#indicators
reys64 = re64(reynolds)
blas = blasius_smooth(reynolds)
haal = blasius_rough(reynolds)

#ūx2 from flowrate
x2speed = pressure[['Flow Rate Time', 'Flow Rate']]
x2speed = x2speed.set_index('Flow Rate Time')
x2speed = (x2speed['Flow Rate']/60000)/(math.pi*(.0055*.0055))*2
x2spped = x2speed.rolling(10).mean()


#slices
First= StartTimes[Step-1]
Last = EndTimes[Step-1]
First = First
Last = Last

#pressure drop 
reservoir = ReservoirHeight[Step-1]
before = EntryPressure[Step-1]
after = ExitPressure[Step-1]

print(type(First))
Start = ((First+Last)/2)-50
End = Start+100
#pressure slices
sslice = pressure_slice_df(spressure, Start, End)
rslice = pressure_slice_df(rpressure, Start, End)

#laser slices
slslice = laser_slice_df(slaser,Start,End)
rlslice = laser_slice_df(rlaser,Start,End)

#reynolds slice
reyslice = pressure_slice_df(reynolds, Start, End)

#percent difference for reynolds slice
reypdiff = reynolds_pdiff(reyslice)
reypdiff = reypdiff.reset_index()
reypdiff = reypdiff[['Pressure Time', 'Percent Difference']]
reypdiff = reypdiff.set_index('Pressure Time')

#indicator slices
reys64slice = re64(reyslice)
blasslice = blasius_smooth(reyslice)
haalslice = blasius_rough(reyslice)

#ūx2 from flowrate slice
x2sslice = x2speed_slice_df(x2speed, Start, End)

#RMS of Reynolds slice
rrms1 = pow(reyslice['Reynolds Number'],2)
rrms2 = rrms1.mean()
rrms3 = pow(rrms2,.5)
print('RMS of the reynolds number is ', rrms3)

#percent difference in fluctuation
#reymean = (((reyslice['Reynolds Number'].max()-reyslice['Reynolds Number'].min())/reyslice['Reynolds Number'].mean())*100).round(2)
reymean = reypdiff['Percent Difference'].mean()
print('The percent difference in fluctuation is ', reymean, 'percent')

#pressure drop of the system
totpdrop = tot_pressure_drop(reservoir)
print('The total pressure drop is ', totpdrop)
pdrop = pressure_drop(reservoir, before, after)
print('The pressure fluctuation is ', pdrop)




#graphs
fig, ax = plt.subplots(4,1, sharex=True)
ax[0].plot(reyslice['Reynolds Number'])
ax[0].legend(["Reynolds"], loc='upper right')
ax[0].set_ylabel('Reynolds Number')
ax[0].grid(True, which = 'both')
ax[0].set_title('Results')
ax[1].plot(reypdiff)
ax[1].set_ylabel('Percent Difference')
ax[1].grid(True, which = 'both')
ax[2].plot(sslice)
ax[2].plot(rslice)
ax[2].plot(reys64slice['Laminar Delta P'])
ax[2].plot(blasslice)
ax[2].plot(haalslice)
ax[2].legend(["Smooth", 'Rough', '64/Re', 'Blasius Equ.', 'Haaland Equ.'], loc='upper right')
ax[2].set_ylabel('Pressure (mBar)')
ax[2].grid(True, which = 'both')
ax[3].plot(slslice)
ax[3].plot(rlslice)
ax[3].plot(x2sslice)
ax[3].legend(["Smooth", 'Rough', 'ūx2 from flowrate'], loc='upper right')
ax[3].set_ylabel('Speed (m/s)')
ax[3].grid(True, which = 'both')


plt.show()
