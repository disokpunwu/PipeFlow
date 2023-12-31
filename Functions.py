#importing libraries
from nptdms import TdmsFile
import numpy as np
import pandas as pd
import matplotlib
from matplotlib import pyplot as plt
import endaq
import math
from typing import Literal


#function to read TDMS files
def tdms_df(path):
    tdms_file = TdmsFile(path)
    tdms_data = tdms_file.as_dataframe()
    match len(tdms_data.columns):
        case 5:
            tdms_data.columns = ['Flow Rate', 'Flow Rate Time', 'Validyne 6-32', 'Validyne8-24', 'Pressure Time']
        case 7:
            tdms_data.columns = ['Motor Frequency', 'Motor Time', 'Flow Rate', 'Flow Rate Time', 'Pressure Time', 'Validyne 6-32', 'Validyne8-24']
        case _:
            raise RuntimeError("Unsupported number of columns read (expected 5 or 7)")
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

def pressure_df_smooth(tdms_df):
    smooth1 = tdms_df
    smooth1 = tdms_df[['Pressure Time', 'Validyne8-24']]
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

#standard deviation for rough pressure data
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
def reynolds_number(tdms):
    flowrate = tdms[['Flow Rate Time', 'Flow Rate']]
    flowrate['Flow Rate Time'] = flowrate['Flow Rate Time'].round(2)
    flowrate['Flow Rate Time'] = flowrate['Flow Rate Time'].drop_duplicates(keep='first')
    flowrate = flowrate.dropna()
    flowrate['Reynolds Number'] = (1004*(11*10**(-3))*flowrate['Flow Rate']/(60*1000)*1/((11*10**(-3)/2)**2*math.pi))/(0.9096*10**(-3))
    reynolds = flowrate[['Flow Rate Time', 'Reynolds Number']]
    reynolds = reynolds.set_index('Flow Rate Time')
    return reynolds

#laminar delta p graph
def re64(reynolds):
    reynolds['64/Re'] = 64/reynolds['Reynolds Number']
    reynolds['Laminar Delta P'] = reynolds['64/Re']*1/(11*10**(-3))*1004/2*(reynolds['Reynolds Number']/(1004*11*1e-3)*(0.9096*10**(-3)))**2/100
    Re64 = reynolds.drop('Reynolds Number', axis='columns')
    Re64 = Re64.drop('64/Re', axis='columns')
    return Re64

#turbulant delta p graph (smooth)
def blasius_smooth(reynolds):
    reynolds['Friction'] = .316/(reynolds['Reynolds Number']**.25)
    reynolds['Blasius'] = reynolds['Friction']*1/(11*10**(-3))*1004/2*(reynolds['Reynolds Number']/(1004*11*1e-3)*(0.9096*10**(-3)))**2/100
    blasius = reynolds['Blasius']
    return blasius

#turbulant delta p graph (rough)
def blasius_rough(reynolds):
     reynolds['Friction'] = (1/(-1.8*np.log10(((1/11)/3.7)**1.11+6.9/reynolds['Reynolds Number'])))**2
     reynolds['Blasius'] = reynolds['Friction']*1/(11*10**(-3))*1004/2*(reynolds['Reynolds Number']/(1004*11*1e-3)*(0.9096*10**(-3)))**2/100
     blasius = reynolds['Blasius']
     return blasius