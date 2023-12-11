#importing functions
from Functions import *

#path to data files
# tdms = tdms_df(r'C:\Users\PipeFlow\Desktop\Experiments\Old\Protrussion\10p\exp2\roughnessR_r=10P-exp2.tdms')
# ldv1 = laser_df(r'C:\Users\PipeFlow\Desktop\Experiments\Old\Protrussion\10p\exp2\roughnessR_r=10P-exp2-1D.SPEED.MSEBP.txt')
# ldv2 = laser_df(r'C:\Users\PipeFlow\Desktop\Experiments\Old\Protrussion\10p\exp2\roughnessR_r=10P-exp2-2D.SPEED.MSEBP.txt')

tdms = tdms_df(r'C:\Users\PipeFlow\Desktop\Experiments\New\Protrussion\10p\ReScan9\ReScan9.tdms')
ldv1 = laser_df(r'C:\Users\PipeFlow\Desktop\Experiments\New\Protrussion\10p\ReScan8\laser1.SPEED.MSEBP.txt')
ldv2 = laser_df(r'C:\Users\PipeFlow\Desktop\Experiments\New\Protrussion\10p\ReScan8\laser2.SPEED.MSEBP.txt')

#start and end time for slices
Start = 1600
End = 1700

#smooth pressure data graphs
smooth = pressure_df_smooth(tdms)
sslice = pressure_slice_df(smooth, Start, End)
spsd = smooth_pressure_psd(sslice, Start, End)
sstd = smooth_pressure_std(smooth)

#rough pressure data graphs
rough = pressure_df_rough(tdms)
rslice = pressure_slice_df(rough, Start, End)
rpsd = rough_pressure_psd(rslice, Start, End)
rstd = rough_pressure_std(rough)

#ideal pressure readings
reynolds = reynolds_number(tdms)
laminard = re64(reynolds)
sturbulant = blasius_smooth(reynolds)
rturbulant = blasius_rough(reynolds)

#moving average
mov = pd.DataFrame()
mov['rolling'] = smooth.rolling(1000).mean()
mov1 = pd.DataFrame()
mov1['rolling'] = rough.rolling(1000).mean()

#transitional stage
stran1 = sstd['Standard Deviation'] > sstd['Standard Deviation'].mean()
stran = sstd.where(stran1)
rtran1 = rstd['Standard Deviation'] > rstd['Standard Deviation'].mean()
rtran = rstd.where(rtran1)

#laminar stage

#standard results graph
fig, ax = plt.subplots(3,1, sharex= True)
ax[0].plot(reynolds['Reynolds Number'])
ax[0].legend(["Reynolds"], loc='upper right')
ax[0].set_ylabel('Reynolds Number')
ax[0].grid(True, which = 'both')
ax[0].set_title('Results')
ax[1].plot(mov)
ax[1].plot(laminard)
ax[1].plot(sturbulant)
ax[1].plot(stran)
ax[1].legend(["Smooth", 'Ideal Laminar', 'Ideal Turbulant'], loc='upper right')
ax[1].set_ylabel('Pressure (mBarr)')
ax[1].grid(True, which = 'both')
ax[2].plot(rough)
ax[2].plot(laminard)
ax[2].plot(rturbulant)
ax[2].legend(["Rough", 'Ideal Laminar', 'Ideal Turbulant'], loc='upper right')
ax[2].set_ylabel('Pressure (mBarr)')
ax[2].grid(True, which = 'both')
plt.show()

# #standard results graph
# fig, ax = plt.subplots(3,1, sharex= True)
# ax[0].plot(reynolds['Reynolds Number'])
# ax[0].legend(["Reynolds"], loc='upper right')
# ax[0].set_ylabel('Reynolds Number')
# ax[0].grid(True, which = 'both')
# ax[0].set_title('Results')
# ax[1].plot(smooth)
# ax[1].plot(laminard)
# ax[1].plot(sturbulant)
# ax[1].legend(["Smooth", 'Ideal Laminar', 'Ideal Turbulant'], loc='upper right')
# ax[1].set_ylabel('Pressure (mBarr)')
# ax[1].grid(True, which = 'both')
# ax[2].plot(rough)
# ax[2].plot(laminard)
# ax[2].plot(rturbulant)
# ax[2].legend(["Rough", 'Ideal Laminar', 'Ideal Turbulant'], loc='upper right')
# ax[2].set_ylabel('Pressure (mBarr)')
# ax[2].grid(True, which = 'both')
# plt.show()

