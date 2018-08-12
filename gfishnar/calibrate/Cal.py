#-*- coding: utf-8 -*-
#@author: soufiane.hifdi@polyml.ca

## Class to calibrate the coordinates and take into account the distance between extruders
class Calibrate():

	## Constructor
	# @param generated_deck Deck produced by the generate class
	# @param yaml_deck Deck from yaml class containing the infos of the input file
	def __init__(self,generated_deck,yaml_deck):

		## tuple of calibrated coordinates from the coord method
		self.coord=Calibrate.coord(self,generated_deck['coord_to_keep'],
			generated_deck['extruder'],
			yaml_deck['X_init'],yaml_deck['Y_init'],yaml_deck['Z_init'],
			yaml_deck['X_trans'],yaml_deck['Y_trans'])

	## Calibrates the coordinates 
	# @param distance_checked_coordinates Distance checked coordinates from the Gen class deck
	# @param T List that gives which extruder in use for every point 
	# @param X_init Initialization X coordinate from the input.yaml
	# @param Y_init Initialization Y coordinate from the input.yaml
	# @param Z_init Initialization Z coordinate from the input.yaml
	# @param X_trans X translation between the two extruders 
	# @param Y_trans Y translation between the two extruders
	def coord(self,distance_checked_coordinates,T,X_init,Y_init,Z_init,X_trans,Y_trans):

		Xfishnar=[]
		Yfishnar=[]
		Zfishnar=[]
		# adaptation of X,Y,Z to fisnar coordinates
		for i in range(0,len(distance_checked_coordinates)):
			X= distance_checked_coordinates[i][0]+X_init-distance_checked_coordinates[0][0]
			Xfishnar.append(X)
			Y=distance_checked_coordinates[i][1]+Y_init-distance_checked_coordinates[0][1]
			Yfishnar.append(Y)
			Z= -(distance_checked_coordinates[i][2])+Z_init
			Zfishnar.append(Z)
		# If the the second extruder is on, add the distance between dispensers
			if T[i]=='T1':
				Xfishnar[i]+=X_trans
				Yfishnar[i]+=Y_trans

		return zip(Xfishnar,Yfishnar,Zfishnar)