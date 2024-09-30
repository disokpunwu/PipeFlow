#Importing Functions
from Functions import *
from MainConfigurationFile import roughness, experiment


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
reynolds = reynolds['Reynolds Number'].squeeze().round(0)

#Analysis
print(f"The Reynolds Number range from {reynolds.min()}Re - {reynolds.max()}")
print(f"The pressure measurements range from {actualpressure.min().round(2)}mBar - {actualpressure.max().round(2)}mBar")
print(f"Zero shift before the experiment: {beforepressure.mean().round(3)}")
print(f"Zero shift after the experiment: {afterpressure.mean().round(3)}")
print(f"Difference in zero shift: {(abs(beforepressure.mean()-afterpressure.mean())).round(3)}")