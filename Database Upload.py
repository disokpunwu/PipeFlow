#Importing Functions
from Functions import *

#Experiment Description
roughness = '4v'
itteration = 'rescan21'

#Uploading Experiments to Database
experiment = (f"{roughness}_{itteration}")
path = getExperimentPath(roughness, itteration, itteration)
DataBaseUpload(experiment, path)