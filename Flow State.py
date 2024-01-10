#importing Functions
from Functions import *

#fetching file data
experiment = '2v_rescan7'
Step = 1

StartTimes      = [100.0, 400.0, 700.0, 1000.0, 1300.0, 1600.0, 1900.0, 2200.0, 2500.0, 2800.0, 3100.0, 3400.0, 3700.0, 4000.0, 4300.0, 4600.0, 4900.0, 5200.0, 5500.0, 5800.0, 6100.0, 6400.0, 6700.0, 7000.0, 7300.0, 7600.0]
EndTimes        = [300.0, 600.0, 900.0, 1200.0, 1500.0, 1800.0, 2100.0, 2400.0, 2700.0, 3000.0, 3300.0, 3600.0, 3900.0, 4200.0, 4500.0, 4800.0, 5100.0, 5400.0, 5700.0, 6000.0, 6300.0, 6600.0, 6900.0, 7200.0, 7500.0, 7800.0]
ReservoirHeight = [79.00, 88.60, 94.40, 103.00, 110.40, 118.50, 125.10, 131.90, 139.50, 146.90, 154.80, 162.80, 174.80, 176.70, 179.10, 182.10, 185.30, 189.40, 192.70, 195.50, 198.40, 202.60, 206.20, 210.20, 212.10, 213.00]
EntryPressure   = [68.00, 58.40, 52.80, 45.100, 38.600, 31.100, 25.100, 19.200, 12.200, 4.7000, -2.000, -11.00, -22.30, -24.20, -27.20, -29.60, -30.70, -30.70, -30.70, -30.70, -30.70, -30.70, -30.70, -30.70, -30.70, -30.70]
ExitPressure    = [69.10, 59.40, 53.90, 46.300, 39.800, 32.400, 26.400, 20.500, 13.400, 6.1000, -.4000, -9.500, -20.40, -22.40, -25.40, -27.80, -29.00, -29.00, -29.00, -29.00, -29.00, -29.00, -29.00, -29.00, -29.00, -29.00]

#seperating data
data = sql_data(experiment)
pressure = data[0]
laser1 = data[1]
laser2 = data[2]

#pressure readings
smooth = pressure_df_smooth(pressure)
rough = pressure_df_rough(pressure)
pres = smooth.merge(rough, left_index=True, right_index=True)

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
sslice = pressure_slice_df(smooth, Start, End)
rslice = pressure_slice_df(rough, Start, End)
pslice = pressure_slice_df(pres, Start, End)

#reynolds number
reynolds = reynolds_number(pressure)
reynolds = reynolds.reset_index()
reynolds = reynolds.rename(columns={'Flow Rate Time':'Pressure Time'})
reynolds = reynolds.set_index('Pressure Time')
#reynolds = reynolds.rolling(10).mean()

#reynolds slice
reyslice = pressure_slice_df(reynolds, Start, End)

#pressure indicators
reys64 = re64(reynolds)
blas = blasius_smooth(reynolds)
haal = haaland_rough(reynolds)

#indicator slices
reys64slice = re64(reyslice)
blasslice = blasius_smooth(reyslice)
haalslice = haaland_rough(reyslice)

#psd for pressure data
ppsd = smooth_pressure_psd(sslice, Start, End)
ppsd1 = rough_pressure_psd(rslice, Start, End)

#standard deviation of reynolds number
reystd = reynolds_std(reynolds)
reysstd = reynolds_std(reyslice)

#percent difference for reynolds number
reypdiff = reynolds_pdiff(reynolds)
reypdiff = reypdiff.reset_index()
reypdiff = reypdiff[['Pressure Time', 'Percent Difference']]
reypdiff = reypdiff.set_index('Pressure Time')

#pressure drop measurements
pdrop = pressure_drop(reservoir, before, after)
print('The pressure fluctuation is ', pdrop)
print(reyslice['Reynolds Number'].max()-reyslice['Reynolds Number'].min())

#percent difference in fluctuation
#reymean = (((reyslice['Reynolds Number'].max()-reyslice['Reynolds Number'].min())/reyslice['Reynolds Number'].mean())*100).round(2)
reymean = reypdiff['Percent Difference'].mean()
print('The percent difference in fluctuation is ', reymean, 'percent')


#Reynolds Slice, Slice, and psd
fig, ax = plt.subplots(3,1)
ax[0].plot(reyslice['Reynolds Number'])
ax[0].legend(['Reynolds'], loc='upper right')
ax[0].set_ylabel('Reynolds Number')
ax[0].grid(True, which = 'both')
ax[1].plot(pslice)
ax[1].plot(reys64slice)
ax[1].plot(blasslice)
ax[1].plot(haalslice)
ax[1].legend(["Smooth", "Rough", '64/Re', 'Blasius', 'Haaland'], loc='upper right')
ax[1].set_ylabel('Pressure (mBarr)')
ax[1].grid(True, which = 'both')
ax[2].plot(ppsd)
ax[2].plot(ppsd1)
ax[2].legend(['Smooth PSD', 'Rough PSD'], loc='upper right')
ax[2].set_ylabel('Percent of Energy')
ax[2].grid(True, which = 'both')

#Reynolds number, Reynolds pdiff, preasure
fig, ax = plt.subplots(3,1, sharex= True)
ax[0].plot(reynolds['Reynolds Number'])
ax[0].legend(['Reynolds'], loc='upper right')
ax[0].set_ylabel('Reynolds')
ax[0].grid(True, which = 'both')
ax[1].plot(reypdiff)
ax[1].legend(["Reynolds"], loc='upper right')
ax[1].set_ylabel('Percent Difference')
ax[1].grid(True, which = 'both')
ax[2].plot(smooth)
ax[2].plot(rough)
ax[2].plot(reys64)
ax[2].plot(blas)
ax[2].plot(haal)
ax[2].legend(["Smooth", "Rough", '64/Re', 'Blasius', 'Haaland'], loc='upper right')
ax[2].set_ylabel('Pressure (mBarr)')
ax[2].grid(True, which = 'both')

#Reynolds slice, preasure slice
fig, ax = plt.subplots(2,1, sharex= True)
ax[0].plot(reyslice['Reynolds Number'])
ax[0].legend(['Reynolds'], loc='upper right')
ax[0].set_ylabel('Reynolds')
ax[0].grid(True, which = 'both')
ax[1].plot(sslice)
ax[1].plot(rslice)
ax[1].plot(reys64slice)
ax[1].plot(blasslice)
ax[1].plot(haalslice)
ax[1].legend(["Smooth", "Rough", '64/Re', 'Blasius', 'Haaland'], loc='upper right')
ax[1].set_ylabel('Pressure (mBarr)')
ax[1].grid(True, which = 'both')


plt.show()



