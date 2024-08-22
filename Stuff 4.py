from Functions import *
flowrate = 12
diameter = 25 * (10**(-3))
crossSectionalArea = (math.pi * diameter**2)/4
density = 997 # kg/m^3 @ 25 degrees celsius
dynamicViscosity = 0.9096 * 10**-3
metresCubedPerSecond = flowrate * (0.1**3) / 60
velocity = metresCubedPerSecond / crossSectionalArea
reynolds = (density*diameter*velocity)/(dynamicViscosity)
print(reynolds)