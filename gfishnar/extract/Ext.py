#-*- coding: utf-8 -*-
#@author: soufiane.hifdi@polyml.ca

import re

## Class extracting all the needed data from the gcode file
class extract():

    ## Constructor
    # @param gcode the gcode as given by the GCODE class

    def __init__(self,gcode, yaml_deck):
        ## Start index of the print, i.e layer 1
        self.start_index=extract.start(self,gcode, yaml_deck)

        ## End index of the print, i.e layer end
        self.end_index=extract.end(self,gcode)

        ## Tuple of the Y coordinates and corresponding indicies in the gcode
        self.Y=extract.Y(self,gcode,self.start_index,self.end_index)

        ## Tuple of the Z coordinates and corresponding indicies in the gcode
        self.layers=extract.layers(self,gcode,self.start_index,self.end_index)

        ## Tuple of the G status and corresponding indicies in the gcode
        self.G=extract.G(self,gcode,self.start_index,self.end_index)

        ## Tuple of the sublayers extracted and corresponding indicies in the gcode
        self.sublayers=extract.sublayers(self,gcode,self.start_index,self.end_index)

        ## Tuple of the X coordinates and corresponding indicies in the gcode
        self.X=extract.X(self,gcode,self.start_index,self.end_index)

        ## Tuple of the extruder extracted and it's corresponding indicies in the gcode
        self.T=extract.extruder(self,gcode,self.start_index,self.end_index)

        ## Tuple of the E extracted and it's corresponding indicies in the gcode
        self.E=extract.E(self,gcode,self.start_index,self.end_index)

        ## Deck of the class extract
        self.deck={'X':self.X,
        'Y':self.Y,
        'layers':self.layers,
        'G':self.G,
        'sublayers':self.sublayers,
        'end_index':self.end_index,
        'start_index':self.start_index,
        'T':self.T,
        'E':self.E}

    ## Extracts the index of 'layer1'
    # @param gcode the gcode
    def start(self,gcode,yaml_deck):
        if yaml_deck['slicer'] == "Simplify3D":
        	# Finds pattern:'layer 1'
            pattern=re.compile(r';\slayer\s1,')
        elif yaml_deck['slicer'] == "Slic3r":
            # Finds pattern:'layer 0'
            pattern=re.compile(r';\slayer\s0,')
        end= pattern.finditer(gcode)
        for endlayer in end:
            index=endlayer.start()
        # Returns the start index
        return index


    ## Extracts the X coordinates from the gcode
    # @param gcode the gcode
    # @param start_index start index of the print
    # @param end_index end index of the print
    def X(self,gcode,start_index,end_index):
    	# Finds pattern, example of pattern: X121.233
        pattern=re.compile(r'\bX\d+\.\d+\b')
        Xmatches=pattern.findall(gcode[start_index:end_index])
        X=pattern.finditer(gcode[start_index:end_index])
        indices=[]
        for x in X:
    	   indices.append(x.start()+start_index)
    	# Returns all the matches and their start indicies
        return Xmatches,indices

    ## Extracts the Y coordinates from the gcode
    # @param gcode the gcode
    # @param start_index start index of the print
    # @param end_index end index of the print
    def Y(self,gcode,start_index,end_index):
    	# Finds pattern, example of pattern: Y121.233
        pattern=re.compile(r'\bY\d+\.\d+\b')
        Ymatches=pattern.findall(gcode[start_index:end_index])
        Y=pattern.finditer(gcode[start_index:end_index])
        indices=[]
        for y in Y:
    	   indices.append(y.start()+start_index)
    	# Returns all the matches and their start indicies
        return Ymatches,indices

    ## Extracts the layers from the gcode
    # @param gcode the gcode
    # @param start_index start index of the print
    # @param end_index end index of the print
    def layers(self,gcode,start_index,end_index):
    	# Finds pattern, example of pattern: Z0.250
        pattern=re.compile(r'\bZ\d+\.\d+\b') #Modified by Aziz 30/03/2019 to find layer Z coordinate from "Z0.AAA" instead of "Z = XXXX"
        #pattern=re.compile(r'\bZ\s=\s\d+\.\d+')
        matchesZ=pattern.findall(gcode[0:end_index])
        Layers= pattern.finditer(gcode[0:end_index])
        indices=[]
        for layers in Layers:
        	indices.append(layers.start())
        # Returns all the matches and their start indicies
        return matchesZ,indices

    ## Extracts the G status from the gcode
    # @param gcode the gcode
    # @param start_index start index of the print
    # @param end_index end index of the print
    def G(self,gcode,start_index,end_index):
    	# Finds pattern, example of pattern: G0 X110.20
        pattern=re.compile(r'\b(G\d+)\s\bX\d+\.\d+\b')
        Gmatches=pattern.findall(gcode[start_index:end_index])
        # Only returns the first group (G\d+)
        G=pattern.finditer(gcode[start_index:end_index])
        indices=[]
        for g in G:
    	   indices.append(g.start(1)+start_index)
        # Returns all the matches and their start indicies
        return Gmatches,indices

    ## Extracts the sublayers from the gcode
    # @param gcode the gcode
    # @param start_index start index of the print
    # @param end_index end index of the print
    def sublayers(self,gcode,start_index,end_index):
    	# Finds pattern, example of pattern :;  outer perimeter\nG1 X223.232
        pattern=re.compile(r';\s(\w+|\w+\s\w+)\n\bG\d+\s\bX\d+\.\d+\b')
        # Only returns the first group (\w+|\w+\s\w+)
        matches=pattern.findall(gcode[start_index:end_index])
        sublayers= pattern.finditer(gcode[start_index:end_index])
        indices=[]
        for layers in sublayers:
    	   indices.append(layers.start(1)+start_index)
        # Returns all the matches and their start indicies
        return matches,indices

    ## Extracts the E from the gcode
    # @param gcode the gcode
    # @param start_index start index of the print
    # @param end_index end index of the print
    def E(self,gcode,start_index,end_index):
    	# Finds pattern, example of pattern: G0 X112.210 Y200.321 E44.44
        pattern=re.compile(r'\bG\d+\s\bX\d+\.\d+\s\bY\d+\.\d+\s\b(E\d+\.\d+)\b')
        # Only returns the first group (E\d+\.\d+)
        matches=pattern.findall(gcode[start_index:end_index])
        E=pattern.finditer(gcode[start_index:end_index])
        indices=[]
        for e in E:
           indices.append(e.start(1)+start_index)
        # Returns all the matches and their start indicies
        return matches,indices

    ## Extracts extruder T0/T1 from the gcode
    # @param gcode the gcode
    # @param start_index start index of the print
    # @param end_index end index of the print
    def extruder(self,gcode,start_index,end_index):
    	# Finds pattern, example of pattern: T0
        pattern=re.compile(r'\bT\d')
        matches=pattern.findall(gcode[start_index:end_index])
        extruder=pattern.finditer(gcode[start_index:end_index])
        indices=[]
        for T in extruder:
           indices.append(T.start()+start_index)
        # Returns all the matches and their start indicies
        return matches,indices

    ## Extracts layer end from the gcode
    # @param gcode the gcode
    # @param start_index start index of the print
    # @param end_index end index of the print
    def end(self,gcode):
    	# Finds pattern, pattern 'layer end'
        pattern=re.compile(r';\slayer\send')
        end= pattern.finditer(gcode)
        for endlayer in end:
            index=endlayer.start()
        # Returns the start index of 'layer end'
        return index
