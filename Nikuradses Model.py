from Functions import *

#fetching file data
experiment = ''
data = sql_data(experiment)
pressure = data[0]
laser1 = data[1]
laser2 = data[2]

#reynolds range
num = np.arange(100,10100,100)
num1 = np.arange(1200,10100,100)

#reynolds number
reynolds = reynolds_number(pressure)
reynolds = reynolds.tail(-1)

#velocity squared
vel = ((reynolds['Reynolds Number']*(0.9096*10**(-3)))/1004*1)**2


#---------------------------------------------------Rough Section
#validyne6-32
val632 = pressure[['Flow Rate Time', 'Validyne 6-32']]
val632['Flow Rate Time'] = val632['Flow Rate Time'].round(2)
val632 = val632.set_index('Flow Rate Time')

#friction factor for rough section
rough = (val632['Validyne 6-32']/100/vel)*(.022/1004)
rough = rough.tail(-1)
rough = pd.DataFrame(rough, columns=['Friction Factor'])
rough['Reynolds Number'] = reynolds
rough = rough[['Reynolds Number', 'Friction Factor']]
rough.dropna(inplace=True)

#averaging pressure data
start = rough['Reynolds Number'].min()
end = rough['Reynolds Number'].max()
fri = []
re = []
while start < end:
    slicer = reynolds_slice(rough, start, start+100)
    avg = slicer['Friction Factor'].mean()
    avg1 = slicer['Reynolds Number'].mean()
    fri.append(avg)
    re.append(avg1)
    start = start+100
fri = np.array(fri)
re = np.array(re)
d = {'Reynolds Number': re, 'Friction Factor':fri}
friction = pd.DataFrame(d)
friction = np.log10(friction)
friction = friction.set_index('Reynolds Number')


#---------------------------------------------------Smooth Section
#validyne8-24
val824 = pressure[['Flow Rate Time', 'Validyne8-24']]
val824['Flow Rate Time'] = val824['Flow Rate Time'].round(2)
val824 = val824.set_index('Flow Rate Time')

#friction factor
smooth = (val824['Validyne8-24']/100/vel)*(.022/1004)
smooth = smooth.tail(-1)
smooth = pd.DataFrame(smooth, columns=['Friction Factor'])
smooth['Reynolds Number'] = reynolds
smooth = smooth[['Reynolds Number', 'Friction Factor']]
smooth.dropna(inplace=True)

#averaging pressure data
start1 = smooth['Reynolds Number'].min()
end1 = smooth['Reynolds Number'].max()
fri1 = []
re1 = []
while start1 < end1:
    slicer1 = reynolds_slice(smooth, start1, start1+100)
    avg2 = slicer1['Friction Factor'].mean()
    avg3 = slicer1['Reynolds Number'].mean()
    fri1.append(avg2)
    re1.append(avg3)
    start1 = start1+100
fri1 = np.array(fri1)
re1 = np.array(re1)
d1 = {'Reynolds Number': re1, 'Friction Factor':fri1}
friction1 = pd.DataFrame(d1)
friction1 = np.log10(friction1)
friction1 = friction1.set_index('Reynolds Number')


#-----------------------------------------------------------------------------------------------64/re & Blasius
#64/re line
lam = pd.DataFrame(num, columns=['Reynolds Number'])
lam['64/re'] = 64/lam['Reynolds Number']
lam = np.log10(lam)
lam = lam.set_index('Reynolds Number')

#Blasius line
tur = pd.DataFrame(num1, columns=['Reynolds Number'])
tur['blasius'] = .316/(tur['Reynolds Number']**.25)
tur = np.log10(tur)
tur = tur.set_index('Reynolds Number')


#-----------------------------------------------------------------------------------------------Graph
plt.plot(friction)
plt.plot(friction1)
plt.plot(lam)
plt.plot(tur)
plt.xlabel('log Re')
plt.ylabel('log f')
plt.legend(['Rough', 'Smooth', '64/Re', 'Blasius'])
plt.grid() 
plt.show()