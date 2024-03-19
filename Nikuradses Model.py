from Functions import *

#fetching file data
experiment = '15p_rescan5'
engine = create_sql_engine(experiment)
(pressure) = read_table(engine, 'pressure')


#reynolds range
num = np.arange(100,10100,100)
num1 = np.arange(1200,10100,100)

#reynolds number
reynolds = reynolds_number(pressure)
reynolds = reynolds.tail(-1)

#constants
density = 1004 # kg/m^3
dynamicViscosity = 0.9096 * (10**-3)
diameter = 11 * (10**-3)
mbarToPa = 100
pressureSensorLength = 1


#---------------------------------------------------Rough Section 1
#validyne6-32
val632 = pressure[['Flow Rate Time', 'Validyne 6-32']]
val632['Flow Rate Time'] = val632['Flow Rate Time'].round(2)
val632 = val632.set_index('Flow Rate Time')

#velocity
velSquared = ((reynolds['Reynolds Number']*dynamicViscosity)/(density*diameter))**2

#friction factor for rough section
rough = (val632['Validyne 6-32']*mbarToPa * 2 * diameter) / (velSquared * density * pressureSensorLength)
rough = rough.tail(-1)
rough = pd.DataFrame(rough, columns=['Friction Factor'])
rough['Reynolds Number'] = reynolds
rough = rough[['Reynolds Number', 'Friction Factor']]
rough.dropna(inplace=True)
rough = rough.sort_values(by=['Reynolds Number'])

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
print(friction)
friction = np.log10(friction)
friction = friction.set_index('Reynolds Number')


#---------------------------------------------------Rough Section 2
#validyne8-22
val822 = pressure[['Flow Rate Time', 'Validyne8-22']]
val822['Flow Rate Time'] = val822['Flow Rate Time'].round(2)
val822['Validyne8-22'] = val822['Validyne8-22']
val822 = val822.set_index('Flow Rate Time')

#friction factor
rough1 = (val822['Validyne8-22']*mbarToPa * 2 * diameter) / (velSquared * density * pressureSensorLength)
rough1 = rough1.tail(-1)
rough1 = pd.DataFrame(rough1, columns=['Friction Factor'])
rough1['Reynolds Number'] = reynolds
rough1 = rough1[['Reynolds Number', 'Friction Factor']]
rough1.dropna(inplace=True)
rough1 = rough1.sort_values(by=['Reynolds Number'])

#averaging pressure data
start1 = rough1['Reynolds Number'].min()
end1 = rough1['Reynolds Number'].max()
fri1 = []
re1 = []
while start1 < end1:
    slicer1 = reynolds_slice(rough1, start1, start1+100)
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


#---------------------------------------------------Smooth Section
#validyne8-24
val824 = pressure[['Flow Rate Time', 'Validyne8-24']]
val824['Flow Rate Time'] = val824['Flow Rate Time'].round(2)
val824['Validyne8-24'] = val824['Validyne8-24']/2
val824 = val824.set_index('Flow Rate Time')

#friction factor
smooth = (val824['Validyne8-24']*mbarToPa * 2 * diameter) / (velSquared * density * pressureSensorLength)
smooth = smooth.tail(-1)
smooth = pd.DataFrame(smooth, columns=['Friction Factor'])
smooth['Reynolds Number'] = reynolds
smooth = smooth[['Reynolds Number', 'Friction Factor']]
smooth.dropna(inplace=True)
smooth = smooth.sort_values(by=['Reynolds Number'])

#averaging pressure data
start11 = smooth['Reynolds Number'].min()
end11 = smooth['Reynolds Number'].max()
fri11 = []
re11 = []
while start11 < end11:
    slicer11 = reynolds_slice(smooth, start11, start11+100)
    avg21 = slicer11['Friction Factor'].mean()
    avg31 = slicer11['Reynolds Number'].mean()
    fri11.append(avg21)
    re11.append(avg31)
    start11 = start11+100
fri11 = np.array(fri11)
re11 = np.array(re11)
d11 = {'Reynolds Number': re11, 'Friction Factor':fri11}
friction11 = pd.DataFrame(d11)
friction11 = np.log10(friction11)
friction11 = friction11.set_index('Reynolds Number')


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
plt.plot(friction11)
plt.plot(friction)
plt.plot(friction1)
plt.plot(lam)
plt.plot(tur)
plt.xlabel('log Re')
plt.ylabel('log f')
plt.legend(['Smooth', 'Rough1', 'Rough2', '64/Re', 'Blasius'])
plt.grid() 
plt.show()