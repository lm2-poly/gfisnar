 # -*- coding: utf-8 -*-
import re 

class extract():
   	def __init__(self,gcode):

            self.start_index=extract.start(self,gcode)
            self.end_index=extract.end(self,gcode)

            self.Y=extract.Y(self,gcode,self.start_index,self.end_index)
            self.layers=extract.layers(self,gcode,self.start_index,self.end_index)
            self.G=extract.G(self,gcode,self.start_index,self.end_index)
            self.sublayers=extract.sublayers(self,gcode,self.start_index,self.end_index)
            self.X=extract.X(self,gcode,self.start_index,self.end_index)
            self.T=extract.extruder(self,gcode,self.start_index,self.end_index)
            self.E=extract.E(self,gcode,self.start_index,self.end_index)
            self.deck={'X':self.X,
            'Y':self.Y,
            'layers':self.layers,
            'G':self.G,
            'sublayers':self.sublayers,
            'end_index':self.end_index,
            'start_index':self.start_index,
            'T':self.T,
            'E':self.E}

        def start(self,gcode):
            pattern=re.compile(r';\slayer\s1,')#pattern:; layer end
            end= pattern.finditer(gcode)
            for endlayer in end:
                index=endlayer.start()
            return index

        def X(self,gcode,start_index,end_index):
        
            pattern=re.compile(r'\bX\d+\.\d+\b') #pattern: X121.233
            Xmatches=pattern.findall(gcode[start_index:end_index])
            X=pattern.finditer(gcode[start_index:end_index])
            indices=[]
            for x in X:
        	indices.append(x.start()+start_index)
            return Xmatches,indices	
		
        def Y(self,gcode,start_index,end_index):

            pattern=re.compile(r'\bY\d+\.\d+\b') #pattern: Y121.253
            Ymatches=pattern.findall(gcode[start_index:end_index])
            Y=pattern.finditer(gcode[start_index:end_index])
            indices=[]
            for y in Y:
        	indices.append(y.start()+start_index)
            return Ymatches,indices	
        

        def layers(self,gcode,start_index,end_index):

    	    pattern=re.compile(r'\bZ\s=\s\d+\.\d+') #pattern: Z = 12.152
            matchesZ=pattern.findall(gcode[start_index:end_index])
            Layers= pattern.finditer(gcode[start_index:end_index])
            indices=[]
            for layers in Layers:
            	indices.append(layers.start()+start_index)
            return matchesZ,indices	

        def G(self,gcode,start_index,end_index):

            pattern=re.compile(r'\b(G\d+)\s\bX\d+\.\d+\b') #pattern: G1 X121.230
    	   #only returns the first group (G\d+)
            Gmatches=pattern.findall(gcode[start_index:end_index])
            G=pattern.finditer(gcode[start_index:end_index])
            indices=[]
            for g in G:
        	   indices.append(g.start(1)+start_index)
            return Gmatches,indices	

        def sublayers(self,gcode,start_index,end_index):

            pattern=re.compile(r';\s(\w+|\w+\s\w+)\n\bG\d+\s\bX\d+\.\d+\b')#pattern:;  outer perimeter\nG1 X223.232
    	   #only returns the first group (\w+|\w+\s\w+), one word or two
            matches=pattern.findall(gcode[start_index:end_index])
            sublayers= pattern.finditer(gcode[start_index:end_index])
            indices=[]
            for layers in sublayers:
        	   indices.append(layers.start(1)+start_index)
            return matches,indices

        def E(self,gcode,start_index,end_index):

            pattern=re.compile(r'\bG\d+\s\bX\d+\.\d+\s\bY\d+\.\d+\s\b(E\d+\.\d+)\b') #pattern: E4.440
            matches=pattern.findall(gcode[start_index:end_index])
            E=pattern.finditer(gcode[start_index:end_index])
            indices=[]
            for e in E:
               indices.append(e.start(1)+start_index)
            return matches,indices 

        def extruder(self,gcode,start_index,end_index):

            pattern=re.compile(r'\bT\d') #pattern: T1/T0
            matches=pattern.findall(gcode[start_index:end_index])
            extruder=pattern.finditer(gcode[start_index:end_index])
            indices=[]
            for T in extruder:
               indices.append(T.start()+start_index)
            return matches,indices 

        def end(self,gcode):

            pattern=re.compile(r';\slayer\send')#pattern:; layer end
            end= pattern.finditer(gcode)
            for endlayer in end:
                index=endlayer.start()
            return index
