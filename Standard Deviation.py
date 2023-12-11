from Functions import *

#fetching file data
rescan = tdms_df(r'C:\Users\PipeFlow\Desktop\Experiments\New\Protrussion\10p\ReScan8\ReScan8.tdms')
laserdata = laser_df(r'C:\Users\PipeFlow\Desktop\Experiments\New\Protrussion\10p\ReScan8\laser1.SPEED.MSEBP.txt')
laserdata2 = laser_df(r'C:\Users\PipeFlow\Desktop\Experiments\New\Protrussion\10p\ReScan8\laser2.SPEED.MSEBP.txt')

# rescan = tdms_df(r'C:\Users\PipeFlow\Desktop\Experiments\Old\Protrussion\10p\exp2\roughnessR_r=10P-exp2.tdms')
# laserdata = laser_df(r'C:\Users\PipeFlow\Desktop\Experiments\Old\Protrussion\10p\exp2\roughnessR_r=10P-exp2-1D.SPEED.MSEBP.txt')
# laserdata2 = laser_df(r'C:\Users\PipeFlow\Desktop\Experiments\Old\Protrussion\10p\exp2\roughnessR_r=10P-exp2-2D.SPEED.MSEBP.txt')


#creating std for pressure data
smooth = pressure_df_smooth(rescan)
rough = pressure_df_rough(rescan)
pstd = smooth_pressure_std(smooth)
pstd1 = rough_pressure_std(rough)

# #creating std for laser data
# laser1 = laser_snr_filter(laserdata, 2)
# laser2 = laser_snr_filter(laserdata2, 2)
# signal1 = laser_df_for_graph(laser1)
# signal2 = laser_df_for_graph(laser2)
# inter1 = laser_interpolate(signal1)
# inter2 = laser_interpolate(signal2)
# lstd = laser_std(inter1)
# lstd1 = laser_std(inter2)


#plotting the std for pressure data
fig, ax = plt.subplots(2,1, sharex= True)
ax[0].plot(rough)
ax[0].plot(smooth)
ax[0].legend(["Rough", "Smooth"], loc='upper right')
ax[0].set_ylabel('Pressure (mBarr)')
ax[0].grid(True, which = 'both')
ax[1].plot(pstd1)
ax[1].plot(pstd)
ax[1].legend(["Rough", "Smooth"], loc='upper right')
ax[1].set_ylabel('Standard Deviation (mBarr)')
ax[1].grid(True, which = 'both')
ax[0].set_title('Pressure Standard Deviation')

# fig, ax = plt.subplots(2,1, sharex= True)
# ax[0].plot(inter2)
# ax[0].plot(inter1)
# ax[0].set_ylim(-.5,2.5)
# ax[0].legend(["After", "Before"], loc='upper right')
# ax[0].set_ylabel('Speed (m/sec)')
# ax[0].grid(True, which = 'both')
# ax[1].plot(lstd1)
# ax[1].plot(lstd)
# ax[1].legend(["After", "Before"], loc='upper right')
# ax[1].set_ylabel('Standard Deviation (m/sec)')
# ax[1].grid(True, which = 'both')
# ax[0].set_title('Speed Standard Deviation')

plt.show()



