#Importing Functions
from Functions import *

#Experiment Description
roughness = '2v'
itteration = 'rescan88'

#Uploading Experiments to Database
experiment = (f"{roughness}_{itteration}")
path = getExperimentPath(roughness, itteration, itteration)
DataBaseUpload(experiment, path)
