#importing functions
from Functions import *
import os

#creating paths for data to be uploaded
experiment = ''
path = r''

#formatting pressure data
pressure = tdms_df(path)

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
reynolds = reynolds.rename(columns={'Reynolds Number': 'ReynoldsNumber'})

#constants
density = 1004 # kg/m^3
dynamicViscosity = 0.9096 * (10**-3)
diameter = 11 * (10**-3)
mbarToPa = 100
pressureSensorLength = 1

#validyne6-32
val632 = pressure[['Flow Rate Time', 'Validyne 6-32']]
val632['Flow Rate Time'] = val632['Flow Rate Time'].round(2)
val632 = val632.set_index('Flow Rate Time')

#velocity
velSquared = ((reynolds['ReynoldsNumber']*dynamicViscosity)/(density*diameter))**2

#friction factor for rough section
rough = (val632['Validyne 6-32']*mbarToPa * 2 * diameter) / (velSquared * density * pressureSensorLength)
rough = rough.tail(-1)
rough = pd.DataFrame(rough, columns=['FrictionFactor'])
rough['ReynoldsNumber'] = reynolds
rough = rough[['ReynoldsNumber', 'FrictionFactor']]
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
    avg = slicer['FrictionFactor'].mean()
    avg1 = slicer['ReynoldsNumber'].mean()
    fri.append(avg)
    re.append(avg1)
    FirstStep = FirstStep+1
    First = First+200
    Last = Last+200
fri = np.array(fri)
re = np.array(re)
d = {'ReynoldsNumber': re, 'FrictionFactor':fri}
friction = pd.DataFrame(d)
friction = np.log10(friction)
friction = friction.set_index('FrictionFactor')
friction = friction.round(1)
friction = friction.reset_index()
friction = friction.set_index('ReynoldsNumber')
friction = friction.dropna()

#allow for large packets to be uploaded to mySQL
#Execute the sql on the mysql server: set global max_allowed_packet=10000000000;

username = os.getenv("PIPEFLOW_DATABASE_USERNAME")
password = os.getenv("PIPEFLOW_DATABASE_PASSWORD")
host = os.getenv("PIPEFLOW_DATABASE_HOST")

#creating a url to connect to mySQL
url_object = URL.create('mysql+mysqlconnector',
                        username = username,
                        password = password,
                        host = host,
                        database = experiment,)

#creating the database in mySQL
mydb = mysql.connector.connect(
  host=host,
  user=username,
  password=password
)
mycursor = mydb.cursor()
mycursor.execute("CREATE SCHEMA "+ experiment)

#downloading data onto mySQL
my_eng = create_engine(url_object)
friction.to_sql(name='friction', con=my_eng, if_exists = 'fail', index=True, chunksize=1000)