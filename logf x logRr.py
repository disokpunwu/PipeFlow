from Functions import *


#-------------------------------------------------------------------------2v

#fetching file data
experiment = ''
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

#velocity
velSquared = ((reynolds['Reynolds Number']*dynamicViscosity)/(density*diameter))**2

#validyne8-22
Validyne822 = pressure[['Flow Rate Time', 'Validyne8-22']]
Validyne822['Flow Rate Time'] = Validyne822['Flow Rate Time'].round(2)
Validyne822 = Validyne822.set_index('Flow Rate Time')
Validyne822 = Validyne822.tail(20)

#friction factor
pipe = ((Validyne822['Validyne8-22']/2)*mbarToPa * 2 * diameter) / (velSquared * density * pressureSensorLength)
pipe = pipe.tail(-1)
pipe = pd.DataFrame(pipe, columns=['Friction Factor'])
pipe.dropna(inplace=True)

a = pipe['Friction Factor'].mean()
a = np.log10(a)

b = 2
b = np.log10(b)

#----------------------------------------------------------------------5p

#fetching file data
experiment = ''
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

#velocity
velSquared = ((reynolds['Reynolds Number']*dynamicViscosity)/(density*diameter))**2

#validyne8-22
Validyne632 = pressure[['Flow Rate Time', 'Validyne 6-32']]
Validyne632['Flow Rate Time'] = Validyne632['Flow Rate Time'].round(2)
Validyne632 = Validyne632.set_index('Flow Rate Time')
Validyne632 = Validyne632.tail(20)

#friction factor
pipe = ((Validyne632['Validyne 6-32']/2)*mbarToPa * 2 * diameter) / (velSquared * density * pressureSensorLength)
pipe = pipe.tail(-1)
pipe = pd.DataFrame(pipe, columns=['Friction Factor'])
pipe.dropna(inplace=True)

c = pipe['Friction Factor'].mean()
c = np.log10(c)

d = 5
d = np.log10(d)

#--------------------------------------------------------------------Graphs

plt.plot(b,a, 'ro')
plt.plot(d,c, 'bo')
plt.xlabel('log R/r')
plt.ylabel('log f')
plt.xlim(0,1)
plt.ylim(-3,0)
plt.legend(['2v', '5p'])
plt.grid() 
plt.show()