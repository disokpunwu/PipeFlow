from Functions import *

#function to slice pressure data
def reynolds_slice(data, Start, End):
    sliceddata = data
    a = sliceddata['Reynolds Number'] > (Start-.1)
    b = sliceddata.where(a)
    c = b.dropna()
    d = c['Reynolds Number'] < (End+.1)
    e = c.where(d)
    sliceddata = e.dropna()
    return sliceddata  

#reynolds range
num10p = np.arange(100,10100,100)
num110p = np.arange(1200,10100,100)

#constants
density = 1004 # kg/m^3
dynamicViscosity = 0.9096 * (10**-3)
diameter = 11 * (10**-3)
mbarToPa = 100
pressureSensorLength = 1


#-----------------------------------------------------------------------------------------------
#fetching file data
experiment1 = '4v_ReScan9'
data1 = sql_data1(experiment1)
pressure1 = data1


#reynolds number
reynolds1 = reynolds_number(pressure1)

#validyne6-32
val1 = pressure1[['Flow Rate Time', 'Validyne 6-32']]
val1['Flow Rate Time'] = val1['Flow Rate Time'].round(2)
val1 = val1.set_index('Flow Rate Time')

#velocity
velSquared1 = ((reynolds1['Reynolds Number']*dynamicViscosity)/(density*diameter))**2

#friction factor
fri1 = (val1['Validyne 6-32']*mbarToPa * 2 * diameter) / (velSquared1 * density * pressureSensorLength)
fri1 = fri1.tail(-1)
fri1 = pd.DataFrame(fri1, columns=['Friction Factor'])
fri1['Reynolds Number'] = reynolds1
fri1 = fri1[['Reynolds Number', 'Friction Factor']]
fri1.dropna(inplace=True)

#averaging pressure data
start1 = fri1['Reynolds Number'].min()
end1 = fri1['Reynolds Number'].max()
fri11 = []
re11 = []
while start1 < end1:
    slicer1 = reynolds_slice(fri1, start1, start1+100)
    avg1 = slicer1['Friction Factor'].mean()
    avg11 = slicer1['Reynolds Number'].mean()
    fri11.append(avg1)
    re11.append(avg11)
    start1 = start1+100
fri11 = np.array(fri11)
re11 = np.array(re11)
d1 = {'Reynolds Number': re11, 'Friction Factor':fri11}
friction1 = pd.DataFrame(d1)
friction1 = np.log10(friction1)
friction1 = friction1.set_index('Reynolds Number')


#-----------------------------------------------------------------------------------------------
#fetching file data
experiment2 = '4v_ReScan18'
data2 = sql_data1(experiment2)
pressure2 = data2


#reynolds number
reynolds2 = reynolds_number(pressure2)

#validyne6-32
val2 = pressure2[['Flow Rate Time', 'Validyne 6-32']]
val2['Flow Rate Time'] = val2['Flow Rate Time'].round(2)
val2['Validyne 6-32'] = val2['Validyne 6-32']
val2 = val2.set_index('Flow Rate Time')

#velocity
velSquared2 = ((reynolds2['Reynolds Number']*dynamicViscosity)/(density*diameter))**2

#friction factor
fri2 = (val2['Validyne 6-32']*mbarToPa * 2 * diameter) / (velSquared2 * density * pressureSensorLength)
fri2 = fri2.tail(-2)
fri2 = pd.DataFrame(fri2, columns=['Friction Factor'])
fri2['Reynolds Number'] = reynolds2
fri2 = fri2[['Reynolds Number', 'Friction Factor']]
fri2.dropna(inplace=True)

#averaging pressure data
start2 = fri2['Reynolds Number'].min()
end2 = fri2['Reynolds Number'].max()
fri22 = []
re22 = []
while start2 < end2:
    slicer2 = reynolds_slice(fri2, start2, start2+100)
    avg2 = slicer2['Friction Factor'].mean()
    avg22 = slicer2['Reynolds Number'].mean()
    fri22.append(avg2)
    re22.append(avg22)
    start2 = start2+100
fri22 = np.array(fri22)
re22 = np.array(re22)
d2 = {'Reynolds Number': re22, 'Friction Factor':fri22}
friction2 = pd.DataFrame(d2)
friction2 = np.log10(friction2)
friction2 = friction2.set_index('Reynolds Number')


#-----------------------------------------------------------------------------------------------
#fetching file data
experiment3 = '4v_ReScan18'
data3 = sql_data1(experiment3)
pressure3 = data3


#reynolds number
reynolds3 = reynolds_number(pressure3)
reynolds3 = reynolds3.tail(-1)

#validyne6-32
val3 = pressure3[['Flow Rate Time', 'Validyne8-22']]
val3['Flow Rate Time'] = val3['Flow Rate Time'].round(2)
val3 = val3.set_index('Flow Rate Time')

#velocity
velSquared3 = ((reynolds3['Reynolds Number']*dynamicViscosity)/(density*diameter))**2

#friction factor
fri3 = (val3['Validyne8-22']*mbarToPa * 2 * diameter) / (velSquared3 * density * pressureSensorLength)
fri3 = fri3.tail(-1)
fri3 = pd.DataFrame(fri3, columns=['Friction Factor'])
fri3['Reynolds Number'] = reynolds3
fri3 = fri3[['Reynolds Number', 'Friction Factor']]
fri3.dropna(inplace=True)

#averaging pressure data
start3 = fri3['Reynolds Number'].min()
end3 = fri3['Reynolds Number'].max()
fri13 = []
re13 = []
while start3 < end3:
    slicer3 = reynolds_slice(fri3, start3, start3+100)
    avg3 = slicer3['Friction Factor'].mean()
    avg13 = slicer3['Reynolds Number'].mean()
    fri13.append(avg3)
    re13.append(avg13)
    start3 = start3+100
fri13 = np.array(fri13)
re13 = np.array(re13)
d3 = {'Reynolds Number': re13, 'Friction Factor':fri13}
friction3 = pd.DataFrame(d3)
friction3 = np.log10(friction3)
friction3 = friction3.set_index('Reynolds Number')


#-----------------------------------------------------------------------------------------------
#fetching file data
experiment4 = '10p_ReScan50'
data4 = sql_data1(experiment4)
pressure4 = data4


#reynolds number
reynolds4 = reynolds_number(pressure4)
reynolds4 = reynolds4.tail(-1)

#validyne6-32
val4 = pressure4[['Flow Rate Time', 'Validyne 6-32']]
val4['Flow Rate Time'] = val4['Flow Rate Time'].round(2)
val4['Validyne 6-32'] = val4['Validyne 6-32']
val4 = val4.set_index('Flow Rate Time')

#velocity
velSquared4 = ((reynolds4['Reynolds Number']*dynamicViscosity)/(density*diameter))**2

#friction factor
fri4 = (val4['Validyne 6-32']*mbarToPa * 2 * diameter) / (velSquared4 * density * pressureSensorLength)
fri4 = fri4.tail(-1)
fri4 = pd.DataFrame(fri4, columns=['Friction Factor'])
fri4['Reynolds Number'] = reynolds4
fri4 = fri4[['Reynolds Number', 'Friction Factor']]
fri4.dropna(inplace=True)

#averaging pressure data
start4 = fri4['Reynolds Number'].min()
end4 = fri4['Reynolds Number'].max()
fri14 = []
re14 = []
while start4 < end4:
    slicer4 = reynolds_slice(fri4, start4, start4+100)
    avg4 = slicer4['Friction Factor'].mean()
    avg14 = slicer4['Reynolds Number'].mean()
    fri14.append(avg4)
    re14.append(avg14)
    start4 = start4+100
fri14 = np.array(fri14)
re14 = np.array(re14)
d4 = {'Reynolds Number': re14, 'Friction Factor':fri14}
friction4 = pd.DataFrame(d4)
friction4 = np.log10(friction4)
friction4 = friction4.set_index('Reynolds Number')


#-----------------------------------------------------------------------------------------------
#fetching file data
experiment5 = '10p_ReScan3'
data5 = sql_data1(experiment5)
pressure5 = data5


#reynolds number
reynolds5 = reynolds_number(pressure5)
reynolds5 = reynolds5.tail(-1)

#validyne6-32
val5 = pressure5[['Flow Rate Time', 'Validyne 6-32']]
val5['Flow Rate Time'] = val5['Flow Rate Time'].round(2)
val5 = val5.set_index('Flow Rate Time')

#velocity
velSquared5 = ((reynolds5['Reynolds Number']*dynamicViscosity)/(density*diameter))**2

#friction factor
fri5 = (val5['Validyne 6-32']*mbarToPa * 2 * diameter) / (velSquared5 * density * pressureSensorLength)
fri5 = fri5.tail(-1)
fri5 = pd.DataFrame(fri5, columns=['Friction Factor'])
fri5['Reynolds Number'] = reynolds5
fri5 = fri5[['Reynolds Number', 'Friction Factor']]
fri5.dropna(inplace=True)

#averaging pressure data
start5 = fri5['Reynolds Number'].min()
end5 = fri5['Reynolds Number'].max()
fri15 = []
re15 = []
while start5 < end5:
    slicer5 = reynolds_slice(fri5, start5, start5+100)
    avg5 = slicer5['Friction Factor'].mean()
    avg15 = slicer5['Reynolds Number'].mean()
    fri15.append(avg5)
    re15.append(avg15)
    start5 = start5+100
fri15 = np.array(fri15)
re15 = np.array(re15)
d5 = {'Reynolds Number': re15, 'Friction Factor':fri15}
friction5 = pd.DataFrame(d5)
friction5 = np.log10(friction5)
friction5 = friction5.set_index('Reynolds Number')


#-----------------------------------------------------------------------------------------------
#fetching file data
experiment6 = '10p_ReScan4'
data6 = sql_data1(experiment6)
pressure6 = data6


#reynolds number
reynolds6 = reynolds_number(pressure6)
reynolds6 = reynolds6.tail(-1)

#validyne6-32
val6 = pressure6[['Flow Rate Time', 'Validyne 6-32']]
val6['Flow Rate Time'] = val6['Flow Rate Time'].round(2)
val6 = val6.set_index('Flow Rate Time')

#velocity
velSquared6 = ((reynolds6['Reynolds Number']*dynamicViscosity)/(density*diameter))**2

#friction factor
fri6 = (val6['Validyne 6-32']*mbarToPa * 2 * diameter) / (velSquared6 * density * pressureSensorLength)
fri6 = fri6.tail(-1)
fri6 = pd.DataFrame(fri6, columns=['Friction Factor'])
fri6['Reynolds Number'] = reynolds6
fri6 = fri6[['Reynolds Number', 'Friction Factor']]
fri6.dropna(inplace=True)

#averaging pressure data
start6 = fri6['Reynolds Number'].min()
end6 = fri6['Reynolds Number'].max()
fri16 = []
re16 = []
while start6 < end6:
    slicer6 = reynolds_slice(fri6, start6, start6+100)
    avg6 = slicer6['Friction Factor'].mean()
    avg16 = slicer6['Reynolds Number'].mean()
    fri16.append(avg6)
    re16.append(avg16)
    start6 = start6+100
fri16 = np.array(fri16)
re16 = np.array(re16)
d6 = {'Reynolds Number': re16, 'Friction Factor':fri16}
friction6 = pd.DataFrame(d6)
friction6 = np.log10(friction6)
friction6 = friction6.set_index('Reynolds Number')


#-----------------------------------------------------------------------------------------------
#fetching file data
experiment7 = '10p_ReScan5'
data7 = sql_data1(experiment7)
pressure7 = data7

#reynolds number
reynolds7 = reynolds_number(pressure7)
reynolds7 = reynolds7.tail(-1)

#validyne6-32
val7 = pressure7[['Flow Rate Time', 'Validyne 6-32']]
val7['Flow Rate Time'] = val7['Flow Rate Time'].round(2)
val7 = val7.set_index('Flow Rate Time')

#velocity
velSquared7 = ((reynolds7['Reynolds Number']*dynamicViscosity)/(density*diameter))**2

#friction factor
fri7 = (val7['Validyne 6-32']*mbarToPa * 2 * diameter) / (velSquared7 * density * pressureSensorLength)
fri7 = fri7.tail(-1)
fri7 = pd.DataFrame(fri7, columns=['Friction Factor'])
fri7['Reynolds Number'] = reynolds7
fri7 = fri7[['Reynolds Number', 'Friction Factor']]
fri7.dropna(inplace=True)

#averaging pressure data
start7 = fri7['Reynolds Number'].min()
end7 = fri7['Reynolds Number'].max()
fri17 = []
re17 = []
while start7 < end7:
    slicer7 = reynolds_slice(fri7, start7, start7+100)
    avg7 = slicer7['Friction Factor'].mean()
    avg17 = slicer7['Reynolds Number'].mean()
    fri17.append(avg7)
    re17.append(avg17)
    start7 = start7+100
fri17 = np.array(fri17)
re17 = np.array(re17)
d7 = {'Reynolds Number': re17, 'Friction Factor':fri17}
friction7 = pd.DataFrame(d7)
friction7 = np.log10(friction7)
friction7 = friction7.set_index('Reynolds Number')


#-----------------------------------------------------------------------------------------------
#fetching file data
experiment8 = '10p_ReScan6'
data8 = sql_data1(experiment8)
pressure8 = data8

#reynolds number
reynolds8 = reynolds_number(pressure8)
reynolds8 = reynolds8.tail(-1)

#validyne6-32
val8 = pressure8[['Flow Rate Time', 'Validyne 6-32']]
val8['Flow Rate Time'] = val8['Flow Rate Time'].round(2)
val8 = val8.set_index('Flow Rate Time')

#velocity
velSquared8 = ((reynolds8['Reynolds Number']*dynamicViscosity)/(density*diameter))**2

#friction factor
fri8 = (val8['Validyne 6-32']*mbarToPa * 2 * diameter) / (velSquared8 * density * pressureSensorLength)
fri8 = fri8.tail(-1)
fri8 = pd.DataFrame(fri8, columns=['Friction Factor'])
fri8['Reynolds Number'] = reynolds8
fri8 = fri8[['Reynolds Number', 'Friction Factor']]
fri8.dropna(inplace=True)

#averaging pressure data
start8 = fri8['Reynolds Number'].min()
end8 = fri8['Reynolds Number'].max()
fri18 = []
re18 = []
while start8 < end8:
    slicer8 = reynolds_slice(fri8, start8, start8+100)
    avg8 = slicer8['Friction Factor'].mean()
    avg18 = slicer8['Reynolds Number'].mean()
    fri18.append(avg8)
    re18.append(avg18)
    start8 = start8+100
fri18 = np.array(fri18)
re18 = np.array(re18)
d8 = {'Reynolds Number': re18, 'Friction Factor':fri18}
friction8 = pd.DataFrame(d8)
friction8 = np.log10(friction8)
friction8 = friction8.set_index('Reynolds Number')

#-----------------------------------------------------------------------------------------------
#fetching file data
experiment9 = '10p_ReScan7'
data9 = sql_data1(experiment9)
pressure9 = data9

#reynolds number
reynolds9 = reynolds_number(pressure9)
reynolds9 = reynolds9.tail(-1)

#validyne6-32
val9 = pressure9[['Flow Rate Time', 'Validyne 6-32']]
val9['Flow Rate Time'] = val9['Flow Rate Time'].round(2)
val9 = val9.set_index('Flow Rate Time')

#velocity
velSquared9 = ((reynolds9['Reynolds Number']*dynamicViscosity)/(density*diameter))**2

#friction factor
fri9 = (val9['Validyne 6-32']*mbarToPa * 2 * diameter) / (velSquared9 * density * pressureSensorLength)
fri9 = fri9.tail(-1)
fri9 = pd.DataFrame(fri9, columns=['Friction Factor'])
fri9['Reynolds Number'] = reynolds9
fri9 = fri9[['Reynolds Number', 'Friction Factor']]
fri9.dropna(inplace=True)

#averaging pressure data
start9 = fri9['Reynolds Number'].min()
end9 = fri9['Reynolds Number'].max()
fri19 = []
re19 = []
while start9 < end9:
    slicer9 = reynolds_slice(fri9, start9, start9+100)
    avg9 = slicer9['Friction Factor'].mean()
    avg19 = slicer9['Reynolds Number'].mean()
    fri19.append(avg9)
    re19.append(avg19)
    start9 = start9+100
fri19 = np.array(fri19)
re19 = np.array(re19)
d9 = {'Reynolds Number': re19, 'Friction Factor':fri19}
friction9 = pd.DataFrame(d9)
friction9 = np.log10(friction9)
friction9 = friction9.set_index('Reynolds Number')


#-----------------------------------------------------------------------------------------------
#fetching file data
experiment10 = '10p_ReScan8'
data10 = sql_data1(experiment10)
pressure10 = data10

#reynolds number
reynolds10 = reynolds_number(pressure10)
reynolds10 = reynolds10.tail(-1)

#validyne6-32
val10 = pressure10[['Flow Rate Time', 'Validyne 6-32']]
val10['Flow Rate Time'] = val10['Flow Rate Time'].round(2)
val10 = val10.set_index('Flow Rate Time')

#velocity
velSquared10 = ((reynolds10['Reynolds Number']*dynamicViscosity)/(density*diameter))**2

#friction factor
fri10 = (val10['Validyne 6-32']*mbarToPa * 2 * diameter) / (velSquared10 * density * pressureSensorLength)
fri10 = fri10.tail(-1)
fri10 = pd.DataFrame(fri10, columns=['Friction Factor'])
fri10['Reynolds Number'] = reynolds10
fri10 = fri10[['Reynolds Number', 'Friction Factor']]
fri10.dropna(inplace=True)

#averaging pressure data
start10 = fri10['Reynolds Number'].min()
end10 = fri10['Reynolds Number'].max()
fri110 = []
re110 = []
while start10 < end10:
    slicer10 = reynolds_slice(fri10, start10, start10+100)
    avg10 = slicer10['Friction Factor'].mean()
    avg110 = slicer10['Reynolds Number'].mean()
    fri110.append(avg10)
    re110.append(avg110)
    start10 = start10+100
fri110 = np.array(fri110)
re110 = np.array(re110)
d10 = {'Reynolds Number': re110, 'Friction Factor':fri110}
friction10 = pd.DataFrame(d10)
friction10 = np.log10(friction10)
friction10 = friction10.set_index('Reynolds Number')

#-----------------------------------------------------------------------------------------------64/re & Blasius
#64/re line
lam = pd.DataFrame(num10p, columns=['Reynolds Number'])
lam['64/re'] = 64/lam['Reynolds Number']
lam= np.log10(lam)
lam = lam.set_index('Reynolds Number')

#Blasius line
tur = pd.DataFrame(num110p, columns=['Reynolds Number'])
tur['blasius'] = .316/(tur['Reynolds Number']**.25)
tur = np.log10(tur)
tur = tur.set_index('Reynolds Number')


#-----------------------------------------------------------------------------------------------Graph
plt.plot(friction1)
plt.plot(friction2)
plt.plot(friction3)
plt.plot(friction4)
plt.plot(friction5)
plt.plot(friction6)
plt.plot(friction7)
plt.plot(friction8)
plt.plot(friction9)
plt.plot(friction10)
plt.plot(lam)
plt.plot(tur)
plt.xlabel('Log Re')
plt.ylabel('Log f')
plt.legend(['4v9 1st Meter', '4v18 1st Meter', '4v18 3rd Meter', '10p50 1st Meter' '64/Re', 'Blasius'])
plt.grid()
plt.show()



