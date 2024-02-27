from Functions import *

#fetching file data
experiment = ''
engine = create_sql_engine(experiment)
(pressure) = read_table(engine, 'pressure')

smootherror = .1
rough1error = .1
rough2error = .1


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

#velocity
velSquared = ((reynolds['Reynolds Number']*dynamicViscosity)/(density*diameter))**2

#---------------------------------------------------Smooth
#validyne8-24
Validyne824 = pressure[['Flow Rate Time', 'Validyne8-24']]
Validyne824['Flow Rate Time'] = Validyne824['Flow Rate Time'].round(2)
Validyne824 = Validyne824.set_index('Flow Rate Time')

#friction factor
pipe = ((Validyne824['Validyne8-24']/2)*mbarToPa * 2 * diameter) / (velSquared * density * pressureSensorLength)
pipe = pipe.tail(-1)
pipe = pd.DataFrame(pipe, columns=['Friction Factor'])
pipe['Reynolds Number'] = reynolds
pipe = pipe[['Reynolds Number', 'Friction Factor']]
pipe.dropna(inplace=True)
pipe = pipe.sort_values(by=['Reynolds Number'])

#averaging pressure data
start = pipe['Reynolds Number'].min()
end = pipe['Reynolds Number'].max()
fri = []
re = []
while start < end:
    slicer = reynolds_slice(pipe, start, start+100)
    avg = slicer['Friction Factor'].mean()
    avg1 = slicer['Reynolds Number'].mean()
    fri.append(avg)
    re.append(avg1)
    start = start+100
fri = np.array(fri)
re = np.array(re)
d = {'Reynolds Number': re, 'Friction Factor':fri}
friction1 = pd.DataFrame(d)
friction1 = np.log10(friction1)
friction1 = friction1.set_index('Reynolds Number')

#---------------------------------------------------Smooth Error
#Validyne8-24 error
Validyne824 = pressure[['Flow Rate Time', 'Validyne8-24']]
Validyne824['Flow Rate Time'] = Validyne824['Flow Rate Time'].round(2)
Validyne824 = Validyne824.set_index('Flow Rate Time')

#friction factor for error
pipe = (((Validyne824['Validyne8-24']/2)+smootherror)*mbarToPa * 2 * diameter) / (velSquared * density * pressureSensorLength)
pipe = pipe.tail(-1)
pipe = pd.DataFrame(pipe, columns=['Friction Factor'])
pipe['Reynolds Number'] = reynolds
pipe = pipe[['Reynolds Number', 'Friction Factor']]
pipe.dropna(inplace=True)
pipe = pipe.sort_values(by=['Reynolds Number'])

#averaging pressure data
start = pipe['Reynolds Number'].min()
end = pipe['Reynolds Number'].max()
fri = []
re = []
while start < end:
    slicer = reynolds_slice(pipe, start, start+100)
    avg = slicer['Friction Factor'].mean()
    avg1 = slicer['Reynolds Number'].mean()
    fri.append(avg)
    re.append(avg1)
    start = start+100
fri = np.array(fri)
re = np.array(re)
d = {'Reynolds Number': re, 'Friction Factor':fri}
friction2 = pd.DataFrame(d)
friction2 = np.log10(friction2)
friction2 = friction2.set_index('Reynolds Number')

#---------------------------------------------------Rough1
#validyne 6-32
Validyne632 = pressure[['Flow Rate Time', 'Validyne 6-32']]
Validyne632['Flow Rate Time'] = Validyne632['Flow Rate Time'].round(2)
Validyne632 = Validyne632.set_index('Flow Rate Time')

#friction factor
pipe = (Validyne632['Validyne 6-32']*mbarToPa * 2 * diameter) / (velSquared * density * pressureSensorLength)
pipe = pipe.tail(-1)
pipe = pd.DataFrame(pipe, columns=['Friction Factor'])
pipe['Reynolds Number'] = reynolds
pipe = pipe[['Reynolds Number', 'Friction Factor']]
pipe.dropna(inplace=True)
pipe = pipe.sort_values(by=['Reynolds Number'])

#averaging pressure data
start = pipe['Reynolds Number'].min()
end = pipe['Reynolds Number'].max()
fri = []
re = []
while start < end:
    slicer = reynolds_slice(pipe, start, start+100)
    avg = slicer['Friction Factor'].mean()
    avg1 = slicer['Reynolds Number'].mean()
    fri.append(avg)
    re.append(avg1)
    start = start+100
fri = np.array(fri)
re = np.array(re)
d = {'Reynolds Number': re, 'Friction Factor':fri}
friction3 = pd.DataFrame(d)
friction3 = np.log10(friction3)
friction3 = friction3.set_index('Reynolds Number')

#---------------------------------------------------Rough1 Error
#Validyne 6-32 error
Validyne632 = pressure[['Flow Rate Time', 'Validyne 6-32']]
Validyne632['Flow Rate Time'] = Validyne632['Flow Rate Time'].round(2)
Validyne632 = Validyne632.set_index('Flow Rate Time')

#friction factor for error
pipe = ((Validyne632['Validyne 6-32']+rough1error)*mbarToPa * 2 * diameter) / (velSquared * density * pressureSensorLength)
pipe = pipe.tail(-1)
pipe = pd.DataFrame(pipe, columns=['Friction Factor'])
pipe['Reynolds Number'] = reynolds
pipe = pipe[['Reynolds Number', 'Friction Factor']]
pipe.dropna(inplace=True)
pipe = pipe.sort_values(by=['Reynolds Number'])

#averaging pressure data
start = pipe['Reynolds Number'].min()
end = pipe['Reynolds Number'].max()
fri = []
re = []
while start < end:
    slicer = reynolds_slice(pipe, start, start+100)
    avg = slicer['Friction Factor'].mean()
    avg1 = slicer['Reynolds Number'].mean()
    fri.append(avg)
    re.append(avg1)
    start = start+100
fri = np.array(fri)
re = np.array(re)
d = {'Reynolds Number': re, 'Friction Factor':fri}
friction4 = pd.DataFrame(d)
friction4 = np.log10(friction4)
friction4 = friction4.set_index('Reynolds Number')

#---------------------------------------------------Rough2
#validyne8-22
Validyne822 = pressure[['Flow Rate Time', 'Validyne8-22']]
Validyne822['Flow Rate Time'] = Validyne822['Flow Rate Time'].round(2)
Validyne822 = Validyne822.set_index('Flow Rate Time')

#friction factor
pipe = (Validyne822['Validyne8-22']*mbarToPa * 2 * diameter) / (velSquared * density * pressureSensorLength)
pipe = pipe.tail(-1)
pipe = pd.DataFrame(pipe, columns=['Friction Factor'])
pipe['Reynolds Number'] = reynolds
pipe = pipe[['Reynolds Number', 'Friction Factor']]
pipe.dropna(inplace=True)
pipe = pipe.sort_values(by=['Reynolds Number'])

#averaging pressure data
start = pipe['Reynolds Number'].min()
end = pipe['Reynolds Number'].max()
fri = []
re = []
while start < end:
    slicer = reynolds_slice(pipe, start, start+100)
    avg = slicer['Friction Factor'].mean()
    avg1 = slicer['Reynolds Number'].mean()
    fri.append(avg)
    re.append(avg1)
    start = start+100
fri = np.array(fri)
re = np.array(re)
d = {'Reynolds Number': re, 'Friction Factor':fri}
friction5 = pd.DataFrame(d)
friction5 = np.log10(friction5)
friction5 = friction5.set_index('Reynolds Number')

#---------------------------------------------------Rough2 Error
#Validyne822 error
Validyne822 = pressure[['Flow Rate Time', 'Validyne8-22']]
Validyne822['Flow Rate Time'] = Validyne822['Flow Rate Time'].round(2)
Validyne822 = Validyne822.set_index('Flow Rate Time')

#friction factor for error
pipe = ((Validyne822['Validyne8-22']+rough2error)*mbarToPa * 2 * diameter) / (velSquared * density * pressureSensorLength)
pipe = pipe.tail(-1)
pipe = pd.DataFrame(pipe, columns=['Friction Factor'])
pipe['Reynolds Number'] = reynolds
pipe = pipe[['Reynolds Number', 'Friction Factor']]
pipe.dropna(inplace=True)
pipe = pipe.sort_values(by=['Reynolds Number'])

#averaging pressure data
start = pipe['Reynolds Number'].min()
end = pipe['Reynolds Number'].max()
fri = []
re = []
while start < end:
    slicer = reynolds_slice(pipe, start, start+100)
    avg = slicer['Friction Factor'].mean()
    avg1 = slicer['Reynolds Number'].mean()
    fri.append(avg)
    re.append(avg1)
    start = start+100
fri = np.array(fri)
re = np.array(re)
d = {'Reynolds Number': re, 'Friction Factor':fri}
friction6 = pd.DataFrame(d)
friction6 = np.log10(friction6)
friction6 = friction6.set_index('Reynolds Number')

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

#-----------------------------------------------------------------------------------------------Error Bars
friction1['Error'] = friction2['Friction Factor']-friction1['Friction Factor']
friction1 = friction1.reset_index()

friction3['Error'] = friction4['Friction Factor']-friction3['Friction Factor']
friction3 = friction3.reset_index()

friction5['Error'] = friction6['Friction Factor']-friction5['Friction Factor']
friction5 = friction5.reset_index()

#-----------------------------------------------------------------------------------------------Graph
fig, ax = plt.subplots()
ax.errorbar(friction1['Reynolds Number'], friction1['Friction Factor'], yerr = friction1['Error'])
ax.errorbar(friction3['Reynolds Number'], friction3['Friction Factor'], yerr = friction3['Error'])
ax.errorbar(friction5['Reynolds Number'], friction5['Friction Factor'], yerr = friction5['Error'])
ax.plot(lam)
ax.plot(tur)
ax.set_xlabel('log Re')
ax.set_ylabel('log f')
ax.legend(['64/Re', 'Blasius', 'Smooth', 'Rough1', 'Rough2'])
ax.grid()
plt.show()