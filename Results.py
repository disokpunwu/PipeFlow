#importing functions
from Functions import *

#fetching file data
experiment = '4v_rescan7'


data = sql_data(experiment)
pressure = data[0]
laser1 = data[1]
laser2 = data[2]

#reynolds number
reynolds = reynolds_number(pressure)

#smooth pressure data graphs
smooth = pressure_df_smooth(pressure)
laminard = re64(reynolds)
sturbulant = blasius_smooth(reynolds)

#rough pressure data graphs
rough = pressure_df_rough(pressure)
rturbulant = haaland_rough(reynolds)

#ūx2 from flowrate
x2speed = x2speed_df(pressure)

#laser1 data graphs
ldv1 = laser_snr_filter(laser1, 2.0)
ldv1 = laser_df_for_graph(ldv1)
ldv1 = laser_interpolate(ldv1)
mov = pd.DataFrame()
mov['rolling'] = ldv1.rolling(10).mean()

#laser2 data graphs
ldv2 = laser_snr_filter(laser2, 2.0)
ldv2 = laser_df_for_graph(ldv2)
ldv2 = laser_interpolate(ldv2)
mov1 = pd.DataFrame()
mov1['rolling'] = ldv2.rolling(10).mean()

#standard results graph
fig, ax = plt.subplots(3,1, sharex= True)
ax[0].plot(reynolds['Reynolds Number'])
ax[0].legend(["Reynolds"], loc='upper right')
ax[0].set_ylabel('Reynolds Number')
ax[0].grid(True, which = 'both')
ax[0].set_title('Results')
ax[1].plot(smooth)
ax[1].plot(rough)
ax[1].plot(laminard)
ax[1].plot(sturbulant)
ax[1].plot(rturbulant)
ax[1].legend(["Smooth", 'Rough', '64/Re', 'Blasius Equ.', 'Haaland Equ.'], loc='upper right')
ax[1].set_ylabel('Pressure (mBar/m)')
ax[1].grid(True, which = 'both')
ax[2].plot(mov)
ax[2].plot(mov1)
ax[2].plot(x2speed)
ax[2].legend(["Smooth", 'Rough', 'ūx2 from flowrate'], loc='upper right')
ax[2].set_ylabel('Speed (m/s)')
ax[2].grid(True, which = 'both')
plt.show()