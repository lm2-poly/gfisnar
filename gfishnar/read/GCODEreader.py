# -*- coding: utf-8 -*-
#@author: soufiane.hifdi@polyml.ca

## Class reading the gcode file
class Gcode():

	## Method that reads the gcode file and returns it as a python string
	# @param  Gcodepath Path of the gcode given in the input.YAML
    def read(self,Gcodepath):
        f = open(Gcodepath, 'r')
        Gcode = f.read()
        return Gcode