#importing libraries
from nptdms import TdmsFile
import numpy as np
import pandas as pd
import matplotlib
from matplotlib import pyplot as plt
import endaq
import math
from typing import Literal
import mysql.connector
from mysql.connector import Error
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import URL
import seaborn as sns
import os
import re
from stat import S_ISDIR, S_ISREG

username = os.getenv("PIPEFLOW_DATABASE_USERNAME")
password = os.getenv("PIPEFLOW_DATABASE_PASSWORD")
host = os.getenv("PIPEFLOW_DATABASE_HOST")

def create_sql_engine(experiment):
    url_object = URL.create('mysql+mysqlconnector',
                        username = username,
                        password = password,
                        host = host,
                        database = experiment,)
    my_eng = create_engine(url_object)
    return my_eng

def read_table(sql_engine, table_name):
    dataframe = pd.read_sql_table(table_name, sql_engine)
    #dataframe = dataframe.set_index('index')
    return dataframe

def read_tables(experiment, table_names):
    sql_engine = create_sql_engine(experiment)
    # List comprehension calling the function
    # once for each element of the table_names list
    return [read_table(sql_engine, name) for name in table_names]

#function to read TDMS files
def tdms_df(path):
    tdms_file = TdmsFile(path)
    tdms_data = tdms_file.as_dataframe()
    match len(tdms_data.columns):
        case 5:
            tdms_data.rename(columns= {"/'Flow Rate'/'Flow Rate'" : 'Flow Rate', "/'Flow Rate'/'Time'": 'Flow Rate Time', "/'Pressure'/'Validyne 6-32'": 'Validyne 6-32', "/'Pressure'/'Validyne 8-24'": 'Validyne8-24', "/'Pressure'/'Time'":'Pressure Time'}, inplace = True)
        case 6:
            tdms_data.rename(columns= {"/'Motor'/'Motor Frequency'" : 'Motor Frequency', "/'Motor'/'Time'":'Motor Time', "/'Flow Rate'/'Flow Rate'":'Flow Rate', "/'Flow Rate'/'Time'":'Flow Rate Time', "/'Pressure'/'Time'":'Pressure Time', "/'Pressure'/'Validyne 6-32'":'Validyne 6-32'}, inplace=True)
        case 7:
            tdms_data.rename(columns= {"/'Motor'/'Motor Frequency'" : 'Motor Frequency', "/'Motor'/'Time'":'Motor Time', "/'Flow Rate'/'Flow Rate'":'Flow Rate', "/'Flow Rate'/'Time'":'Flow Rate Time', "/'Pressure'/'Time'":'Pressure Time', "/'Pressure'/'Validyne 6-32'":'Validyne 6-32', "/'Pressure'/'Validyne 8-24'":'Validyne8-24'},inplace=True)
        case 8:
            tdms_data.rename(columns= {"/'Motor'/'Motor Frequency'" : 'Motor Frequency', "/'Motor'/'Time'":'Motor Time', "/'Flow Rate'/'Flow Rate'":'Flow Rate', "/'Flow Rate'/'Time'":'Flow Rate Time', "/'Pressure'/'Time'":'Pressure Time', "/'Pressure'/'Validyne 6-32'":'Validyne 6-32', "/'Pressure'/'Validyne 8-22'":'Validyne8-22', "/'Pressure'/'Validyne 8-24'":'Validyne8-24'},inplace=True)
        case _:
            raise RuntimeError("Unsupported number of columns read (expected 5 6, or 7)")
    return tdms_data

#format all pressure data for graphing
def pressure_df(tdms_df):
    pressure1 = tdms_df
    pressure1 = tdms_df[['Pressure Time', 'Validyne8-24', 'Validyne 6-32']]
    pressure = pressure1.set_index('Pressure Time')
    return pressure

#format pressure data in the smooth section
def pressure_df_2(tdms_df, region: Literal["rough", "smooth"]):
    match region:
        case "rough":
            isRough = True
        case "smooth":
            isRough = False
        case _:
            raise ValueError("Invalid argument, expected 'smooth' or 'rough'")
    frame_subset = tdms_df[['Pressure Time', getPressureColumnName(isRough)]]
    return frame_subset.set_index('Pressure Time')

#format all pressure data for graphing
def pressure_df3(tdms_df):
    pressure1 = tdms_df
    pressure1 = tdms_df[['Flow Rate Time', 'Validyne8-24', 'Validyne 6-32']]
    pressure = pressure1.set_index('Flow Rate Time')
    return pressure

def pressure_df_smooth(tdms_df):
    smooth1 = tdms_df
    smooth1 = tdms_df[['Pressure Time', 'Validyne8-24']]
    smooth1['Validyne8-24'] = smooth1['Validyne8-24']/2
    smooth = smooth1.set_index('Pressure Time')
    return smooth

#format pressure data in the rough section
def pressure_df_rough(tdms_df):
    rough1 = tdms_df
    rough1 = tdms_df[['Pressure Time', 'Validyne 6-32']]
    rough = rough1.set_index('Pressure Time')
    return rough

#function to slice pressure data
def pressure_slice_df(formatted_data, Start, End):
    sliceddata = formatted_data
    sliceddata = sliceddata.reset_index()
    a = sliceddata['Pressure Time'] > (Start-.1)
    b = sliceddata.where(a)
    c = b.dropna()
    d = c['Pressure Time'] < (End+.1)
    e = c.where(d)
    sliceddata = e.dropna()
    sliceddata = sliceddata.set_index('Pressure Time')
    return sliceddata    

#function for power spectrum with rough pressure data
def rough_pressure_psd(sliced_data, Start, End):
    roughpressure1psd = sliced_data
    roughpressure1psd = endaq.calc.psd.welch(sliced_data, bin_width=.0001)
    roughpressure1psd.reindex()
    roughpressure1var = sliced_data['Validyne 6-32'].var()
    roughpressure1psd['Amplitude'] = (roughpressure1psd['Validyne 6-32']/roughpressure1var)/(End-Start)
    roughpressurepsd = roughpressure1psd.drop('Validyne 6-32', axis= 'columns')
    return roughpressurepsd

#function for power spectrum with smooth pressure data
def smooth_pressure_psd(sliced_data, Start, End):
    smoothpressure1psd = sliced_data
    smoothpressure1psd = endaq.calc.psd.welch(sliced_data, bin_width=.001)
    smoothpressure1psd.reindex()
    smoothpressure1var = sliced_data['Validyne8-24'].var()
    smoothpressure1psd['Amplitude'] = (smoothpressure1psd['Validyne8-24']/smoothpressure1var)/(End-Start)
    smoothpressurepsd = smoothpressure1psd.drop('Validyne8-24', axis= 'columns')
    return smoothpressurepsd

#standard deviation for smooth pressure data
def smooth_pressure_std(smooth):
    r2 = smooth.reset_index()
    steps = 10
    slices = 50
    begin = r2['Pressure Time'].min()
    start = begin
    end1 = r2['Pressure Time'].max()
    end = round(end1/steps)*steps
    itter = (end-begin)/steps
    itter = itter.astype('int')
    sdev = []
    while begin < end:
        slicer = pressure_slice_df(smooth, begin, begin+slices)
        stand = slicer['Validyne8-24'].std()
        sdev.append(stand)
        begin = begin+steps
    time = np.linspace(start, end, itter)
    d = {'Pressure Time':time, 'Standard Deviation':sdev}
    sdeviation = pd.DataFrame(d)
    #sdeviation['Standard Deviation'] =   (sdeviation['Standard Deviation']-  sdeviation['Standard Deviation'].min())/(sdeviation['Standard Deviation'].max()-sdeviation['Standard Deviation'].min())
    sdeviation['Standard Deviation'] =   (sdeviation['Standard Deviation']-  sdeviation['Standard Deviation'].mean())/  sdeviation['Standard Deviation'].std()
    sdeviation = sdeviation.set_index('Pressure Time')
    return sdeviation

#standard deviation for rough pressure data
def rough_pressure_std(rough):
    r2 = rough.reset_index()
    steps = 10
    slices = 50
    begin = r2['Pressure Time'].min()
    start = begin
    end1 = r2['Pressure Time'].max()
    end = round(end1/steps)*steps
    itter = (end-begin)/steps
    itter = itter.astype('int')
    sdev = []
    while begin < end:
        slicer = pressure_slice_df(rough, begin, begin+slices)
        stand = slicer['Validyne 6-32'].std()
        sdev.append(stand)
        begin = begin+steps
    time = np.linspace(start, end, itter)
    d = {'Pressure Time':time, 'Standard Deviation':sdev}
    sdeviation = pd.DataFrame(d)
    #sdeviation['Standard Deviation'] =   (sdeviation['Standard Deviation']-  sdeviation['Standard Deviation'].min())/(sdeviation['Standard Deviation'].max()-sdeviation['Standard Deviation'].min())
    sdeviation['Standard Deviation'] =   (sdeviation['Standard Deviation']-  sdeviation['Standard Deviation'].mean())/  sdeviation['Standard Deviation'].std()
    sdeviation = sdeviation.set_index('Pressure Time')
    return sdeviation

#standard deviation for reynolds number
def reynolds_std(reynolds):
    r2 = reynolds.reset_index()
    steps = 10
    slices = 50
    begin = r2['Pressure Time'].min()
    start = begin
    end1 = r2['Pressure Time'].max()
    end = round(end1/steps)*steps
    itter = (end-begin)/steps
    itter = itter.astype('int')
    sdev = []
    while begin < end:
        slicer = pressure_slice_df(reynolds, begin, begin+slices)
        stand = slicer['Reynolds Number'].std()
        sdev.append(stand)
        begin = begin+steps
    time = np.linspace(start, end, itter)
    sdev.pop()
    d = {'Pressure Time':time, 'Standard Deviation':sdev}
    sdeviation = pd.DataFrame(d)
    #sdeviation['Standard Deviation'] =   (sdeviation['Standard Deviation']-  sdeviation['Standard Deviation'].min())/(sdeviation['Standard Deviation'].max()-sdeviation['Standard Deviation'].min())
    sdeviation['Standard Deviation'] =   (sdeviation['Standard Deviation']-  sdeviation['Standard Deviation'].mean())/  sdeviation['Standard Deviation'].std()
    sdeviation = sdeviation.set_index('Pressure Time')
    return sdeviation

#percent difference
def reynolds_pdiff(reynolds):
    r2 = reynolds.reset_index()
    steps = 10
    slices = 50
    begin = r2['Pressure Time'].min()
    start = begin
    end1 = r2['Pressure Time'].max()
    end = round(end1/steps)*steps
    itter = (end-begin)/steps
    itter = itter.astype('int')
    rmean = []
    rmax = []
    rmin = []
    while begin < end:
        slicer = pressure_slice_df(reynolds, begin, begin+slices)
        reymean = slicer['Reynolds Number'].mean()
        reymax = slicer['Reynolds Number'].max()
        reymin = slicer['Reynolds Number'].min()
        rmean.append(reymean)
        rmax.append(reymax)
        rmin.append(reymin)
        begin = begin+steps
    time = np.linspace(start, end, itter)
    if np.count_nonzero(rmean) != np.count_nonzero(time):
        rmean.pop()
    else:
        pass
    if np.count_nonzero(rmax) != np.count_nonzero(time):
        rmax.pop()
    else:
        pass    
    if np.count_nonzero(rmin) != np.count_nonzero(time):
        rmin.pop()
    else:
        pass 
    # rmean.pop()
    # rmax.pop()
    # rmin.pop()
    d = {'Pressure Time':time, 'Reynolds Mean':rmean, 'Reynolds Max':rmax, 'Reynolds Min':rmin}
    pdifference = pd.DataFrame(d)
    pdifference['Percent Difference'] =   (((pdifference['Reynolds Max']-  pdifference['Reynolds Min'].mean())/  pdifference['Reynolds Mean'])*100).round(2)
    pdifference = pdifference.set_index('Pressure Time')
    return pdifference

#function to slice pressure data
def reynolds_slice(data, Start, End):
    sliceddata = data
    a = sliceddata['Reynolds Number'] > (Start-.1)
    b = sliceddata.where(a)
    c = b.dropna()
    d = c['Reynolds Number'] < (End+.1)
    e = c.where(d)
    sliceddata = e.dropna()
    return sliceddata  

def getPressureColumnName(isRough):
    return "Validyne 6-32" if isRough else "Validyne8-24"

#fuction to determine pressure drop percentage
def pressure_drop(reservoir, entry, exit):
    res = reservoir-79
    ent = 51.2-res
    before = ((entry-ent)/1.02)/(108.6+res)*100
    before = round(before)
    bef = 'pressure drop before entrance is'
    pipe = ((exit - entry)/1.02)/(108.6+res)*100
    pipe = round(pipe)
    pip = 'pressure drop in the pipe is'
    after = ((159.8-exit)/1.02)/(108.6+res)*100
    after = round(after)
    aft = 'pressure drop after the pipe is'

    return bef, before, pip, pipe, aft, after

#function to determine total pressure drop
def tot_pressure_drop(reservoir):
    res = reservoir-79
    ent = 51.2-res
    ext = (159.8-ent)/1.02
    return ext


#function to calculate 2x mean speed
def x2speed_df(pressure):
    x2speed = pressure[['Flow Rate Time', 'Flow Rate']]
    x2speed = x2speed.set_index('Flow Rate Time')
    x2speed = (x2speed['Flow Rate']/60000)/(math.pi*(.0055*.0055))*2
    x2speed = x2speed.rolling(10).mean()
    return x2speed

#function to slice 2x speed data
def x2speed_slice_df(formatted_data, Start, End):
    sliceddata = formatted_data
    sliceddata = sliceddata.reset_index()
    a = sliceddata['Flow Rate Time'] > (Start-.1)
    b = sliceddata.where(a)
    c = b.dropna()
    d = c['Flow Rate Time'] < (End+.1)
    e = c.where(d)
    sliceddata = e.dropna()
    sliceddata = sliceddata.set_index('Flow Rate Time')
    return sliceddata 






#function to read laser files
def laser_df(path):
    laser_data = pd.read_csv(path, delimiter='\t')
    laser_data.columns = ['Device Time (msec)', 'Device Time (usec)', 'Speed (m/sec)', 'SNR']
    return laser_data

def laser_snr_filter(laserdata, snr):
    a = laserdata['SNR'] > snr
    b = laserdata.where(a)
    c = b.dropna()
    return c

#function to format laser data for graphing
def laser_df_for_graph(laser_df):
    laserdata = laser_df
    laserdata ['Device Time (msec)'] = laserdata['Device Time (msec)']*.001
    laserdata ['Device Time (usec)'] = laserdata['Device Time (usec)']*.000001
    laserdata ['Device Time'] = laserdata['Device Time (msec)']+laserdata['Device Time (usec)']
    laserdata = laserdata[['Device Time', 'Speed (m/sec)']]
    laserdata = laserdata.set_index('Device Time')
    return laserdata

#function to interpolate data
def laser_interpolate(dataframe):
    laser = dataframe
    laser = laser.reset_index()
    laser['Device Time'] = laser['Device Time'].round(1)
    laser['Device Time'] = laser['Device Time'].drop_duplicates(keep='first')
    laser = laser.dropna()
    maxVal = laser['Device Time'].max()
    laser2 = pd.DataFrame()
    uni = np.linspace(0.0,maxVal,int(maxVal*10))
    uni = uni.round(1)
    laser2['Device Time'] = uni
    laser3 = laser2.merge(laser, on='Device Time', how='left')
    laser4 = laser3.drop('Device Time', axis='columns')
    laser5 = laser4.interpolate(method='linear')
    laser5['Device Time'] = laser3['Device Time']
    laser5 = laser5.set_index('Device Time')
    return laser5

#function to slice the dataframe for time windows
def laser_slice_df(formatted_data, Start, End):
    sliceddata = formatted_data
    sliceddata = sliceddata.reset_index()
    a = sliceddata['Device Time'] > (Start-.1)
    b = sliceddata.where(a)
    c = b.dropna()
    d = c['Device Time'] < (End+.1)
    e = c.where(d)
    sliceddata = e.dropna()
    sliceddata = sliceddata.set_index('Device Time')
    return sliceddata
    
#function for power spectrum with laser data
def laser_psd(sliced_data, Start, End):
    sliced_data1 = sliced_data
    laser1psd = sliced_data
    laser1psd = endaq.calc.psd.welch(sliced_data, bin_width=.001)
    laser1psd.reindex()
    laser1var = sliced_data1['Speed (m/sec)'].var()
    laser1psd['Amplitude'] = (laser1psd['Speed (m/sec)']/laser1var)/(End-Start)
    laserpsd = laser1psd.drop('Speed (m/sec)', axis= 'columns')
    return laserpsd

#standard deviation for laser data
def laser_std(interpolate):
    l2 = interpolate.reset_index()
    steps = 10
    slices = 50
    begin = l2['Device Time'].min()
    start = begin-.1
    end1 = l2['Device Time'].max()
    end = round(end1/steps)*steps
    itter = (end-start)/steps
    itter = itter.astype('int')
    sdev = []
    while begin < end:
        slicer = laser_slice_df(interpolate, begin, begin+slices)
        stand = slicer['Speed (m/sec)'].std()
        sdev.append(stand)
        begin = begin+steps
    time = np.linspace(start, end, itter)
    d = {'Device Time':time, 'Standard Deviation':sdev}
    sdeviation = pd.DataFrame(d)
    sdeviation['Standard Deviation'] =   (sdeviation['Standard Deviation']-  sdeviation['Standard Deviation'].min())/(sdeviation['Standard Deviation'].max()-sdeviation['Standard Deviation'].min())
    #sdeviation['Standard Deviation'] =   (sdeviation['Standard Deviation']-  sdeviation['Standard Deviation'].mean())/  sdeviation['Standard Deviation'].std()
    sdeviation = sdeviation.set_index('Device Time')
    return sdeviation











#reynolds number graph
def reynolds_number(flowrateDataFrame):
    flowrate = flowrateDataFrame[['Flow Rate Time', 'Flow Rate']]
    flowrate.loc[:, 'Flow Rate Time'] = flowrate['Flow Rate Time'].round(2).drop_duplicates(keep='first')
    # flowrate['Flow Rate Time'] = flowrate['Flow Rate Time'].drop_duplicates(keep='first')
    flowrate = flowrate.dropna()
    diameter = 11 * (10**(-3))
    crossSectionalArea = (math.pi * diameter**2)/4

    density = 997 # kg/m^3 @ 25 degrees celsius
    dynamicViscosity = 0.9096 * 10**-3
    # flowrate['Flow Rate'] is l/min = 10cm^3 / minute = 0.1m^3 / min
    metresCubedPerSecond = flowrate['Flow Rate'] * (0.1**3) / 60
    velocity = metresCubedPerSecond / crossSectionalArea
    flowrate['Reynolds Number'] = (density*diameter*velocity)/(dynamicViscosity)
    reynolds = flowrate[['Flow Rate Time', 'Reynolds Number']]
    reynolds = reynolds.set_index('Flow Rate Time')
    return reynolds

#laminar delta p graph
def re64(reynolds):
    Re = reynolds['Reynolds Number']
    diameter = 11*10**(-3)
    density = 1004
    dv = 0.9096*10**(-3)
    kinematic_viscosity = 0.8926e-6  # 流体の動粘性係数 (m^2/s)
    reynolds['64/Re'] = 64/Re
    reynolds['Laminar Delta P'] = (64*Re) * dv * kinematic_viscosity / (200*pow(diameter,3))
    Re64 = reynolds.drop('Reynolds Number', axis='columns')
    Re64 = Re64.drop('64/Re', axis='columns')
    return Re64

#laminar delta p graph
def re65(reynolds):
    reynolds['64/Re'] = 64/reynolds['Reynolds Number']
    #reynolds['Laminar Delta P'] = (reynolds['64/Re'])*(1004/2)*(((((reynolds['Reynolds Number'])*(0.9096*10**(-3)))/1004)**2)/(11*1e-3))*100
    reynolds['Laminar Delta P'] = (reynolds['64/Re'])*(1004/2)*((reynolds['Reynolds Number']/(1004*11*1e-3)*(0.9096*10**(-3)))**2)/(11*10**(-3))/100
    Re64 = reynolds.drop('Reynolds Number', axis='columns')
    Re64 = Re64.drop('64/Re', axis='columns')
    return Re64

#turbulant delta p graph (smooth)
def blasius_smooth(reynolds):
    reynolds['Friction'] = .316/(reynolds['Reynolds Number']**.25)
    reynolds['Blasius'] = (reynolds['Friction'])*(1004/2)*((reynolds['Reynolds Number']/(1004*11*1e-3)*(0.9096*10**(-3)))**2)/(11*10**(-3))/100
    #reynolds['Blasius'] = reynolds['Friction']/(11*10**(-3))*1004/2*(reynolds['Reynolds Number']/(1004*11*1e-3)*(0.9096*10**(-3)))**2/100
    blasius = reynolds['Blasius']
    return blasius

#turbulant delta p graph (rough)
def blasius_rough(reynolds):
     reynolds['Friction'] = (1/(-1.8*np.log10(((1/11)/3.7)**1.11+6.9/reynolds['Reynolds Number'])))**2
     reynolds['Blasius'] = reynolds['Friction']*1/(11*10**(-3))*1004/2*(reynolds['Reynolds Number']/(1004*11*1e-3)*(0.9096*10**(-3)))**2/100
     blasius = reynolds['Blasius']
     return blasius

#turbulant delta p graph (rough)
def haaland_rough(reynolds):
     reynolds['Friction'] = (1/(-1.8*np.log10(((3.667/.11)/3.7)**1.11+6.9/reynolds['Reynolds Number'])))**2
     reynolds['Haaland'] = (reynolds['Friction'])*(1004/2)*((reynolds['Reynolds Number']/(1004*11*1e-3)*(0.9096*10**(-3)))**2)/(11*10**(-3))/100
     haaland = reynolds['Haaland']
     return haaland

#Shortcut for retrieving the path of experiment roughnesses
def getRoughnessPath(roughness):
    
    rootPath = r'C:\Users\PipeFlow\Desktop\Experiments'
    roughnessPath = os.path.join(rootPath, 'Data', 'New', 'Valley', roughness)
    if S_ISDIR(os.stat(roughnessPath).st_mode):
        return roughnessPath
    else:
        raise RuntimeError("Did not file a directory at " + roughnessPath)

#Shortcut for retrieving the path of specific experiments
def getExperimentPath(roughness, experiment, stage):
    expectedPath = os.path.join(getRoughnessPath(roughness), experiment, f"{stage}.tdms")
    if S_ISREG(os.stat(expectedPath).st_mode):
        return expectedPath
    else:
        raise RuntimeError("Did not file a regular file at " + expectedPath)

#Allows for the uploading of experiments to the database
def DataBaseUpload(experiment, path):
    pressure = tdms_df(path)
    username = os.getenv("PIPEFLOW_DATABASE_USERNAME")
    password = os.getenv("PIPEFLOW_DATABASE_PASSWORD")
    host = os.getenv("PIPEFLOW_DATABASE_HOST")
    url_object = URL.create('mysql+mysqlconnector',
                            username = username,
                            password = password,
                            host = host,
                            database = experiment,)
    mydb = mysql.connector.connect(
     host=host,
      user=username,
     password=password
    )
    mycursor = mydb.cursor()
    mycursor.execute("CREATE SCHEMA "+ experiment)
    my_eng = create_engine(url_object)
    pressure.to_sql(name='pressure', con=my_eng, if_exists = 'fail', index=True, chunksize=1000)


#rounds the number up
def round_up(value, to_next):
    return int(math.ceil(value / to_next)) * to_next

#creates nukuradse diagram from pressure data
def process_experiment(experiment, zeroshift = .00000001, start= 150, stop = 200, step = 200, pressureSensorLength = 1, diameter = 11 * (10**-3)):
    #fetching file data
    engine = create_sql_engine(experiment)
    (pressure) = read_table(engine, 'pressure')
    fileDuration = round_up(pressure['Flow Rate Time'].max(), 100)
    #Timestamp for Steps
    StartTimes = np.arange(start,fileDuration,step)
    EndTimes = np.arange(stop,fileDuration+step,step)
    numSteps = StartTimes.size
    #reynolds number
    reynolds = reynolds_number(pressure)
    #constants
    density = 1004 # kg/m^3
    dynamicViscosity = 0.9096 * (10**-3)
    mbarToPa = 100
    #velocity
    velSquared = ((reynolds['Reynolds Number']*dynamicViscosity)/(density*diameter))**2
    #---------------------------------------------------Rough Section
    #validyne6-32
    val632 = pressure[['Flow Rate Time', 'Validyne 6-32']]
    val632.loc[:, 'Flow Rate Time'] = val632['Flow Rate Time'].round(2)
    val632 = val632.set_index('Flow Rate Time')
    val632['Validyne 6-32'] = val632['Validyne 6-32']-zeroshift 
    #friction factor for rough section
    rough = (val632['Validyne 6-32']*mbarToPa * 2 * diameter) / (velSquared * density * pressureSensorLength)
    rough = pd.DataFrame(rough, columns=['Friction Factor'])
    rough['Reynolds Number'] = reynolds
    rough = rough[['Reynolds Number', 'Friction Factor']]
    rough.dropna(inplace=True)
    #averaging pressure data
    fri = []
    re = []
    currentIndex = 0
    while currentIndex < numSteps:
        First = StartTimes[currentIndex]
        Last = EndTimes[currentIndex]
        x = slice(First,Last)
        slicer = rough.loc[x, :] # All columns, rows between First and Last
        avg = slicer['Friction Factor'].mean()
        avg1 = slicer['Reynolds Number'].mean()
        fri.append(avg)
        re.append(avg1)
        currentIndex += 1
    fri = np.array(fri)
    re = np.array(re)
    d = {'Reynolds Number': re, 'Friction Factor':fri}
    rough_friction = pd.DataFrame(d)
    rough_friction = np.log10(rough_friction)
    rough_friction = rough_friction.set_index('Reynolds Number')
    #---------------------------------------------------Smooth Section
    #validyne8-24
    val824 = pressure[['Flow Rate Time', 'Validyne8-24']]
    val824.loc[:, 'Flow Rate Time'] = val824['Flow Rate Time'].round(2)
    val824.loc[:, 'Validyne8-24'] = val824['Validyne8-24']/2
    val824 = val824.set_index('Flow Rate Time')
    #friction factor
    smooth = (val824['Validyne8-24']*mbarToPa * 2 * diameter) / (velSquared * density * pressureSensorLength)
    smooth = smooth.tail(-1)
    smooth = pd.DataFrame(smooth, columns=['Friction Factor'])
    smooth['Reynolds Number'] = reynolds
    smooth = smooth[['Reynolds Number', 'Friction Factor']]
    smooth.dropna(inplace=True)
    #averaging pressure data
    fri = []
    re = []
    currentIndex = 0
    while currentIndex < numSteps:
        First = StartTimes[currentIndex]
        Last = EndTimes[currentIndex]
        x = slice(First,Last)
        slicer = smooth.loc[x, :] # all columns, times between First and Last
        avg = slicer['Friction Factor'].mean()
        avg1 = slicer['Reynolds Number'].mean()
        fri.append(avg)
        re.append(avg1)
        currentIndex = currentIndex+1
    fri = np.array(fri)
    re = np.array(re)
    d = {'Reynolds Number': re, 'Friction Factor':fri}
    smooth_friction = pd.DataFrame(d)
    smooth_friction = np.log10(smooth_friction)
    smooth_friction = smooth_friction.set_index('Reynolds Number')

    result = dict()
    result['smooth'] = smooth_friction
    result['rough'] = rough_friction
    return result

#creates nikuradse diagram with zeroshift incorporated
def Process_ZeroShift_Experiment(roughness, itteration):
    # locating file data
    location = r"C:\Users\PipeFlow\Desktop\Experiments\Data\New\Valley"
    experiment = (f"{roughness}_{itteration}")
    beforepath = (f"{location}\{roughness}\{itteration}\{'before'}.tdms")
    path = (f"{location}\{roughness}\{itteration}\{itteration}.tdms")
    afterpath = (f"{location}\{roughness}\{itteration}\{'after'}.tdms")
    # calculating mean zero-shift before and after experiment
    before = tdms_df(beforepath)
    before = before['Validyne 6-32'].mean()
    after = tdms_df(afterpath)
    after = after['Validyne 6-32'].mean()
    #applying the zeroshift to the data
    beforezeroshift = process_experiment(experiment, zeroshift= before)
    beforezeroshift = beforezeroshift['rough']
    nozeroshift = process_experiment(experiment)
    nozeroshift = nozeroshift['rough']
    afterzeroshift = process_experiment(experiment, zeroshift= after)
    afterzeroshift = afterzeroshift['rough']
    result = dict()
    result['before'] = beforezeroshift
    result['actual'] = nozeroshift
    result['after'] = afterzeroshift
    return result

# #creates nikuradse diagram from excel measurements
# def Process_Excel_Experiemnt(roughness, experiment):
#     path = r"C:\Users\PipeFlow\Desktop\Experiments\Data\New\Valley"
#     ExcelPath = os.path.join(path, roughness, experiment, experiment)
#     FinalPath = (f"{ExcelPath}.xlsx")
#     data = pd.read_excel(FinalPath)
#     #constants
#     pressureSensorLength = 1 
#     diameter = 11 * (10**-3)
#     density = 1004 # kg/m^3
#     dynamicViscosity = 0.9096 * (10**-3)
#     mbarToPa = 100
#     velSquared = ((data['Reynolds Number']*dynamicViscosity)/(density*diameter))**2
#     data['Friction'] = (data['Pressure']*mbarToPa * 2 * diameter) / (velSquared * density * pressureSensorLength)
#     data = data[['Reynolds Number', 'Friction']]
#     data = np.log10(data)
#     data.set_index('Reynolds Number', inplace=True)
#     return data

#creates nikuradse diagram from excel measurements
def Process_Excel_Experiemnt(roughness, experiment):
    path = r"C:\Users\PipeFlow\Desktop\Experiments\Data\New\Valley"
    ExcelPath = os.path.join(path, roughness, experiment, experiment)
    FinalPath = (f"{ExcelPath}.xlsx")
    pressure = pd.read_excel(FinalPath)
    sqldata = process_experiment(f"{roughness}_{experiment}")
    rough = sqldata['rough'].reset_index()
    data = pd.DataFrame()
    data['Reynolds Number'] = 10**(rough['Reynolds Number'])
    data['Pressure'] = pressure['Pressure']/1.02

    #constants
    pressureSensorLength = 1 
    diameter = 11 * (10**-3)
    density = 1004 # kg/m^3
    dynamicViscosity = 0.9096 * (10**-3)
    mbarToPa = 100
    velSquared = ((data['Reynolds Number']*dynamicViscosity)/(density*diameter))**2
    data['Friction'] = (data['Pressure']*mbarToPa * 2 * diameter) / (velSquared * density * pressureSensorLength)
    data = data[['Reynolds Number', 'Friction']]
    data = np.log10(data)
    data.set_index('Reynolds Number', inplace=True)
    return data