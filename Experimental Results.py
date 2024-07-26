#importing functions
from Functions import *

#fetching file data
experiment = '2v_rescan79'
engine = create_sql_engine(experiment)
(pressure) = read_table(engine, 'pressure')


#reynolds number
reynolds = reynolds_number(pressure)

#smooth pressure data graphs
smooth = pressure_df_smooth(pressure)
laminar = re64(reynolds)

#rough pressure data graphs
rough = pressure_df_rough(pressure)
turbulant = haaland_rough(reynolds)

print(rough)
print(rough['Validyne 6-32'].max())

print(reynolds[reynolds['Reynolds Number'] > 1000])
# reynolds.reset_index(inplace=True)
print(reynolds['Reynolds Number'].max())

#standard results graph
fig, ax = plt.subplots(2,1, sharex= True)
ax[0].plot(reynolds['Reynolds Number'])
ax[0].legend(["Reynolds"], loc='upper right')
ax[0].set_ylabel('Reynolds Number')
ax[0].grid(True, which = 'both')
ax[0].set_title('Results')
ax[1].plot(rough)
ax[1].plot(laminar)
#ax[1].plot(turbulant)
ax[1].legend(["Rough", '64/Re'], loc='upper right')
ax[1].set_ylabel('Pressure (mBar/m)')
ax[1].grid(True, which = 'both')
plt.show()
