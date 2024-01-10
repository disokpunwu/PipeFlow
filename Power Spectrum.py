#importing functions for psd
from Functions import *

#defining the start and end time i am looking to slice
Start = 7050
End = 7150

#fetching file data
experiment = '4v_rescan7'


data = sql_data(experiment)
pressure = data[0]
laser1 = data[1]
laser2 = data[2]

#creating psd for pressure data
smoothp = pressure_df_smooth(pressure)
roughp = pressure_df_rough(pressure)
pressureslice = pressure_slice_df(smoothp, Start, End)
pressureslice1 = pressure_slice_df(roughp, Start, End)
ppsd = smooth_pressure_psd(pressureslice, Start, End)
ppsd1 = rough_pressure_psd(pressureslice1, Start, End)

#creating psd for laser data
ldv1 = laser_snr_filter(laser1, 2.0)
ldv1 = laser_df_for_graph(ldv1)
ldv1 = laser_interpolate(ldv1)
ldv2 = laser_snr_filter(laser2, 2.0)
ldv2 = laser_df_for_graph(ldv2)
ldv2 = laser_interpolate(ldv2)
slicer = laser_slice_df(ldv1, Start, End)
slicer2 = laser_slice_df(ldv2, Start, End)
lpsd = laser_psd(slicer, Start, End)
lpsd1 = laser_psd(slicer2, Start, End)

#plotting the psd for pressure data
fig, ax = plt.subplots(3,1)
ax[0].plot(roughp)
ax[0].plot(smoothp)
ax[0].legend(["After", "Before"], loc='upper right')
ax[0].set_ylabel('Pressure (mBar/m)')
ax[0].grid(True, which = 'both')
ax[1].plot(pressureslice1)
ax[1].plot(pressureslice)
ax[1].legend(["After", "Before"], loc='upper right')
ax[1].set_ylabel('Pressure (mBar/m)')
ax[1].grid(True, which = 'both')
ax[2].plot(ppsd1)
ax[2].plot(ppsd)
ax[2].legend(["After", "Before"], loc='upper right')
ax[2].set_ylabel('Energy (%)')
ax[2].grid(True, which = 'both')
ax[0].set_title('Pressure Power Spectrum')

#plotting the psd for laser data
fig, ax = plt.subplots(3,1)
ax[0].plot(ldv2)
ax[0].plot(ldv1)
ax[0].set_ylim(-.5,2.5)
ax[0].legend(["After", "Before"], loc='upper right')
ax[0].set_ylabel('Speed (m/sec)')
ax[0].grid(True, which = 'both')
ax[1].plot(slicer2)
ax[1].plot(slicer)
ax[1].legend(["After", "Before"], loc='upper right')
ax[1].set_ylabel('Speed (m/sec)')
ax[1].grid(True, which = 'both')
ax[2].plot(lpsd1)
ax[2].plot(lpsd)
ax[2].legend(["After", "Before"], loc='upper right')
ax[2].set_ylabel('Energy (%)')
ax[2].grid(True, which = 'both')
ax[0].set_title('Laser Power Spectrum')

plt.show()



