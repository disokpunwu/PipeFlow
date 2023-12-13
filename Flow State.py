#importing Functions
from Functions import *

#fetching file data
experiment = '10p_experiment1'
data = sql_data(experiment)
pressure = data[0]

#time slice
Start = 2600
End = 2700

#pressure readings
smooth = pressure_df_smooth(pressure)
rough = pressure_df_rough(pressure)
pres = smooth.merge(rough, left_index=True, right_index=True)

#pressure slices
sslice = pressure_slice_df(smooth, Start, End)
rslice = pressure_slice_df(rough, Start, End)
pslice = pressure_slice_df(pres, Start, End)

#reynolds number
reynolds = reynolds_number(pressure)
reynolds = reynolds.reset_index()
reynolds = reynolds.rename(columns={'Flow Rate Time':'Pressure Time'})
reynolds = reynolds.set_index('Pressure Time')

#reynolds slice
reyslice = pressure_slice_df(reynolds, Start, End)

#pressure indicators
reys64 = re64(reynolds)
blas = blasius_smooth(reynolds)
haal = blasius_rough(reynolds)

#indicator slices
reys64slice = re64(reyslice)
blasslice = blasius_smooth(reyslice)
haalslice = blasius_rough(reyslice)

#psd for pressure data
ppsd = smooth_pressure_psd(sslice, Start, End)
ppsd1 = rough_pressure_psd(rslice, Start, End)

#standard deviation of reynolds number
reystd = reynolds_std(reynolds)
reysstd = reynolds_std(reyslice)

#pressure drop measurements
pdrop = pressure_drop(79, 98, 20)
print(pdrop)
print(reyslice['Reynolds Number'].max()-reyslice['Reynolds Number'].min())


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

#Reynolds number, Reynolds std, preasure
fig, ax = plt.subplots(3,1, sharex= True)
ax[0].plot(reynolds['Reynolds Number'])
ax[0].legend(['Reynolds'], loc='upper right')
ax[0].set_ylabel('Reynolds')
ax[0].grid(True, which = 'both')
ax[1].plot(reystd)
ax[1].legend(["Reynolds"], loc='upper right')
ax[1].set_ylabel('Standard Deviation')
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



