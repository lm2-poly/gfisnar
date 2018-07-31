 # -*- coding: utf-8 -*-
import re 

class extract():
    """Any method of this class, finds the patterns and retruns the matches and their start indices"""
    def X(self,gcode):
        
    	pattern=re.compile(r'\bX\d+\.\d+\b') #pattern: X121.233
        Xmatches=pattern.findall(gcode)
        X=pattern.finditer(gcode)
        indices=[]
        for x in X:
        	indices.append(x.start())
        return Xmatches,indices	
		
    def Y(self,gcode):

        pattern=re.compile(r'\bY\d+\.\d+\b') #pattern: Y121.253
        Ymatches=pattern.findall(gcode)
        Y=pattern.finditer(gcode)
        indices=[]
        for y in Y:
        	indices.append(y.start())
        return Ymatches,indices	
        

    def layers(self,gcode):

    	pattern=re.compile(r'\bZ\s=\s\d+\.\d+') #pattern: Z = 12.152
        matchesZ=pattern.findall(gcode)
        Layers= pattern.finditer(gcode)
        indices=[]
        for layers in Layers:
        	indices.append(layers.start())
        return matchesZ,indices	

    def G(self,gcode):

    	pattern=re.compile(r'\b(G\d+)\s\bX\d+\.\d+\b') #pattern: G1 X121.230
    	#only returns the first group (G\d+)
        Gmatches=pattern.findall(gcode)
        G=pattern.finditer(gcode)
        indices=[]
        for g in G:
        	indices.append(g.start())
        return Gmatches,indices	

    def sublayers(self,gcode):

    	pattern=re.compile(r';\s(\w+|\w+\s\w+)\n\bG\d+\s\bX\d+\.\d+\b')#pattern:;  outer perimeter\nG1 X223.232

    	#only returns the first group (\w+|\w+\s\w+), one word or two
        matches=pattern.findall(gcode)
        sublayers= pattern.finditer(gcode)
        indices=[]
        for layers in sublayers:
        	indices.append(layers.start())
        return matches,indices

    def end(self,gcode):
        pattern=re.compile(r';\slayer\send')#pattern:; layer end
        end= pattern.finditer(gcode)
        for endlayer in end:
            index=endlayer.start()
        return index