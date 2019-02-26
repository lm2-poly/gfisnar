#-*- coding: utf-8 -*-
#@author: aziz-yamar.gueye@polyml.ca



from gfishnar import *

#------------------------------READ--------------------------------------------
yaml = YAML("input.yaml")
Gcode = Gcode()
gcode=Gcode.read(yaml.gcodepath)
#-----------------------------EXTRACT------------------------------------------
extract=extract(gcode)
#-----------------------------REVERSE TOOLPATH----------------------------------
reverse= Reverse(extract.deck,yaml.deck)
#-----------------------------CALIBRATE----------------------------------------
calibrate=Calibrate(reverse.deck,yaml.deck)
#-----------------------------WRITE--------------------------------------------
writer=write(reverse.deck,calibrate.coord)
print 'Output file(s) is now available in the current directory'
print 'Import it into Excel, then copy-paste the content in the Fisnar software'
#-----------------------------REWRITE GCODE----------------------------------
GCODErewriter = GCODErewriter(yaml.gcodepath,reverse.new_points,reverse.new_E)
print 'Output Gcode file is now available in the current directory'


import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


fig = plt.figure()
ax1 = fig.add_subplot(111,projection='3d')

x = [point[0] for point in calibrate.coord]
y = [point[1] for point in calibrate.coord]
z = [point[2] for point in calibrate.coord]


ax1.plot3D(x,y,z)
plt.show()
