from Functions import *

experiment = ''
Step =1


StartTimes      = []
EndTimes        = []
ReservoirHeight = []
EntryPressure   = []
ExitPressure    = []


#seperating data
(pressure, laser1, laser2) = read_tables(experiment, ['pressure', 'laser1', 'laser2'])

#reynolds number
reynolds = reynolds_number(pressure)
reynolds = reynolds.reset_index()
reynolds = reynolds.rename(columns={'Flow Rate Time':'Pressure Time'})
reynolds = reynolds.set_index('Pressure Time')
reynolds = reynolds.rolling(10).mean()

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

#reynolds slice
reyslice = pressure_slice_df(reynolds, Start, End)

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

#laser slices
slslice = laser_slice_df(slaser,Start,End)
rlslice = laser_slice_df(rlaser,Start,End)
print(slslice)

#flow meter
rrms1 = (pow(((pow(slslice.mean()-slslice,2).sum())/len(slslice)),.5))/slslice.mean()
rrms = rrms1['rolling']*100
print(rrms)

rrms12 = (pow(((pow(reyslice.mean()-reyslice,2).sum())/len(reyslice)),.5))/reyslice.mean()
rrms2 = rrms12['Reynolds Number']*100
print(rrms2)
print(reyslice['Reynolds Number'].mean())
print(reyslice['Reynolds Number'].max()-reyslice['Reynolds Number'].min())
print(reynolds)


