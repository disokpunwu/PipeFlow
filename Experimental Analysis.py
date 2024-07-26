#Importing Functions
from Functions import *

#Define experiment
roughness = '2v'
experiment = 'Rescan88'


#Establsih Stages of Experiments
before = 'before'
actual = experiment
after = 'after'

#Retrieve Data from Experiment
actualpath = getExperimentPath(roughness, experiment, actual)
actualtdms = tdms_df(actualpath)
actualpressure = actualtdms['Validyne 6-32']

#Retrieve Data from Before Experiment
beforepath = getExperimentPath(roughness, experiment, before)
beforetdms = tdms_df(beforepath)
beforepressure = beforetdms['Validyne 6-32']

#Retrieve Data from After Experiment
afterpath = getExperimentPath(roughness, experiment, after)
aftertdms = tdms_df(afterpath)
afterpressure = aftertdms['Validyne 6-32']

#Reynolds Number
reynolds = reynolds_number(actualtdms)

#Analysis
print(f"Max Reynolds: {reynolds.max()}")
print(f"Min Reynolds: {reynolds.min()}")
print(f"Max Pressure: {actualpressure.max()}")
print(f"Min Pressure: {actualpressure.min()}")
print(f"Zero Shift Before: {beforepressure.mean()}")
print(f"Zero Shift After: {afterpressure.mean()}")
print(f"Zero Shift Difference: {abs(beforepressure.mean()-afterpressure.mean())}")
