from Functions import *

#fetching file data
experiment = ''
engine = create_sql_engine(experiment)
(pressure) = read_table(engine, 'pressure')

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
friction_smooth = friction1.copy()
friction_smooth1 = friction1

# #---------------------------------------------------Smooth Error
#fetching file data
experiment = ''
engine = create_sql_engine(experiment)
(friction) = read_table(engine, 'friction')
friction = friction.sort_values(by='ReynoldsNumber')

#number of samples
friction_count = friction.pivot_table(index=['ReynoldsNumber'], aggfunc='size').reset_index()
friction_count = friction_count.rename(columns={0:'count'})

#mean values
friction_mean = friction.groupby('ReynoldsNumber').mean().reset_index()
friction_mean = friction_mean.rename(columns={'FrictionFactor':'mean'})

#merged table
friction1 = friction.merge(friction_mean,'inner', 'ReynoldsNumber')
friction2 = friction1.merge(friction_count,'inner', 'ReynoldsNumber')

#statistical error
friction2['MeanDiff'] = friction2['FrictionFactor']-friction2['mean']
friction2['SquaredDevi'] = friction2['MeanDiff']**2
friction3 = pd.DataFrame()
friction3['SumOfSquaredDevi'] = friction2.groupby('ReynoldsNumber')['SquaredDevi'].sum('SquaredDevi')
friction4 = friction3.merge(friction_count,'inner','ReynoldsNumber')
friction4['std'] = (friction4['SumOfSquaredDevi']/friction4['count'])**(1/2)
friction4['error'] = friction4['std']/(friction4['count']**(1/2))
friction_error_smooth = pd.DataFrame()
friction_error_smooth['ReynoldsNumber'] = friction4['ReynoldsNumber']
friction_error_smooth['Error'] = friction4['error']

#dataframes for graphing
friction_smooth['Reynolds Number'] = friction_smooth['Reynolds Number'].round(1)
friction_smooth = friction_smooth.dropna()
friction_smooth = friction_smooth.rename(columns={'Reynolds Number':'ReynoldsNumber'})
friction_smooth1 = friction_smooth1.dropna()
friction_error_smooth = friction_smooth.merge(friction_error_smooth, 'inner', 'ReynoldsNumber')
friction_smooth1 = friction_smooth1.merge(friction_error_smooth, 'inner', 'Friction Factor')


friction_error_smooth = friction_smooth1.drop(['Friction Factor', 'ReynoldsNumber'], axis=1)
friction_smooth = friction_smooth1.drop(['Error', 'ReynoldsNumber'], axis=1)
friction_smooth1 = friction_smooth1.drop(['Error', 'ReynoldsNumber'], axis=1).set_index('Reynolds Number')

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
friction_rough = friction.copy()
friction_rough1 = friction

#---------------------------------------------------Rough Error
#fetching file data
experiment = ''
engine = create_sql_engine(experiment)
(friction) = read_table(engine, 'friction')
friction = friction.sort_values(by='ReynoldsNumber')

#number of samples
friction_count = friction.pivot_table(index=['ReynoldsNumber'], aggfunc='size').reset_index()
friction_count = friction_count.rename(columns={0:'count'})

#mean values
friction_mean = friction.groupby('ReynoldsNumber').mean().reset_index()
friction_mean = friction_mean.rename(columns={'FrictionFactor':'mean'})

#merged table
friction1 = friction.merge(friction_mean,'inner', 'ReynoldsNumber')
friction2 = friction1.merge(friction_count,'inner', 'ReynoldsNumber')

#statistical error
friction2['MeanDiff'] = friction2['FrictionFactor']-friction2['mean']
friction2['SquaredDevi'] = friction2['MeanDiff']**2
friction3 = pd.DataFrame()
friction3['SumOfSquaredDevi'] = friction2.groupby('ReynoldsNumber')['SquaredDevi'].sum('SquaredDevi')
friction4 = friction3.merge(friction_count,'inner','ReynoldsNumber')
friction4['std'] = (friction4['SumOfSquaredDevi']/friction4['count'])**(1/2)
friction4['error'] = friction4['std']/(friction4['count']**(1/2))
friction_error_rough = pd.DataFrame()
friction_error_rough['ReynoldsNumber'] = friction4['ReynoldsNumber']
friction_error_rough['Error'] = friction4['error']

#dataframes for graphing
friction_rough['Reynolds Number'] = friction_rough['Reynolds Number'].round(1)
friction_rough = friction_rough.dropna()
friction_rough = friction_rough.rename(columns={'Reynolds Number':'ReynoldsNumber'})
friction_rough1 = friction_rough1.dropna()
friction_error_rough = friction_rough.merge(friction_error_rough, 'inner', 'ReynoldsNumber')
friction_rough1 = friction_rough1.merge(friction_error_rough, 'inner', 'Friction Factor')


friction_error_rough = friction_rough1.drop(['Friction Factor', 'ReynoldsNumber'], axis=1)
friction_rough = friction_rough1.drop(['Error', 'ReynoldsNumber'], axis=1)
friction_rough1 = friction_rough1.drop(['Error', 'ReynoldsNumber'], axis=1).set_index('Reynolds Number')

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
# fig, ax = plt.subplots()
# ax.plot(friction_smooth1)
# ax.plot(friction_rough1)
# ax.plot(lam)
# ax.plot(tur)
# ax.set_xlabel('log Re')
# ax.set_ylabel('log f')
# #ax.legend(['64/Re', 'Blasius', 'Smooth', 'Rough'])
# ax.grid()
# plt.show()

#-----------------------------------------------------------------------------------------------Graph with Error Bars
fig, ax = plt.subplots()
ax.errorbar(friction_smooth['Reynolds Number'], friction_smooth['Friction Factor'], yerr = friction_error_rough['Error'])
ax.errorbar(friction_rough['Reynolds Number'], friction_rough['Friction Factor'], yerr = friction_error_rough['Error'])
ax.plot(lam)
ax.plot(tur)
ax.set_xlabel('log Re')
ax.set_ylabel('log f')
ax.legend(['64/Re', 'Blasius', 'Smooth', 'Rough'])
ax.grid()
plt.show()