#importing functions
from Functions import *


#creating paths for data to be uploaded
experiment = '10p_experiment1'
path = r'C:\Users\PipeFlow\Desktop\Experiments\Old\Protrussion\10p\exp1\roughnessR_r=10P-exp1.tdms'
ldv1 = r'C:\Users\PipeFlow\Desktop\Experiments\Old\Protrussion\10p\exp1\roughnessR_r=10P-exp1-1D.SPEED.MSEBP.txt'
ldv2 = r'C:\Users\PipeFlow\Desktop\Experiments\Old\Protrussion\10p\exp1\roughnessR_r=10P-exp1-2D.SPEED.MSEBP.txt'

#formatting pressure data
pressure = tdms_df(path)


#formatting smooth laser data
laser1 = laser_df(ldv1)
laser1 = laser_snr_filter(laser1, 2.0)
laser1 = laser_df_for_graph(laser1)
laser1 = laser_interpolate(laser1)


#formatting rough laser data
laser2 = laser_df(ldv2)
laser2 = laser_snr_filter(laser2, 2.0)
laser2 = laser_df_for_graph(laser2)
laser2 = laser_interpolate(laser2)

#creating a url to connect to mySQL
url_object = URL.create('mysql+mysqlconnector',
                        username = 'root',
                        password = '***REMOVED***',
                        host = '***REMOVED***',
                        database = experiment,)

#downloading data onto mySQL
my_eng = create_engine(url_object)
pressure.to_sql(name='pressure', con=my_eng, if_exists = 'replace', index=True)
laser1.to_sql(name='laser1', con=my_eng, if_exists = 'replace', index=True)
laser2.to_sql(name='laser2', con=my_eng, if_exists = 'replace', index=True)