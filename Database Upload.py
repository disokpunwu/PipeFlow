#importing functions
from Functions import *
import os

#creating paths for data to be uploaded
experiment = '8v_ReScan11'
path = r'C:\Users\PipeFlow\Desktop\Experiments\Data\New\Valley\8v\ReScan11\Rescan11.tdms'


#formatting pressure data
pressure = tdms_df(path)


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
pressure.to_sql(name='pressure', con=my_eng, if_exists = 'fail', index=True, chunksize=1000)
