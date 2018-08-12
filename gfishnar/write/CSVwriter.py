#-*- coding: utf-8 -*-
#@author: soufiane.hifdi@polymtl.ca
import csv

## Class writing the data generated into a CSV file
class write():

	## Constructor
	# @param generated_deck Deck given by the Gen class
	# @param calibrated_coord Tuple (X,Y,Z) of the calibrated coordinates, from the Calibrate class
	def __init__(self,generated_deck,calibrated_coord):

		## List containing all the elements to be written in the CSV file
		self.assembled=write.assembly(self,generated_deck['status'],calibrated_coord,
			generated_deck['IO'],generated_deck['rotation'],generated_deck['Speed'])

		myFile = open('output.csv', 'w')
		with myFile:
    			writer = csv.writer(myFile)
    			writer.writerows(self.assembled)

    ## Assembles all the data and modifies their structure to match the CSV writer structure
    # @param status Multimaterial printing status of the Fisnar, from the Gen class deck
    # @param calibrated_coord calibrated coordinates from the Calibrate class
    # @param IO Fisnar extrusion (0 if no extrusion, 1 otherwise), from the Gen class deck
    # @param rotation Angle of rotation from the Gen class deck
    # @param speed Printing speed as given by the Gen class deck
	def assembly(self,status,calibrated_coord,IO,rotation,speed):
		X=[]
		Y=[]
		Z=[]
		list_of_lists=[]
		
		for i in range(0,len(calibrated_coord)):
			X.append(calibrated_coord[i][0])
			Y.append(calibrated_coord[i][1])
			Z.append(calibrated_coord[i][2])

		list_of_lists.append(status)
		list_of_lists.append(X)
		list_of_lists.append(Y)
		list_of_lists.append(Z)
		list_of_lists.append(IO)
		list_of_lists.append(rotation)
		list_of_lists.append(speed)
		return list_of_lists