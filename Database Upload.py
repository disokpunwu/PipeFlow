from Functions import *
import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine
from sqlalchemy import URL


experiment = '10p_experiment1'
path = r'C:\Users\PipeFlow\Desktop\Experiments\Old\Protrussion\10p\exp1\roughnessR_r=10P-exp1.tdms'
ldv1 = r'C:\Users\PipeFlow\Desktop\Experiments\Old\Protrussion\10p\exp1\roughnessR_r=10P-exp1-1D.SPEED.MSEBP.txt'
ldv2 = r'C:\Users\PipeFlow\Desktop\Experiments\Old\Protrussion\10p\exp1\roughnessR_r=10P-exp1-2D.SPEED.MSEBP.txt'

#formatting pressure data
pressure = tdms_df(path)
smooth_pressure = pressure_df_smooth(pressure)
rough_pressure = pressure_df_rough(pressure)

#formatting smooth laser data
laser1 = laser_df(ldv1)
laser1 = laser_snr_filter(laser1, 2.0)
laser1 = laser_df_for_graph(laser1)
smooth_laser = laser_interpolate(laser1)

#formatting rough laser data
laser2 = laser_df(ldv2)
laser2 = laser_snr_filter(laser2, 2.0)
laser2 = laser_df_for_graph(laser2)
rough_laser = laser_interpolate(laser2)


url_object = URL.create('mysql+mysqlconnector',
                        username = 'root',
                        password = '***REMOVED***',
                        host = '***REMOVED***',
                        database = experiment,)


my_eng = create_engine(url_object)
smooth_pressure.to_sql(name='smooth_pressure', con=my_eng, if_exists = 'replace', index=True)
rough_pressure.to_sql(name = 'rough_pressure', con=my_eng, if_exists='replace', index=True)
smooth_laser.to_sql(name='smooth_laser', con=my_eng, if_exists = 'replace', index=True)
rough_laser.to_sql(name='rough_laser', con=my_eng, if_exists = 'replace', index=True)