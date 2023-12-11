#importing functions for psd
from Functions import *

#defining the start and end time i am looking to slice
Start = 100
End = 200


#fetching file data
rescan = tdms_df(r'C:\Users\PipeFlow\Desktop\Experiments\New\Protrussion\10p\ReScan15\ReScan15.tdms')
laserdata = laser_df(r'C:\Users\PipeFlow\Desktop\Experiments\New\Protrussion\10p\ReScan8\laser1.SPEED.MSEBP.txt')
laserdata2 = laser_df(r'C:\Users\PipeFlow\Desktop\Experiments\New\Protrussion\10p\ReScan8\laser2.SPEED.MSEBP.txt')

#creating psd for pressure data
pressure = pressure_df_smooth(rescan)
pressure1 = pressure_df_rough(rescan)
pressureslice = pressure_slice_df(pressure, Start, End)
pressureslice1 = pressure_slice_df(pressure1, Start, End)
ppsd = smooth_pressure_psd(pressureslice, Start, End)
ppsd1 = rough_pressure_psd(pressureslice1, Start, End)

# #creating psd for laser data
# filters = laser_snr_filter(laserdata, 2)
# filters2 = laser_snr_filter(laserdata2, 2)
# lasergraph = laser_df_for_graph(filters)
# lasergraph2 = laser_df_for_graph(filters2)
# interpol = laser_interpolate(lasergraph)
# interpol2 = laser_interpolate(lasergraph2)
# slicer = laser_slice_df(interpol, Start, End)
# slicer2 = laser_slice_df(interpol2, Start, End)
# lpsd = laser_psd(slicer, Start, End)
# lpsd1 = laser_psd(slicer2, Start, End)


#plotting the psd for pressure data
fig, ax = plt.subplots(3,1)
ax[0].plot(pressure1)
ax[0].plot(pressure)
ax[0].legend(["After", "Before"], loc='upper right')
ax[0].set_ylabel('Pressure (mBarr)')
ax[0].grid(True, which = 'both')
ax[1].plot(pressureslice1)
ax[1].plot(pressureslice)
ax[1].legend(["After", "Before"], loc='upper right')
ax[1].set_ylabel('Pressure (mBarr)')
ax[1].grid(True, which = 'both')
ax[2].plot(ppsd1)
ax[2].plot(ppsd)
ax[2].legend(["After", "Before"], loc='upper right')
ax[2].set_ylabel('Energy (%)')
ax[2].grid(True, which = 'both')
ax[0].set_title('Pressure Power Spectrum')


# #plotting the psd for laser data
# fig, ax = plt.subplots(3,1)
# ax[0].plot(lasergraph2)
# ax[0].plot(lasergraph)
# ax[0].set_ylim(-.5,2.5)
# ax[0].legend(["After", "Before"], loc='upper right')
# ax[0].set_ylabel('Speed (m/sec)')
# ax[0].grid(True, which = 'both')
# ax[1].plot(slicer2)
# ax[1].plot(slicer)
# ax[1].legend(["After", "Before"], loc='upper right')
# ax[1].set_ylabel('Speed (m/sec)')
# ax[1].grid(True, which = 'both')
# ax[2].plot(lpsd1)
# ax[2].plot(lpsd)
# ax[2].legend(["After", "Before"], loc='upper right')
# ax[2].set_ylabel('Energy (%)')
# ax[2].grid(True, which = 'both')
# ax[0].set_title('Laser Power Spectrum')



# #plotting the psd for pressure data
# plt.figure()
# plt.plot(ppsd1)
# plt.plot(ppsd)
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('Energy (%)')
# plt.grid(True, which = 'both')
# plt.legend(['After', 'Before'], loc='upper right')
# plt.title('Pressure Power Spectrum')

# #plotting the psd for laser data
# plt.figure()
# plt.plot(lpsd1)
# plt.plot(lpsd)
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('Energy (%)')
# plt.grid(True, which = 'both')
# plt.legend(['After', 'Before'], loc='upper right')
# plt.title('Laser Power Spectrum')

plt.show()



