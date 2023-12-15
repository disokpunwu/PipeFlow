#importing functions
from Functions import *


#creating paths for data to be uploaded
experiment = ''
path = r''
ldv1 = r''
ldv2 = r''

#formatting pressure data
pressure = tdms_df(path)

#formatting smooth laser data
laser1 = laser_df(ldv1)

#formatting rough laser data
laser2 = laser_df(ldv2)

#allow for large packets to be uploaded to mySQL
#Execute the sql on the mysql server: set global max_allowed_packet=10000000000;

#creating a url to connect to mySQL
url_object = URL.create('mysql+mysqlconnector',
                        username = 'root',
                        password = '***REMOVED***',
                        host = '***REMOVED***',
                        database = experiment,)

#creating the database in mySQL
mydb = mysql.connector.connect(
  host="***REMOVED***",
  user="root",
  password="***REMOVED***"
)
mycursor = mydb.cursor()
mycursor.execute("CREATE SCHEMA "+ experiment)

#downloading data onto mySQL
my_eng = create_engine(url_object)
pressure.to_sql(name='pressure', con=my_eng, if_exists = 'fail', index=True, chunksize=1000)
laser1.to_sql(name='laser1', con=my_eng, if_exists = 'fail', index=True, chunksize=1000)
laser2.to_sql(name='laser2', con=my_eng, if_exists = 'fail', index=True, chunksize=1000)