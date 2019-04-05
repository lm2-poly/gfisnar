#-*- coding: utf-8 -*-
#@author: aziz-yamar.gueye@polyml.ca

from gfishnar import *

#------------------------------READ--------------------------------------------
yaml = YAML("input.yaml")
Gcode = Gcode()
gcode=Gcode.read(yaml.gcodepath)
#-----------------------------EXTRACT------------------------------------------
extract=extract(gcode,yaml.deck)
#-----------------------------GENERATE-----------------------------------------
generate= Reverse(extract.deck,yaml.deck)
#-----------------------------REWRITE GCODE----------------------------------
GCODErewriter = GCODErewriter(yaml.gcodepath,generate.final_reversed_points,generate.final_reversed_E)
print 'Output Gcode file is now available in the current directory'
#-----------------------------PLOT TOOLPATH ----------------------------------
plot = Toolpath_3D_plotter(generate.final_reversed_points)
layer_coordinates = plot.reversed_layer_coordinates(extract.deck,generate.final_reversed_points)
layer_plot = plot.layer_plot(6,layer_coordinates)
