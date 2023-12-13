# from Functions import *

# Start = 1600
# End = 1700
# path = r'C:\Users\PipeFlow\Desktop\Experiments\Old\Protrussion\10p\exp3\roughnessR_r=10P-exp3-2D.SPEED.MSEBP.txt'
# laser = laser_df(path)
# laser1 = laser_snr_filter(laser, 2)
# laser2 = laser_df_for_graph(laser1)
# laser3 = laser_interpolate(laser2)
# laser4 = laser_slice_df(laser3, Start, End)
# laser5 = laser_psd(laser4, Start, End)
# plt.plot(laser5)
# plt.show()

# data = laser_df(r'C:\Users\PipeFlow\Desktop\Experiments\Old\Protrussion\10p\exp3\roughnessR_r=10P-exp3-1D.SPEED.MSEBP.txt')
# dataframe = laser_df_for_graph(data)

# laser = dataframe
# laser = laser.reset_index()
# laser['Device Time'] = laser['Device Time'].round(2)
# laser['Device Time'] = laser['Device Time'].drop_duplicates(keep='first')
# laser = laser.dropna()
# maxVal = laser['Device Time'].max()
# laser2 = pd.DataFrame()
# uni = np.linspace(0.0,maxVal,int(maxVal*100))
# uni = uni.round(2)
# laser2['Device Time'] = uni
# laser3 = laser2.merge(laser, on='Device Time', how='left')
# laser4 = laser3.drop('Device Time', axis='columns')
# laser5 = laser4.interpolate(method='linear')
# laser5['Device Time'] = laser3['Device Time']
# laser5 = laser5.set_index('Device Time')
# print(laser5['Speed (m/sec)'].isna().sum())

# interpol = laser_interpolate(dataframe)
# slices = laser_slice_df(interpol, 1600, 1700)
# print(slices)
# psd = laser_psd(slices,1600, 1700)
# plt.plot(psd)
# plt.show()

# laser1 = laser_df_for_graph
# laser1 = laser1.reset_index()
# laser1['Device Time'] = laser1['Device Time'].round(1)
# max = laser1['Device Time'].max()
# laser2 = pd.DataFrame()
# laser2['milliseconds'] = (laser1.index+1)/10
# a = laser2['milliseconds'] < (max+.1)
# b = laser2.where(a)
# laser2 = b.dropna()
# laser2['index'] = laser2.index
# laser2 = laser2.set_index('milliseconds')
# laser1['Device Time'] = laser1['Device Time'].drop_duplicates(keep='first')
# laser1 = laser1.dropna()
# laser1 = laser1.reset_index()
# laser1 = laser1.drop('index', axis='columns')
# laser1 = laser1.set_index('Device Time')
# laser3 = laser2.join(laser1, lsuffix='_caller', rsuffix='_other')
# laser3 = laser3.reset_index()
# laser3 = laser3.drop('index', axis='columns')
# laser3 = laser3.interpolate(method='linear')
# laser3 = laser3.rename(columns={'milliseconds':'Device Time'})
# laser3 = laser3.set_index('Device Time')

# import pandas as pd
# from io import StringIO
# #function to read laser files
# def laser_df(path):
#     laser_data = pd.read_csv(path, delimiter='\t')
#     laser_data.columns = ['Device Time (msec)', 'Device Time (usec)', 'Speed (m/sec)', 'SNR']
#     return laser_data

# def pressureDataframeFromCSV(csvString, hasHeaders = False, headers = []):
#     if hasHeaders:
#         # The first row is headers. Valid options are header="infer" or 0 if names is passed
#         headerVal = "infer" if len(headers) == 0 else 0
#     else:
#         # The first row is not headers. Valid options are header = None
#         headerVal = None
#     nameVal = None if len(headers) == 0 else headers
#     return pd.read_csv(StringIO(csvString), header=headerVal, names=nameVal)

# from Functions import *
# path = r"C:\Users\PipeFlow\Desktop\Experiments\Old\Protrussion\10p\exp2\roughnessR_r=10P-exp2.tdms"



# # def re64(reynolds):
# #     reynolds['64/Re'] = 64/reynolds['Reynolds Number']
# #     return re64

# def reynolds_number(path):
#     tdms = tdms_df(path)
#     flowrate = tdms[['Flow Rate Time', 'Flow Rate']]
#     flowrate['Flow Rate Time'] = flowrate['Flow Rate Time'].round(2)
#     flowrate['Flow Rate Time'] = flowrate['Flow Rate Time'].drop_duplicates(keep='first')
#     flowrate = flowrate.dropna()
#     flowrate['Reynolds Number'] = (1004*(11*10**(-3))*flowrate['Flow Rate']/(60*1000)*1/((11*10**(-3)/2)**2*math.pi))/(0.9096*10**(-3))
#     reynolds = flowrate[['Flow Rate Time', 'Reynolds Number']]
#     reynolds = reynolds.set_index('Flow Rate Time')
#     return reynolds

# def re64(reynolds):
#     reynolds['64/Re'] = 64/reynolds['Reynolds Number']
#     reynolds['Laminar Delta P'] = reynolds['64/Re']*1/(11*10**(-3))*1004/2*(reynolds['Reynolds Number']/(1004*11*1e-3)*(0.9096*10**(-3)))**2/100
#     Re64 = reynolds.drop('Reynolds Number', axis='columns')
#     Re64 = Re64.drop('64/Re', axis='columns')
#     return Re64

# def blasius_smooth(reynolds):
#     reynolds['Friction'] = .316/(reynolds['Reynolds Number']**.25)
#     reynolds['Blasius'] = reynolds['Friction']*1/(11*10**(-3))*1004/2*(reynolds['Reynolds Number']/(1004*11*1e-3)*(0.9096*10**(-3)))**2/100
#     blasius = reynolds['Blasius']
#     return blasius

# def blasius_rough(reynolds):
#      reynolds['Friction'] = (1/(-1.8*np.log10(((1/11)/3.7)**1.11+6.9/reynolds['Reynolds Number'])))**2
#      reynolds['Blasius'] = reynolds['Friction']*1/(11*10**(-3))*1004/2*(reynolds['Reynolds Number']/(1004*11*1e-3)*(0.9096*10**(-3)))**2/100
#      blasius = reynolds['Blasius']
#      return blasius




#     reynolds['Blasius'] = .316/(reynolds['Reynolds Number']**.25)






#     #reynolds['Friction'] = (1/(-1.8*np.log10(((10/11)/3.7)**1.11+6.9/reynolds['Reynolds Number'])))**2
#     #reynolds['Blasius'] = reynolds['Friction']*1/(11*10**(-3))*1004/2*(reynolds['Reynolds Number']/(1004*11*1e-3)*(0.9096*10**(-3)))**2
#     blasius = reynolds['Blasius']
#     return blasius


# tdms = tdms_df(path)
# smooth = pressure_df_smooth(tdms)
# rough = pressure_df_rough(tdms)
# reynolds = reynolds_number(path)
# reynold = reynolds[['Reynolds Number']]
# re64 = re64(reynolds)
# sblasius = blasius_smooth(reynolds)
# rblasius = blasius_rough(reynolds)
# #print(blasius)

# reynolds['Friction'] = .316/(reynolds['Reynolds Number']**.25)
# reynolds['Blasius'] = reynolds['Friction']*1/(11*10**(-3))*1004/2*(reynolds['Reynolds Number']/(1004*11*1e-3)*(0.9096*10**(-3)))**2
# print(reynolds)

# reynolds['Friction'] = (1/(-1.8*np.log10(((10/11)/3.7)**1.11+6.9/reynolds['Reynolds Number'])))**2
# reynolds['Blasius'] = reynolds['Friction']*1/(11*10**(-3))*1004/2*(reynolds['Reynolds Number']/(1004*11*1e-3)*(0.9096*10**(-3)))**2
# print(reynolds)






# #plotting the std for pressure data
# fig, ax = plt.subplots(3,1, sharex= True)
# ax[0].plot(reynolds['Reynolds Number'])
# ax[0].legend(["Reynolds"], loc='upper right')
# ax[0].set_ylabel('Reynolds Number')
# ax[0].grid(True, which = 'both')
# ax[1].plot(smooth)
# ax[1].plot(re64)
# ax[1].plot(sblasius)
# ax[1].legend(["Smooth"], loc='upper right')
# ax[1].set_ylabel('Pressure mBarr')
# ax[1].grid(True, which = 'both')
# ax[2].plot(rough)
# ax[2].plot(re64)
# ax[2].plot(rblasius)
# ax[2].legend(["rough"], loc='upper right')
# ax[2].set_ylabel('Pressure (mBarr)')
# ax[2].grid(True, which = 'both')
# plt.show()



# from Functions import *

# path = r'C:\Users\PipeFlow\Desktop\Experiments\Old\Protrussion\10p\exp2\roughnessR_r=10P-exp2.tdms'

# tdms = tdms_df(path)
# smooth = pressure_df_smooth(tdms)
# rough = pressure_df_rough(tdms)

# s2 = smooth.reset_index()
# steps = 10
# begin = s2['Pressure Time'].min()
# start = begin
# stop = s2['Pressure Time'].max()
# itter = (stop-begin)/steps
# itter = itter.astype('int')
# avg = []
# while start < stop:
#     slices = pressure_slice_df(smooth, start, start+steps)
#     movavg = slices['Validyne8-24'].mean()
#     avg.append(movavg)
#     start = start+steps
# time = np.linspace(begin, stop, itter)
# avg = np.delete(avg, -1)





# from Functions import *

# #fetching file data

# rescan = tdms_df(r'C:\Users\PipeFlow\Desktop\Experiments\New\Protrussion\10p\ReScan8\ReScan8.tdms')
# laserdata = laser_df(r'C:\Users\PipeFlow\Desktop\Experiments\New\Protrussion\10p\ReScan8\laser1.SPEED.MSEBP.txt')
# laserdata2 = laser_df(r'C:\Users\PipeFlow\Desktop\Experiments\New\Protrussion\10p\ReScan8\laser2.SPEED.MSEBP.txt')

# # rescan = tdms_df(r'C:\Users\PipeFlow\Desktop\Experiments\Old\Protrussion\10p\exp2\roughnessR_r=10P-exp2.tdms')
# # laserdata = laser_df(r'C:\Users\PipeFlow\Desktop\Experiments\Old\Protrussion\10p\exp2\roughnessR_r=10P-exp2-1D.SPEED.MSEBP.txt')
# # laserdata2 = laser_df(r'C:\Users\PipeFlow\Desktop\Experiments\Old\Protrussion\10p\exp2\roughnessR_r=10P-exp2-2D.SPEED.MSEBP.txt')

# #defining transitional stage
# smooth = pressure_df_2(rescan, "smooth")
# rough = pressure_df_2(rescan, "rough")
# pstd = smooth_pressure_std(smooth)
# pstd1 = rough_pressure_std(rough)
# a = pstd['Standard Deviation'] > pstd['Standard Deviation'].mean()
# stran = pstd.where(a)
# c = pstd1['Standard Deviation'] > pstd1['Standard Deviation'].mean()
# rtran = pstd1.where(c)


# #moving average
# mov = pd.DataFrame()
# mov['rolling'] = smooth.rolling(1000).mean()
# mov1 = pd.DataFrame()
# mov1['rolling'] = rough.rolling(1000).mean()

# # #defining laminar stage
# # pstd['Transition'] = stran['Standard Deviation']
# # pstd['Transition'] = pstd['Transition'].fillna(0)
# # e = pstd['Transition'] == 0
# # f = pstd.where(e)


# # transitional = b
# # transitional = transitional.reset_index()
# # transitional['Pressure Time'] = transitional['Pressure Time'].round(0)
# # transitional['Pressure Time'] = transitional['Pressure Time'].astype(int)

# # print(transitional)

# #plotting the std for pressure data
# fig, ax = plt.subplots(3,1, sharex= True)
# ax[0].plot(rough)
# ax[0].plot(smooth)
# ax[0].legend(["Rough", "Smooth"], loc='upper right')
# ax[0].set_ylabel('Pressure (mBarr)')
# ax[0].grid(True, which = 'both')
# ax[1].plot(pstd1)
# ax[1].plot(pstd)
# ax[1].legend(["Rough", "Smooth"], loc='upper right')
# ax[1].set_ylabel('Standard Deviation (mBarr)')
# ax[1].grid(True, which = 'both')
# ax[2].plot(rtran)
# ax[2].plot(stran)
# ax[2].legend(["Rough", "Smooth"], loc='upper right')
# ax[2].set_ylabel('Transition')
# ax[2].grid(True, which = 'both')
# plt.show()


# rescan = tdms_df(r'C:\Users\PipeFlow\Desktop\Experiments\New\Protrussion\10p\ReScan9\ReScan9.tdms')
# smooth = pressure_df_smooth(rescan)
# rough = pressure_df_rough(rescan)

# plt.plot(smooth)
# plt.plot(rough)
# plt.show()


# from Functions import *

# path = r'C:\Users\PipeFlow\Desktop\Experiments\New\Protrussion\10p\ReScan20\ReScan20.tdms'
# pressure = tdms_df(path)
# smooth = pressure_df_smooth(pressure)
# rough = pressure_df_rough(pressure)

# def pressure_drop(reservoir, entry, exit):
#     res = reservoir-79
#     ent = 51.2-res
#     before = ((entry-ent)/1.02)/(108.6+res)*100
#     before = round(before)
#     bef = 'pressure drop before entrance is'
#     pipe = ((exit - entry)/1.02)/(108.6+res)*100
#     pipe = round(pipe)
#     pip = 'pressure drop in the pipe is'
#     after = ((159.8-exit)/1.02)/(108.6+res)*100
#     after = round(after)
#     aft = 'pressure drop after the pipe is'

#     return bef, before, pip, pipe, aft, after

# check = pressure_drop(151.8, 75.6, 92.2)
# print(check)

# from Functions import *
# path = r'C:\Users\PipeFlow\Desktop\Experiments\New\Protrussion\10p\ReScan30\ReScan30.tdms'
# #pressure readings
# pressure = tdms_df(path)
# smooth = pressure_df_smooth(pressure)
# rough = pressure_df_rough(pressure)
# pres = smooth.merge(rough, left_index=True, right_index=True)
# #pres['sum'] = (pres['Validyne8-24']+pres['Validyne 6-32'])

# #reynolds number
# reynolds = reynolds_number(pressure)
# reynolds = reynolds.reset_index()
# reynolds = reynolds.rename(columns={'Flow Rate Time':'Pressure Time'})
# reynolds = reynolds.set_index('Pressure Time')

# #print(reynolds)

# #standard deviation for rough pressure data
# def reynolds_std(reynolds):
#     r2 = reynolds.reset_index()
#     steps = 10
#     slices = 50
#     begin = r2['Pressure Time'].min()
#     start = begin
#     end1 = r2['Pressure Time'].max()
#     end = round(end1/steps)*steps
#     itter = (end-begin)/steps
#     itter = itter.astype('int')
#     sdev = []
#     while begin < end:
#         slicer = pressure_slice_df(reynolds, begin, begin+slices)
#         stand = slicer['Reynolds Number'].std()
#         sdev.append(stand)
#         begin = begin+steps
#     time = np.linspace(start, end, itter,)
#     sdev.pop()
#     d = {'Pressure Time':time, 'Standard Deviation':sdev}
#     sdeviation = pd.DataFrame(d)
#     #sdeviation['Standard Deviation'] =   (sdeviation['Standard Deviation']-  sdeviation['Standard Deviation'].min())/(sdeviation['Standard Deviation'].max()-sdeviation['Standard Deviation'].min())
#     sdeviation['Standard Deviation'] =   (sdeviation['Standard Deviation']-  sdeviation['Standard Deviation'].mean())/  sdeviation['Standard Deviation'].std()
#     sdeviation = sdeviation.set_index('Pressure Time')
#     return sdeviation

# #standard deviation of reynolds number
# reystd = reynolds_std(reynolds)
# print(reystd)

# from Functions import *
# import seaborn as sns
# from mpl_toolkits.mplot3d import Axes3D

# df = pd.read_excel(r'c:\Users\PipeFlow\Desktop\Pressure Drop 11202023\12042023\Fluctuation Table.xlsx')
# corr = df.corr()
# # sns.heatmap(corr, 
# #             xticklabels=corr.columns.values,
# #             yticklabels=corr.columns.values)
# # sns.lmplot(x='Before', y='Reynolds', data=df)
# # sns.lmplot(x='During', y='Reynolds', data=df)
# # sns.lmplot(x='After', y='Reynolds', data=df)

# fig = plt.figure()
# ax = fig.add_subplot(projection='3d')
# ax.scatter(df['Before'], df['After'], df['Reynolds'], c=df['During'], cmap=plt.hot())
# ax.set_xlabel('Before')
# ax.set_ylabel('After')
# ax.set_zlabel('Reynolds')
# # my_cmap = plt.get_cmap('hsv')
# # scct = ax.scatter3D(df['Before'], df['After'], df['Reynolds'], alpha = 0.8, c = (df['Before']+df['After']+df['Reynolds']), cmap = my_cmap)
# # fig.colorbar(scct)
# plt.show()



# #function to interpolate data
# def laser_df_interpolate(laser_df_for_graph):
#     laser1 = laser_df_for_graph
#     laser1 = laser1.reset_index()
#     laser1['Device Time'] = laser1['Device Time'].round(1)
#     max = laser1['Device Time'].max()
#     laser2 = pd.DataFrame()
#     laser2['milliseconds'] = (laser1.index+1)/10
#     a = laser2['milliseconds'] < (max+.1)
#     b = laser2.where(a)
#     laser2 = b.dropna()
#     laser2['index'] = laser2.index
#     laser2 = laser2.set_index('milliseconds')
#     laser1['Device Time'] = laser1['Device Time'].drop_duplicates(keep='first')
#     laser1 = laser1.dropna()
#     laser1 = laser1.reset_index()
#     laser1 = laser1.drop('index', axis='columns')
#     laser1 = laser1.set_index('Device Time')
#     laser3 = laser2.join(laser1, lsuffix='_caller', rsuffix='_other')
#     laser3 = laser3.reset_index()
#     laser3 = laser3.drop('index', axis='columns')
#     laser3 = laser3.interpolate(method='linear')
#     laser3 = laser3.rename(columns={'milliseconds':'Device Time'})
#     laser3 = laser3.set_index('Device Time')
#     return laser3

# from Functions import *
# import mysql.connector
# from mysql.connector import Error
# from sqlalchemy import create_engine
# from sqlalchemy import URL
# import pandasql as psd

# # host_name = '***REMOVED***'
# # db_name = '10p_experiment1'
# # u_name = 'root'
# # u_pass = '***REMOVED***'
# # port_num = '3306'
# url_object = URL.create('mysql+mysqlconnector',
#                         username = 'root',
#                         password = '***REMOVED***',
#                         host = '***REMOVED***',
#                         database = '10p_experiment1',)

# path = r'C:\Users\PipeFlow\Desktop\Experiments\Old\Protrussion\10p\exp3\roughnessR_r=10P-exp3.tdms'
# ldv1 = r'C:\Users\PipeFlow\Desktop\Experiments\Old\Protrussion\10p\exp3\roughnessR_r=10P-exp3-1D.SPEED.MSEBP.txt'
# ldv2 = r'C:\Users\PipeFlow\Desktop\Experiments\Old\Protrussion\10p\exp3\roughnessR_r=10P-exp3-2D.SPEED.MSEBP.txt'

# pressure = tdms_df(path)
# laser1 = laser_df(ldv1)
# laser2 = laser_df(ldv2)

# # my_eng = create_engine('mysql+mysqlconnector://'+u_name+':'+u_pass+'@'+host_name+':'+'3306'+'/'+db_name)
# my_eng = create_engine(url_object)
# pressure.to_sql(name='Pressure', con=my_eng, if_exists = 'replace', index=False)
# laser1.to_sql(name='Laser1', con=my_eng, if_exists = 'replace', index=False)
# laser2.to_sql(name='Laser2', con=my_eng, if_exists = 'replace', index=False)



# from Functions import *
# import mysql.connector
# from mysql.connector import Error
# import sqlalchemy
# from sqlalchemy import create_engine
# from sqlalchemy import URL


# experiment = '10p_experiment1'
# url_object = URL.create('mysql+mysqlconnector',
#                         username = 'root',
#                         password = '***REMOVED***',
#                         host = '***REMOVED***',
#                         database = experiment,)
# my_eng = create_engine(url_object)

# pressure = pd.read_sql_table('pressure', my_eng)
# pressure = pressure.set_index('index')
# laser1 = pd.read_sql_table('laser1', my_eng)
# laser1 = laser1.set_index('Device Time')
# laser2 = pd.read_sql_table('laser2', my_eng)
# laser2 = laser2.set_index('Device Time')
# print(pressure)
# print(laser1)
# print(laser2)

# def sql_data(experiment):
#     url_object = URL.create('mysql+mysqlconnector',
#                         username = 'root',
#                         password = '***REMOVED***',
#                         host = '***REMOVED***',
#                         database = experiment,)
#     my_eng = create_engine(url_object)

#     pressure = pd.read_sql_table('pressure', my_eng)
#     pressure = pressure.set_index('index')
#     laser1 = pd.read_sql_table('laser1', my_eng)
#     laser1 = laser1.set_index('Device Time')
#     laser2 = pd.read_sql_table('laser2', my_eng)
#     laser2 = laser2.set_index('Device Time')
#     return pressure, laser1, laser2

# experiment = '10p_experiment1'
# data = sql_data(experiment)
# print(data[0])
# print(data[1])
# print(data[2])

# #moving average
# mov = pd.DataFrame()
# mov['rolling'] = smooth.rolling(1000).mean()
# mov1 = pd.DataFrame()
# mov1['rolling'] = rough.rolling(1000).mean()