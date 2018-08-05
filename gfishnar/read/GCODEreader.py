# -*- coding: utf-8 -*-
class Gcode():
    def read(self,Gcodepath):
        f = open(Gcodepath, 'r')
        Gcode = f.read()
        return Gcode