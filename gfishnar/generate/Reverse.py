#-*- coding: utf-8 -*-
#@author: aziz-yamar.gueye@polyml.ca

from .Gen import *

def distance(point1,point2):
	## Computes and returns distance between two 3D points
	# @param point1 list of the XYZ coordinates of the point 1
	# @param point2 list of the XYZ coordinates of the point 2
	dist = math.sqrt((point1[0]-point2[0])**2 +(point1[1]-point2[1])**2 +(point1[2]-point2[2])**2)
	return dist

def middle_point(point1,point2):
	## Computes and returns the middle point of segment defined by the two points
	# @param point1 list of the XYZ coordinates and index of the point 1: ex [x y z index]
	# @param point2 list of the XYZ coordinates and index of the point 2: ex [x,y,z, index]
	x= (point1[0]+point2[0])/2
	y= (point1[1]+point2[1])/2
	z= (point1[2]+point2[2])/2
	i = point2[3]
	middle_point = [x,y,z,i]
	return middle_point

## Class to reverse transform the toolpath in order to obtain a curved toolpath
# Mettre plus d'infos
class Reverse(Gen):

	## Constructor
    # @param deck The deck of the extract class
    # @param yaml_deck The deck of the YAML class
	def __init__(self,deck,yaml_deck):

		## Curvature radius from input.yaml
		self.R = yaml_deck['curvature_radius']

		## Interpolation precision from input.yaml
		self.interpolation_precision = yaml_deck['interpolation_precision']

		## X Y Z coordinates for each line of Gcode and the index of the beginning of the line
		self.points = Reverse.points(self,deck['X'],deck['Y'],deck['layers'])

		## New X Y Z  coordinates that are reversed for the curved toolpath
		self.reversed_points = Reverse.reversed_points(self,self.points,self.R)

		## XYZ coordinates with added coordinates from interpolation for curved toolpath
		self.final_points = Reverse.interpolate(self, self.points, self.R, self.interpolation_precision)[0]

		##Final XYZ coordinates that are reversed for curved toolpath
		self.final_reversed_points = Reverse.interpolate(self, self.points, self.R, self.interpolation_precision)[1]

		##Extrusion values from extract deck
		self.extrusion = Reverse.E(self,deck['E'])

		## Extrusion values with added extrusion values from interpolation
		self.final_E = Reverse.final_E(self,self.extrusion,self.points,self.final_points)

		## Final extrusion values for curved toolpath
		self.final_reversed_E = Reverse.final_reversed_E(self, self.extrusion, self.final_E, self.points, self.final_points, self.final_reversed_points)

		## Modify deck before generation
		self.modify_deck = Reverse.modify_deck(self, deck, self.final_reversed_E, self.reversed_points,self.final_reversed_points)

		## Deck of the Reverse class
		self.deck = Reverse.regenerate(self,self.modify_deck,yaml_deck,self.points,self.final_reversed_points,self.extrusion)

	## Retrieves the X, Y and Z coordinates and corresponding indices of the Gcode
	## Returns a list of points in the format [X Y Z index] in each line where index is the index of the X coordinate of the line in Gcode
	# @param deckX The X coordinates from the deck of the extract class
	# @param deckY The Y coordinates from the deck of the extract class
	# @param deckLayers The Z coordinates from the deck of the extract class
	def points(self,deckX,deckY,deckLayers):

		X=[]
		Y=[]
		Z=[]
		for x,i in zip(deckX[0],deckX[1]):
			X.append ([float(x[1:]), i ])
		for y,i in zip(deckY[0],deckY[1]):
			Y.append ([float(y[1:]), i])
		for z,i in zip(deckLayers[0],deckLayers[1]):
			Z.append ([float(z[1:]), i])
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

	## Calculates the new coordinates of a signle point by applying reverse transformation
	# @param a point with [x y z index] format
	# @param R  curvature_radius from input.yaml
	def reversed_point(self,point,R):

		new_point = []
		new_point.append(round(point[0],3))
		alpha = point[1]/R
		new_point.append(round(math.tan(alpha)*math.fabs(math.cos(alpha))*(R-point[2]),3))
		new_point.append(round(R - math.fabs(math.cos(alpha))*(R-point[2]),3))
		new_point.append(point[3])
		return new_point

	## Calculates the new coordinates of all points by applying reverse transformation
	# @param points The points from points method
	# @param R  curvature_radius from input.yaml
	def reversed_points(self,points,R):

		new_points = []
		if isinstance(points[0],(int,float)):
			new_points.append(round(points[0],3))
			alpha = points[1]/R
			new_points.append(round(math.tan(alpha)*math.fabs(math.cos(alpha))*(R-points[2]),3))
			new_points.append(round(R - math.fabs(math.cos(alpha))*(R-points[2]),3))
		else:
			for point in points:
				new_point = []
				new_point.append(round(point[0],3)) #reversed x coordinate
				alpha = point[1]/R
				new_point.append(round(math.tan(alpha)*math.fabs(math.cos(alpha))*(R-point[2]),3)) #reversed y coordinate
				new_point.append(round(R - math.fabs(math.cos(alpha))*(R-point[2]),3)) #reversed z coordinate
				new_point.append(point[3]) #keeps the index of X coordinate as the index of the point
				new_points.append(new_point)
		return new_points

	## Introduces interpolation points
	# @param points The points from points method
	# @param R curvature radius from input.yaml
	# @param interpolation_precision interpolation precision from input.yaml
	def interpolate(self, points, R, interpolation_precision):

		final_points = []
		for point in points:
			final_points.append(point)
		final_reversed_points =[]
		i=0
		reverse_point1 = Reverse.reversed_point(self,final_points[i],R)
		final_reversed_points.append(reverse_point1)
		while i<len(final_points)-1:
			middle1 = middle_point(final_points[i],final_points[i+1])
			reverse_middle = Reverse.reversed_point(self,middle1,R)
			reverse_point1 = Reverse.reversed_point(self,final_points[i],R)
			reverse_point2 = Reverse.reversed_point(self,final_points[i+1],R)
			middle2 = middle_point(reverse_point1, reverse_point2)
			dist = distance(reverse_middle,middle2)
			if dist < interpolation_precision:
				final_reversed_points.append(reverse_point2)
				i += 1
			else:
				final_points.insert(i+1,middle1)

		assert len(final_reversed_points) == len(final_points), "Length of final reversed points is not equal to length of final points"
		return final_points,final_reversed_points

	## Computes the extrusion values from deck
	# @param deckE the extrusion values from extract deck
	def E(self,deckE):

		E=[]
		for i in range(0,len(deckE[0])):
			extrusion = float(deckE[0][i][1:])
			index = deckE[1][i]
			E.append([extrusion , index])
		return E

	## Computes the extrusion values for interpolated points
	## Interpolated E values are given the same index as the original destination point
	# @param E the extrusion values from Reverse class E method
	# @param points the points from points method
	# @param final_points the points from final_points method
	def final_E(self, E, points, final_points):
		j=0
		final_E = []
		for i in range(0,len(points)-1):
			if points[i][3]< E[j][1] < points[i+1][3]:
				for k,final_point in enumerate(final_points):
					if final_point[3]==points[i][3]:
						new_dist = distance(points[i-1],final_point)
						dist = distance(points[i-1],points[i])
						if j ==0:
							E_interpolate = [round((E[j][0])*(new_dist/dist),4),E[j][1]]
						else:
							E_interpolate = [round((E[j][0]-E[j-1][0])*(new_dist/dist)+E[j-1][0],4),E[j][1]]
						final_E.append(E_interpolate)
				j = j+1
		if j < len(E):
			if E[j][1] > points[-1][3]:
				for k,final_point in enumerate(final_points):
					if final_point[3]==points[-1][3]:
						new_dist = distance(points[-2],final_point)
						dist = distance(points[-2],points[-1])
						E_interpolate = [round((E[j][0]-E[j-1][0])*(new_dist/dist)+E[j-1][0],4),E[j][1]]
						final_E.append(E_interpolate)

		return final_E

	## Calculates the new extrusion values for reversed toolpath by conserving the extrusion per length unit in planar toolpath
	# @param E The extrusion values list from E method
	# @param final_E The extrusion values list from final_E method
	# @param points The points from points method
	# @param final_points  The points from final_points method
	# @param final_reversed_points  The points from final_reversed_points method
	def final_reversed_E(self, E, final_E, points, final_points,final_reversed_points):

		final_reversed_E = []
		j=0

		for i,e in enumerate(final_E):
			for k in range(0,len(final_points)):
				if final_points[k-1][3]< e[1] <final_points[k][3]:
					dist=distance(final_points[k-2],final_points[k-1])
					new_dist = distance(final_reversed_points[k-2],final_reversed_points[k-1])
					if i ==0:
						final_reversed_e = round((e[0])*(new_dist/dist),4)
					else:
						final_reversed_e = round(((new_dist * (e[0] -final_E[i-1][0] ) / dist) + final_E[i-1][0]),4)
					final_reversed_E.append([final_reversed_e , e[1]])
					break

		# for the last layers E
		s= 0
		while final_E[s][1] < final_points[-1][3]:
			s= s+1
			if s ==len(final_E):
				s = s-1
				break
		while final_E[s][1] > final_points[-1][3]:
			if final_points[j][3]==final_points[-1][3]:
				new_dist = distance(final_reversed_points[j-1],final_reversed_points[j])
				dist = distance(final_points[j-1],final_points[j])
				E_interpolate = [round((final_E[s][0]-final_E[s-1][0])*(new_dist/dist)+final_E[s-1][0],4),final_E[s][1]]
				final_reversed_E.append(E_interpolate)
				j = j+1
				if s+1 <= len(final_E)-1:
					s = s+1
				else:
					break
			else:
				j = j+1
		assert len(final_reversed_E)==len(final_E),"Length of final E and final reversed E dont match"
		return final_reversed_E

	## Modifies the deck from the extract class to include changes made by reverse transformation
	# @param deck The deck from extract class
	# @param final_reversed_E The extrusion values list from final_reversed_E method
	# @param final_points  The points from final_points method
	# @param final_reversed_points  The points from final_reversed_points method
	def modify_deck(self,deck,final_reversed_E, final_points,final_reversed_points):
		#Applies changes of coordinates
		modified_deck = deck.copy()
		Xmatches=['X'+str(point[0]) for point in final_reversed_points]
		Ymatches=['Y'+str(point[1]) for point in final_reversed_points]
		Zmatches=['Z = '+str(point[2]) for point in final_reversed_points]
		Line_startindices=[point[3] for point in final_reversed_points]
		modified_deck['X'] = [Xmatches,Line_startindices]
		modified_deck['Y'] = [Ymatches,Line_startindices]
		modified_deck['layers'] = [Zmatches,Line_startindices]

		#Applies changes for G values in deck
		for i,point in enumerate(final_points):
			for final_point in final_reversed_points:
				if point[3] == final_point[3] and point != final_point:
					modified_deck['G'][0].insert(i+1,deck['G'][0][i])
					modified_deck['G'][1].insert(i+1,deck['G'][1][i])
		assert len(modified_deck['G'][0])==len(final_reversed_points), "Length of G values not equal to length of final points"

		#Applies changes for E values in deck
		deckE = ['E'+str(E[0]) for E in final_reversed_E]
		deckindices = [E[1] for E in final_reversed_E]
		modified_deck['E'] = [deckE,deckindices]
		return modified_deck

	## Generates the IO status for every point, 1 if extrusion takes place, 0 otherwise
	# @param points the points from points method
	# @param final_reversed_points the points from final_reversed_points method
	# @param E the extrusion values from Reverse class E method
	# @param indices_to_keep Indicies of the distance checked points, from the distance check method
	def IO(self, points, final_reversed_points, E, indices_to_keep):

		j=0
		IO=[0]*len(final_reversed_points)
		one_indices = []
		for i in range(0,len(points)-1):
			if points[i][3]<E[j][1]<points[i+1][3]:
				one_indices.append(points[i][3])
				j+=1
		for one_index  in one_indices:
			for i in range(0,len(final_reversed_points)-1):
				if final_reversed_points[i][3] == one_index:
					IO[i]=1
		IO=[x for i,x in enumerate(IO) if i in indices_to_keep]
		return IO

	## Regenerates a new deck using Generate class methods
	# @param deck The modified deck from modify_deck method
	# @param yaml_deck The deck from YAML class
	# @param points The points from points method
	# @param final_reversed_points The points from final_reversed_points method
	# @param E The extrusion values from E method
	def regenerate(self,deck,yaml_deck, points, final_reversed_points, E):

		X = [point[0] for point in final_reversed_points]
		Y = [point[1] for point in final_reversed_points]
		Z = [point[2] for point in final_reversed_points]

		self.coordinates = zip(X,Y,Z)

		## Coordinates of the points that passed the distance check calculation
		self.distance_checked_coord=Gen.DistanceCheck(self,self.coordinates,yaml_deck['dist_min'])[0]

		## Indices of the points that passed the distance check calculation
		self.indices_to_keep=Gen.DistanceCheck(self,self.coordinates,yaml_deck['dist_min'])[1]

		## Modified G status, adapted for the fisnar
		self.mod_G=Gen.modG(self,deck['G'],deck['sublayers'],deck['end_index'],self.indices_to_keep)

		## Extruder in use for every point
		self.T=Gen.T(self,deck['X'],deck['Y'],deck['T'],deck['end_index'],self.indices_to_keep,yaml_deck['slicer'])

		## Mutlimaterial Fisnar status
		self.fisnar_status=Gen.status(self,self.T)

		## Reverse class method for Fisnar IO: 0 if no extrusion, 1 otherwise
		self.IO=Reverse.IO(self, points, final_reversed_points, E, self.indices_to_keep)

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
