#importing functions
from Functions import *
from MainConfigurationFile import roughness, experiment, Step
from MainConfigurationFile import StartTimes, EndTimes, ReservoirHeight, EntryPressure, ExitPressure, types



# Retrieve Data from Experiment
actualpath = getExperimentPath(roughness, experiment, experiment, types)
print(actualpath)
pressure = tdms_df(actualpath)

#Retrieve Data from laser
laserpath1 = getLaserPath(roughness, experiment,'1', types)
laser1 = laser_df(laserpath1)
laserpath2 = getLaserPath(roughness, experiment, '2', types)
laser2 = laser_df(laserpath2)


#creating the dataframes
#smooth pressure
spressure = pressure_df_smooth(pressure)

#rough pressure
rpressure = pressure_df_rough(pressure)



#format pressure data in the rough section
def pressure_df_rough1(tdms_df):
    rough1 = tdms_df
    rough1 = tdms_df[['Pressure Time', 'Validyne8-22']]
    rough = rough1.set_index('Pressure Time')
    return rough
rpressure2 = pressure_df_rough1(pressure)

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
Start = First
End = Last

#pressure slices
sslice = pressure_slice_df(spressure, Start, End)
rslice = pressure_slice_df(rpressure, Start, End)
rslice2 = pressure_slice_df(rpressure2, Start, End)

#laser slices
slslice = laser_slice_df(slaser,Start,End)
rlslice = laser_slice_df(rlaser,Start,End)
lasermax = rlslice.max()
lasermin = rlslice.min()
print('The velocity is fluctuating between ',lasermin, 'and ', lasermax)

#reynolds slice
reyslice = pressure_slice_df(reynolds, Start, End)
reysm = reyslice['Reynolds Number'].mean()
print('The Reynolds Number is ', reysm)

#percent difference for reynolds slice
reypdiff = reynolds_pdiff(reyslice)
reypdiff = reypdiff.reset_index()
reypdiff = reypdiff[['Pressure Time', 'Percent Difference']]
reypdiff = reypdiff.set_index('Pressure Time')

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
ax[1].plot(rslice2)
ax[1].plot(reys64slice['Laminar Delta P'])
ax[1].plot(blasslice)
ax[1].legend(["Smooth", 'Rough1', 'Rough2', '64/Re', 'Blasius Equ.', 'Haaland Equ.'], loc='upper right')
ax[1].set_ylabel('Pressure (mBar/m)')
ax[1].grid(True, which = 'both')
ax[2].plot(slslice)
ax[2].plot(rlslice)
ax[2].plot(x2sslice)
ax[2].legend(['Rough', 'ūx2 from flowrate'], loc='upper right')
ax[2].set_ylabel('Speed (m/s)')
ax[2].grid(True, which = 'both')
plt.show()
