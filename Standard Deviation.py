from Functions import *

#fetching file data
experiment = ''


data = sql_data(experiment)
pressure = data[0]
laser1 = data[1]
laser2 = data[2]

#creating std for pressure data
smooth = pressure_df_smooth(pressure)
rough = pressure_df_rough(pressure)
pstd = smooth_pressure_std(smooth)
pstd1 = rough_pressure_std(rough)

#transitional stage for pressure data
stran1 = pstd['Standard Deviation'] > pstd['Standard Deviation'].mean()
stran = pstd.where(stran1)
rtran1 = pstd1['Standard Deviation'] > pstd1['Standard Deviation'].mean()
rtran = pstd1.where(rtran1)

#creating std for laser data
ldv1 = laser_snr_filter(laser1, 2.0)
ldv1 = laser_df_for_graph(ldv1)
ldv1 = laser_interpolate(ldv1)
lstd = laser_std(ldv1)
ldv2 = laser_snr_filter(laser2, 2.0)
ldv2 = laser_df_for_graph(ldv2)
ldv2 = laser_interpolate(ldv2)
lstd1 = laser_std(ldv2)

#transitional stage for laser data
l1tran1 = lstd['Standard Deviation'] > lstd['Standard Deviation'].mean()
l1tran = lstd.where(l1tran1)
l2tran1 = lstd1['Standard Deviation'] > lstd1['Standard Deviation'].mean()
l2tran = pstd1.where(l2tran1)

#plotting the std for pressure data
fig, ax = plt.subplots(3,1, sharex= True)
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
ax[2].plot(rtran)
ax[2].plot(stran)
ax[2].legend(["Rough", "Smooth"], loc='upper right')
ax[2].set_ylabel('Standard Deviation (mBarr)')
ax[2].grid(True, which = 'both')
ax[0].set_title('Pressure Standard Deviation')

#plotting std for laser data
fig, ax = plt.subplots(3,1, sharex= True)
ax[0].plot(ldv2)
ax[0].plot(ldv1)
ax[0].set_ylim(-.5,2.5)
ax[0].legend(["Rough", "Smooth"], loc='upper right')
ax[0].set_ylabel('Speed (m/sec)')
ax[0].grid(True, which = 'both')
ax[1].plot(lstd1)
ax[1].plot(lstd)
ax[1].legend(["Rough", "Smooth"], loc='upper right')
ax[1].set_ylabel('Standard Deviation (m/sec)')
ax[1].grid(True, which = 'both')
ax[2].plot(l2tran)
ax[2].plot(l1tran)
ax[2].legend(["Rough", "Smooth"], loc='upper right')
ax[2].set_ylabel('Standard Deviation (mBarr)')
ax[2].grid(True, which = 'both')
ax[0].set_title('Speed Standard Deviation')

plt.show()



