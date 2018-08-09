# -*- coding: utf-8 -*-
import csv

class write():

	def __init__(self,generated_deck,calibrated_coord):

		self.assembled=write.assembly(self,generated_deck['status'],calibrated_coord,
			generated_deck['IO'],generated_deck['rotation'],generated_deck['Speed'])

		myFile = open('output.csv', 'w')
		with myFile:
    			writer = csv.writer(myFile)
    			writer.writerows(self.assembled)

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