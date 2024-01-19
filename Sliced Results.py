#importing functions
from Functions import *


#fetching file data
experiment = ''
Step = 1

StartTimes =      [100.0, 300.0, 500.0, 700.0, 900.00, 1100.0, 1300.0, 1500.0, 1700.0, 1900.0, 2100.0, 2300.0, 2500.0, 2700.0, 2900.0]
EndTimes =        [200.0, 400.0, 600.0, 800.0, 1000.0, 1200.0, 1400.0, 1600.0, 1800.0, 2000.0, 2200.0, 2400.0, 2600.0, 2800.0, 3000.0]
ReservoirHeight = [108.0, 109.6, 111.7, 112.0, 113.30, 113.30, 182.00, 185.70, 186.50, 188.40, 191.80, 194.70, 197.60, 199.60, 204.50]
EntryPressure   = [59.40, 57.90, 57.00, 57.50, 54.900, 54.900, -16.30, -21.00, -23.00, -25.00, -28.00, -28.00, -28.00, -28.00, -28.00]
ExitPressure    = [61.00, 59.60, 59.00, 59.10, 57.100, 57.100, -14.50, -20.00, -21.50, -22.80, -26.00, -26.00, -26.00, -26.00, -26.00]

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
haal = haaland_rough(reynolds)

#ūx2 from flowrate
x2speed = x2speed_df(pressure)


#slices
First= StartTimes[Step-1]
Last = EndTimes[Step-1]
First = First
Last = Last

#pressure drop 
reservoir = ReservoirHeight[Step-1]
before = EntryPressure[Step-1]
after = ExitPressure[Step-1]
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
reysm = reyslice['Reynolds Number'].mean()
print('The Reynolds Number is ', reysm)

# #percent difference for reynolds slice
# reypdiff = reynolds_pdiff(reyslice)
# reypdiff = reypdiff.reset_index()
# reypdiff = reypdiff[['Pressure Time', 'Percent Difference']]
# reypdiff = reypdiff.set_index('Pressure Time')

#indicator slices
reys64slice = re64(reyslice)
blasslice = blasius_smooth(reyslice)
haalslice = haaland_rough(reyslice)

#ūx2 from flowrate slice
x2sslice = x2speed_slice_df(x2speed, Start, End)

#RMS of Reynolds slice
rrms12 = (pow(((pow(reyslice.mean()-reyslice,2).sum())/len(reyslice)),.5))/reyslice.mean()
rrms2 = rrms12['Reynolds Number']*100
print('The RMS is ', rrms2)
refluc = reyslice['Reynolds Number'].max()-reyslice['Reynolds Number'].min()
print('The viariation in Re is ', refluc)

#pressure drop of the system
totpdrop = tot_pressure_drop(reservoir)
print('The total pressure drop is ', totpdrop)
pdrop = pressure_drop(reservoir, before, after)
print('The pressure drop before the entrance is ', pdrop[1])
print('The pressure drop in the pipe is ', pdrop[3])
print('The pressure drop after the pipe is ', pdrop[5])



#graphs
fig, ax = plt.subplots(3,1, sharex=True)
ax[0].plot(reyslice['Reynolds Number'])
ax[0].legend(["Reynolds"], loc='upper right')
ax[0].set_ylabel('Reynolds Number')
ax[0].grid(True, which = 'both')
ax[0].set_title('Results')
ax[1].plot(sslice)
ax[1].plot(rslice)
ax[1].plot(reys64slice['Laminar Delta P'])
ax[1].plot(blasslice)
ax[1].plot(haalslice)
ax[1].legend(["Smooth", 'Rough', '64/Re', 'Blasius Equ.', 'Haaland Equ.'], loc='upper right')
ax[1].set_ylabel('Pressure (mBar/m)')
ax[1].grid(True, which = 'both')
ax[2].plot(slslice)
ax[2].plot(rlslice)
ax[2].plot(x2sslice)
ax[2].legend(["Smooth", 'Rough', 'ūx2 from flowrate'], loc='upper right')
ax[2].set_ylabel('Speed (m/s)')
ax[2].grid(True, which = 'both')
plt.show()
