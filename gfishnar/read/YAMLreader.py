#-*- coding: utf-8 -*-
#@author: soufiane.hifdi@polyml.ca

import yaml
import os.path
import sys

## Class reading and storing the inputs of the user in the input.yaml
class YAML():

    ## Constructor
    # Reads the input.yaml file, assigns to each tag it's value and gives error messages to the user in case of misuse
    # @param inputFile The folder path of the input.yaml file
    def __init__(self, inputFile):

            if not os.path.exists(inputFile):
                print "Error: Could not find" + inputFile
                sys.exit(1)
            else:
                with open(inputFile,'r') as f:

                    ## Container of the tags parsed from the yaml file
                    self.doc = yaml.load(f)

                    # Reads the Input file section :

                    if not "InputFile" in self.doc:
                        print "Error: Specify an InputFile section in your yaml"
                        sys.exit(1)
                    else:
                        if not "Path" in self.doc["InputFile"]:
                            print "Error: Specify Path tag in InputFile section"
                            sys.exit(1)
                        else:
                            ## Path of the gcode file to modify
                            self.gcodepath = self.doc["InputFile"]["Path"]

                    # Reads the Minimal print distance section :

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
                            ## Mininal distance specified in the yaml
                            self.dist_min = self.doc["Minimal print distance"]["D"]

                    # Reads the Initial poistion section :

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
                            ## initial X poisition of the start point
                            self.X = self.doc["Initial position"]["X"]
                            ## initial Y poisition of the start point
                            self.Y = self.doc["Initial position"]["Y"]
                            ## initial Z poisition of the start point
                            self.Z = self.doc["Initial position"]["Z"]

                    # Reads the Speed section :

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
                            ## Print speed (if extrusion of ink takes place)
                            self.print_speed = self.doc["Speed"]["Print speed"]
                            ## Travel speed
                            self.travel_speed = self.doc["Speed"]["Travel speed"]

                    # Reads the Translation between dispensers section :

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
                            ## X coordinate distance between the dispensers
                            self.X_trans = self.doc["Translation between dispensers"]["X"]
                            ## Y coordinate distance between the dispensers
                            self.Y_trans = self.doc["Translation between dispensers"]["Y"]

                    # Reads the Rotation angle section :

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
                            ## Angle of rotation of the Fisnar
                            self.rotation = self.doc["Rotation angle"]["R"]

                    # Reads the Curved toolpath section :

                    if not "Curved toolpath" in self.doc:
                        print "Error: Specify a curved toolpath section in your yaml"
                        sys.exit(1)
                    else:
                        if not "Curved" in self.doc["Curved toolpath"]:
                            print "Error: Specify Curved tag in Curved toolpath section"
                            sys.exit(1)
                        elif self.doc["Curved toolpath"]["Curved"]==None:
                            print 'error: Curved tag in Curved toolpath section is empty'
                            sys.exit(1)
                        else:
                            self.curved = self.doc["Curved toolpath"]["Curved"]
                            if self.doc["Curved toolpath"]["Curved"] == True:
                                if not "Curvature radius" in self.doc["Curved toolpath"]:
                                    print "Error: Specify Curvature radius tag in Curved toolpath section"
                                    sys.exit(1)
                                elif self.doc["Curved toolpath"]["Curvature radius"]==None:
                                    print 'error: Curvature radius tag in Curved toolpath section is empty'
                                    sys.exit(1)
                                else:
                                    self.curvature_radius = self.doc["Curved toolpath"]["Curvature radius"]

                                if not "Interpolation precision" in self.doc["Curved toolpath"]:
                                    print "Error: Specify Interpolation precision tag in Curved toolpath section"
                                    sys.exit(1)
                                elif self.doc["Curved toolpath"]["Interpolation precision"]==None:
                                    print 'error: INterpolation precision tag in Curved toolpath section is empty'
                                    sys.exit(1)
                                else:
                                    self.interpolation_precision = self.doc["Curved toolpath"]["Interpolation precision"]
                            else:
                                self.interpolation_precision = None
                                self.curvature_radius = None


                    ## Deck of the YAML class
                    self.deck={'X_init':self.X,
                    'Y_init':self.Y,
                    'Z_init':self.Z,
                    'print_speed':self.print_speed,
                    'travel_speed':self.travel_speed,
                    'X_trans':self.X_trans,
                    'Y_trans':self.Y_trans,
                    'dist_min':self.dist_min,
                    'rotation_angle':self.rotation,
                    'curved':self.curved,
                    'curvature_radius':self.curvature_radius,
                    'interpolation_precision':self.interpolation_precision}
