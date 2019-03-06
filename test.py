#-*- coding: utf-8 -*-
#@author: aziz-yamar.gueye@polyml.ca



from gfishnar import *

#------------------------------READ--------------------------------------------
yaml = YAML("input.yaml")
Gcode = Gcode()
gcode=Gcode.read(yaml.gcodepath)

#-----------------------------EXTRACT------------------------------------------
extract=extract(gcode)

#-----------------------------GENERATE-----------------------------------------
if yaml.curved == True:
    generate= Reverse(extract.deck,yaml.deck)
else:
    generate = Gen(extract.deck,yaml.deck)

#-----------------------------CALIBRATE----------------------------------------
calibrate=Calibrate(generate.deck,yaml.deck)

#-----------------------------WRITE--------------------------------------------
writer=write(generate.deck,calibrate.coord)
print 'Output file(s) is now available in the current directory'
print 'Import it into Excel, then copy-paste the content in the Fisnar software'

#-----------------------------REWRITE GCODE----------------------------------
if yaml.curved == True:
    GCODErewriter = GCODErewriter(yaml.gcodepath,generate.new_points,generate.new_E)
    print 'Output Gcode file is now available in the current directory'

#-----------------------------PLOT TOOLPATH ----------------------------------
plot = Toolpath_3D_plotter(calibrate.coord)
