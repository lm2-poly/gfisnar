#-*- coding: utf-8 -*-
#@author: aziz-yamar.gueye@polyml.ca

from .Gen import *


## Class to reverse transform the toolpath in order to obtain a curved toolpath
class Reverse(Gen):

	## Constructor
    # @param deck The deck of the extract class
    # @param yaml_deck The deck of the YAML class
	def __init__(self,deck,yaml_deck):

		## X Y Z coordinates for each line of Gcode and the index of the beginning of the line
		self.points = Reverse.points(self,deck['X'],deck['Y'],deck['layers'])

		self.R = yaml_deck['curvature_radius']

		## New X Y Z  coordinates for the curved toolpath
		self.new_points = Reverse.new_points(self,self.points,self.R)

		## New extrusion values for the curved toolpath
		self.new_E = Reverse.new_E(self,deck['E'], self.points, self.new_points)

		## Deck of the Reverse class
		self.deck = Reverse.regenerate(self,deck,yaml_deck,self.new_points,self.new_E)



	def points(self,deckX,deckY,deckLayers):
		## Retrieves the X, Y and Z coordinates and corresponding indices of the Gcode
		## Returns a list of points in the format [X Y Z index] in each line where index is the index of the beginning of the line in Gcode

		# @param deckX The X coordinates from the deck of the extract class
		# @param deckY The Y coordinates from the deck of the extract class
		# @param deckLayers The Z coordinates from the deck of the extract class
		X=[]
		Y=[]
		Z=[]
		for x,i in zip(deckX[0],deckX[1]):
			X.append ([float(x[1:]), i ])
		for y,i in zip(deckY[0],deckY[1]):
			Y.append ([float(y[1:]), i])
		for z,i in zip(deckLayers[0],deckLayers[1]):
			Z.append ([float(z[4:]), i])
		points = []
		for i in range (0,len(X)):
			points.append ([ X[i][0] , Y[i][0] ])
		k=0

		# adds z coordinate to the list of points
		for j in range(0,len(Z)):
			while X[k][1] < Z[j][1]:
				points[k].append(Z[j-1][0])
				points[k].append(X[k][1])
				k=k+1
			if X[k][1]>Z[-1][1]: #for the last layer
				for i in range(k,len(X)):
					points[i].append(Z[-1][0])
					points[i].append(X[i][1])
		if len(points)!=len(X):
			print 'X and Z coordinates does not match'
		if len(points)!=len(Y):
			print 'Y and Z coordinates does not match'
		return points

	def new_points(self,points,R):
		## Calculates the new coordinates of each point by applying reverse transformation
		# @param points The points from points method
		# @param R  Z Distance between nozzle initial position and lowest layer

		new_points = []
		for point in points:
			new_point = []
			new_point.append(round(point[0],3))
			alpha = point[1]/R
			new_point.append(round(math.tan(alpha)*math.fabs(math.cos(alpha))*(R-point[2]),3))
			new_point.append(round(R - math.fabs(math.cos(alpha))*(R-point[2]),3))
			new_point.append(point[3])
			new_points.append(new_point)
		return new_points

	def new_E(self,deckE,points,new_points):
		## Calculates the new extrusion values of each line by conserving the extrusion per length unit in planar toolpath
		# @param deckE The extrusion values list from extract class
		# @param points The points from points method
		# @param new_points  The new points from new_points method

		E=[]
		for i in range(0,len(deckE[0])):
			extrusion = float(deckE[0][i][1:])
			index = deckE[1][i]
			E.append([extrusion , index])

		new_E = []
		for i,e in enumerate(E):
			for k in range(0,len(points)):
				if points[k-1][3]< e[1] <points[k][3]:
					dist=math.sqrt((points[k-1][0]-points[k-2][0])**2 +(points[k-1][1]-points[k-2][1])**2 +(points[k-1][2]-points[k-2][2])**2)
					new_dist = math.sqrt((new_points[k-1][0]-new_points[k-2][0])**2
					+(new_points[k-1][1]-new_points[k-2][1])**2 +(new_points[k-1][2]-new_points[k-2][2])**2)

					new_e = round(((new_dist * (e[0] -E[i-1][0] ) / dist) + E[i-1][0]),4)
					new_E.append([new_e , e[1]])


			if  i == (len(E)-1): #for last point
				dist=math.sqrt((points[-1][0]-points[-2][0])**2 +(points[-1][1]-points[-2][1])**2 +(points[-1][2]-points[-2][2])**2)
				new_dist = math.sqrt((new_points[-1][0]-new_points[-2][0])**2 +(new_points[-1][1]-new_points[-2][1])**2 +(new_points[-1][2]-new_points[-2][2])**2)

				new_e = round(( (new_dist * (e[0] -E[i-1][0]) / dist) + E[i-1][0]),4)
				new_E.append([new_e , e[1]])

		return new_E

	def regenerate(self,deck,yaml_deck,new_points,new_E):
		## Regenerates a new deck with new X Y Z coordinates and extrusion values
		# @param deck The deck from extract class
		# @param yaml_deck The deck from YAML class
		# @param new_points The list of points from new_points method
		# @param new_E The extrusion values from new_E method

		X = [point[0] for point in new_points]
		Y = [point[1] for point in new_points]
		Z = [point[2] for point in new_points]
		self.coordinates = zip(X,Y,Z)
		## Coordinates of the points that passed the distance check calculation
		self.distance_checked_coord=Reverse.DistanceCheck(self,self.coordinates,yaml_deck['dist_min'])[0]

		## Indices of the points that passed the distance check calculation
		self.indices_to_keep=Gen.DistanceCheck(self,self.coordinates,yaml_deck['dist_min'])[1]

		## Modified G status, adapted for the fisnar
		self.mod_G=Gen.modG(self,deck['G'],deck['sublayers'],deck['end_index'],self.indices_to_keep)

		## Extruder in use for every point
		self.T=Gen.T(self,deck['X'],deck['Y'],deck['T'],deck['end_index'],self.indices_to_keep)

		## Mutlimaterial Fisnar status
		self.fisnar_status=Gen.status(self,self.T)

		## Fisnar IO: 0 if no extrusion, 1 otherwise
		self.IO=Gen.IO(self,deck['X'],deck['E'],self.indices_to_keep)

		## Speed for every point
		self.speed=Gen.speed(self,self.mod_G,
			yaml_deck['travel_speed'],yaml_deck['print_speed'],self.IO)[0]

		self.mod_G_to_keep=Gen.speed(self,self.mod_G,
			yaml_deck['travel_speed'],yaml_deck['print_speed'],self.IO)[1]

		## Angle of rotation
		self.rotation=Gen.rotation(self,self.distance_checked_coord,yaml_deck['rotation_angle'])

		## Deck of the Gen class
		self.deck={'status':self.fisnar_status
		,'coord_to_keep':self.distance_checked_coord
		,'indices_to_keep':self.indices_to_keep
		,'mod_G_to_keep':self.mod_G_to_keep
		,'Speed':self.speed
		,'rotation':self.rotation
		,'extruder':self.T
		,'IO':self.IO
	}
		return self.deck
