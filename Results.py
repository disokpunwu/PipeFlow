#importing functions
from Functions import *

#fetching file data
experiment = '10p_experiment1'
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
rturbulant = blasius_rough(reynolds)

#ūx2 from flowrate
x2speed = pressure[['Flow Rate Time', 'Flow Rate']]
x2speed = x2speed.set_index('Flow Rate Time')
x2speed = (x2speed['Flow Rate']/60000)/(math.pi*(.0055*.0055))*2

#moving average for laser data
mov = pd.DataFrame()
mov['rolling'] = laser1.rolling(10).mean()
mov1 = pd.DataFrame()
mov1['rolling'] = laser2.rolling(10).mean()

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
ax[1].set_ylabel('Pressure (mBarr)')
ax[1].grid(True, which = 'both')
ax[2].plot(mov)
ax[2].plot(mov1)
ax[2].plot(x2speed)
ax[2].legend(["Smooth", 'Rough', 'ūx2 from flowrate'], loc='upper right')
ax[2].set_ylabel('Speed (m/s)')
ax[2].grid(True, which = 'both')
plt.show()