#importing functions for psd
from Functions import *


#fetching file data
experiment = '2v_rescan7'
Step = 1

StartTimes      = [100.0, 400.0, 700.0, 1000.0, 1300.0, 1600.0, 1900.0, 2200.0, 2500.0, 2800.0, 3100.0, 3400.0, 3700.0, 4000.0, 4300.0, 4600.0, 4900.0, 5200.0, 5500.0, 5800.0, 6100.0, 6400.0, 6700.0, 7000.0, 7300.0, 7600.0]
EndTimes        = [300.0, 600.0, 900.0, 1200.0, 1500.0, 1800.0, 2100.0, 2400.0, 2700.0, 3000.0, 3300.0, 3600.0, 3900.0, 4200.0, 4500.0, 4800.0, 5100.0, 5400.0, 5700.0, 6000.0, 6300.0, 6600.0, 6900.0, 7200.0, 7500.0, 7800.0]
ReservoirHeight = [79.00, 88.60, 94.40, 103.00, 110.40, 118.50, 125.10, 131.90, 139.50, 146.90, 154.80, 162.80, 174.80, 176.70, 179.10, 182.10, 185.30, 189.40, 192.70, 195.50, 198.40, 202.60, 206.20, 210.20, 212.10, 213.00]
EntryPressure   = [68.00, 58.40, 52.80, 45.100, 38.600, 31.100, 25.100, 19.200, 12.200, 4.7000, -2.000, -11.00, -22.30, -24.20, -27.20, -29.60, -30.70, -30.70, -30.70, -30.70, -30.70, -30.70, -30.70, -30.70, -30.70, -30.70]
ExitPressure    = [69.10, 59.40, 53.90, 46.300, 39.800, 32.400, 26.400, 20.500, 13.400, 6.1000, -.4000, -9.500, -20.40, -22.40, -25.40, -27.80, -29.00, -29.00, -29.00, -29.00, -29.00, -29.00, -29.00, -29.00, -29.00, -29.00]

data = sql_data(experiment)
pressure = data[0]
laser1 = data[1]
laser2 = data[2]

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



