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

                    if not "InputFile" in self.doc:
                        print "Error: Specify an InputFile section in your yaml"
                        sys.exit(1)
                    else:
                        if not "Path" in self.doc["InputFile"]:
                            print "Error: No Path tag found"
                            sys.exit(1)
                        else:
                            self.gcodepath = self.doc["InputFile"]["Path"] #gcodepath attribute contains the 
                            #specified gcode path
