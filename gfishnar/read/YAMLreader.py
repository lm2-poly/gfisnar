  # -*- coding: utf-8 -*-
import yaml
import os.path
import sys


class YAML():

    def __init__(self, inputFile):

            if not os.path.exists(inputFile):
                print "Error: Could not find" + inputFile
                sys.exit(1)
            else:
                with open(inputFile,'r') as f:

                    self.doc = yaml.load(f) # Container of the tags parsed from the yaml file

                    #Input file section :

                    if not "InputFile" in self.doc:
                        print "Error: Specify an InputFile section in your yaml"
                        sys.exit(1)
                    else:
                        if not "Path" in self.doc["InputFile"]:
                            print "Error: Specify Path tag in InputFile section"
                            sys.exit(1)
                        else:
                            self.gcodepath = self.doc["InputFile"]["Path"] #gcodepath attribute contains the 
                            #specified gcode path

                    #Minimal print distance section :

                    if not "Minimal print distance" in self.doc:
                        print "Error: Specify a Minimal print distance section in your yaml"
                        sys.exit(1)
                    else:
                        if not "D" in self.doc["Minimal print distance"]:
                            print "Error: Specify a D tag found in Minimal print distance section"
                            sys.exit(1)
                        elif self.doc["Minimal print distance"]["D"]==None:
                            print 'error: D tag in Minimal print distance section is empty'
                            sys.exit(1)
                        else:
                            self.dist_min = self.doc["Minimal print distance"]["D"] 

                    #Initial poistion section :

                    if not "Initial position" in self.doc:
                        print "Error: Specify an Initial position section in your yaml"
                        sys.exit(1)
                    else:
                        if not "X" in self.doc["Initial position"]:
                            print "Error: Specify X tag in Initial position section"
                            sys.exit(1)
                        elif not "Y" in self.doc["Initial position"]:
                            print "Error: Specify Y tag in Initial position section"
                            sys.exit(1)
                        elif not "Z" in self.doc["Initial position"]:
                            print "Error: Specify Z tag in Initial position section"
                            sys.exit(1)
                        elif self.doc["Initial position"]["X"]==None:
                            print 'error: X tag in Initial position section is empty'
                            sys.exit(1)
                        elif self.doc["Initial position"]["Y"]==None:
                            print 'error: Y tag in Initial position section is empty'
                            sys.exit(1)
                        elif self.doc["Initial position"]["Z"]==None:
                            print 'error: Z tag in Initial position section is empty'
                            sys.exit(1)
                        else:
                            self.X = self.doc["Initial position"]["X"] 
                            self.Y = self.doc["Initial position"]["Y"]
                            self.Z = self.doc["Initial position"]["Z"]

                    #Speed section :

                    if not "Speed" in self.doc:
                        print "Error: Specify a speed section in your yaml"
                        sys.exit(1)
                    else:
                        if not "Print speed" in self.doc["Speed"]:
                            print "Error: Specify Print speed tag in Speed section"
                            sys.exit(1)
                        elif not "Travel speed" in self.doc["Speed"]:
                            print "Error: Specify Travel speed tag in Speed section"
                            sys.exit(1)
                        elif self.doc["Speed"]["Print speed"]==None:
                            print 'error: Print speed tag in Speed section is empty'
                            sys.exit(1)
                        elif self.doc["Speed"]["Travel speed"]==None:
                            print 'error: Travel speed tag in Speed section is empty'
                            sys.exit(1)
                        else:
                            self.print_speed = self.doc["Speed"]["Print speed"] 
                            self.travel_speed = self.doc["Speed"]["Travel speed"]

                    # Translation between dispensers section :

                    if not "Translation between dispensers" in self.doc:
                        print "Error: Specify an Translation between dispensers section in your yaml"
                        sys.exit(1)
                    else:
                        if not "X" in self.doc["Translation between dispensers"]:
                            print "Error: No X tag found in Translation between dispensers section"
                            sys.exit(1)
                        elif not "Y" in self.doc["Translation between dispensers"]:
                            print "Error: No Y tag found in Translation between dispensers section"
                            sys.exit(1)
                        
                        elif self.doc["Translation between dispensers"]["X"]==None:
                            print 'error: X tag in Translation between dispensers section is empty'
                            sys.exit(1)
                        elif self.doc["Translation between dispensers"]["Y"]==None:
                            print 'error: Y tag in Translation between dispensers section is empty'
                            sys.exit(1)
                        else:
                            self.X_trans = self.doc["Translation between dispensers"]["X"] 
                            self.Y_trans = self.doc["Translation between dispensers"]["Y"]

                    # Rotation angle section :

                    if not "Rotation angle" in self.doc:
                        print "Error: Specify a Rotation angle section in your yaml"
                        sys.exit(1)
                    else:
                        if not "R" in self.doc["Rotation angle"]:
                            print "Error: No R tag found in Rotation angle section"
                            sys.exit(1)
                        elif self.doc["Rotation angle"]["R"]==None:
                            print 'error: R tag in Rotation angle section is empty'
                            sys.exit(1)
                        else:
                            self.rotation = self.doc["Rotation angle"]["R"]

                    #Construction of the class YAML deck:

                    self.deck={'X_init':self.X,
                    'Y_init':self.Y,
                    'Z_init':self.Z,
                    'print_speed':self.print_speed,
                    'travel_speed':self.travel_speed,
                    'X_trans':self.X_trans,
                    'Y_trans':self.Y_trans,
                    'dist_min':self.dist_min,
                    'rotation_angle':self.rotation}
