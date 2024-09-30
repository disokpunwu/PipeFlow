from Functions import *
from MainConfigurationFile import roughness, experiment
#Retrieve Data from Experiment
actualpath = getExperimentPath(roughness, experiment)
pressure = tdms_df(actualpath)

#reynolds range
num = np.arange(100,10100,100)
num1 = np.arange(1200,10100,100)

#Timestamp for Steps
StartTimes = np.arange(100,5700,200)
EndTimes = np.arange(200,5800,200)

#Steps
FirstStep = 1
LastStep = np.count_nonzero(StartTimes)

#reynolds number
reynolds = reynolds_number(pressure)

#constants
density = 1004 # kg/m^3
dynamicViscosity = 0.9096 * (10**-3)
diameter = 11 * (10**-3)
mbarToPa = 100
pressureSensorLength = 1

#velocity
velSquared = ((reynolds['Reynolds Number']*dynamicViscosity)/(density*diameter))**2

#---------------------------------------------------Rough Section
#validyne6-32
val632 = pressure[['Flow Rate Time', 'Validyne 6-32']]
val632['Flow Rate Time'] = val632['Flow Rate Time'].round(2)
val632 = val632.set_index('Flow Rate Time')

#friction factor for rough section
rough = (val632['Validyne 6-32']*mbarToPa * 2 * diameter) / (velSquared * density * pressureSensorLength)
rough = rough.tail(-1)
rough = pd.DataFrame(rough, columns=['Friction Factor'])
rough['Reynolds Number'] = reynolds
rough = rough[['Reynolds Number', 'Friction Factor']]
rough.dropna(inplace=True)

#averaging pressure data
FirstStep = 1
LastStep = np.count_nonzero(StartTimes)
fri = []
re = []
First= StartTimes[FirstStep-1]
Last = EndTimes[FirstStep-1]
while FirstStep < LastStep:
    x = slice(First,Last)
    slicer = (rough[x])
    avg = slicer['Friction Factor'].mean()
    avg1 = slicer['Reynolds Number'].mean()
    fri.append(avg)
    re.append(avg1)
    FirstStep = FirstStep+1
    First = First+200
    Last = Last+200
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
val824['Validyne8-24'] = val824['Validyne8-24']/2
val824 = val824.set_index('Flow Rate Time')

#friction factor
smooth = (val824['Validyne8-24']*mbarToPa * 2 * diameter) / (velSquared * density * pressureSensorLength)
smooth = smooth.tail(-1)
smooth = pd.DataFrame(smooth, columns=['Friction Factor'])
smooth['Reynolds Number'] = reynolds
smooth = smooth[['Reynolds Number', 'Friction Factor']]
smooth.dropna(inplace=True)

#averaging pressure data
FirstStep = 1
LastStep = np.count_nonzero(StartTimes)
fri = []
re = []
First= StartTimes[FirstStep-1]
Last = EndTimes[FirstStep-1]
while FirstStep < LastStep:
    x = slice(First,Last)
    slicer = (smooth[x])
    avg = slicer['Friction Factor'].mean()
    avg1 = slicer['Reynolds Number'].mean()
    fri.append(avg)
    re.append(avg1)
    FirstStep = FirstStep+1
    First = First+200
    Last = Last+200
fri = np.array(fri)
re = np.array(re)
d = {'Reynolds Number': re, 'Friction Factor':fri}
friction1 = pd.DataFrame(d)
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
plt.plot(friction1)
plt.plot(friction)
plt.plot(lam)
plt.plot(tur)
plt.xlabel('log Re')
plt.ylabel('log f')
plt.legend(['Rough', '64/Re', 'Blasius'])
plt.legend(['Smooth', 'Rough', '64/Re', 'Blasius'])
plt.grid() 
plt.show()