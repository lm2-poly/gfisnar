#-*- coding: utf-8 -*-
#@author: soufiane.hifdi@polyml.ca
import math
import sys

## Class to generate all the inputs for the fisnar using the attributes of the extract class and yaml class
class Gen():

	## Constructor
    # @param deck The deck of the extract class
    # @param yaml_deck The deck of the yaml class
	def __init__(self,deck,yaml_deck):

		## Z coordinate of every point
		self.Z=Gen.Zcoord(self,deck['X'],deck['Y'],deck['layers'],deck['end_index'])

		## Tuple regrouping the X,Y and Z coordinates
		self.coordinates=Gen.coordinates(self,deck['X'],deck['Y'],self.Z)

		## Coordinates of the points that passed the distance check calculation
		self.distance_checked_coord=Gen.DistanceCheck(self,self.coordinates,yaml_deck['dist_min'])[0]

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

	##  Appends the Z coordinate to every point 
    # @param X X coordinates from the extract class deck
    # @param Y Y coordinates from the extract class deck
    # @param end_index End index from the extract class deck
	def Zcoord(self,X,Y,layers,end_index):
		i=0
		Z=[]
		for j in range(0,len(layers[0])):
			while X[1][i]<layers[1][j]:
				Z.append(layers[0][j-1])
				i=i+1
			if X[1][i]>layers[1][-1]: #for the last layer
				for k in range(i,len(X[0])):
					Z.append(layers[0][-1])
		if len(Z)!=len(X[0]):
			print 'X and Z coordinates does not match'
		if len(Z)!=len(Y[0]):
			print 'Y and Z coordinates does not match'
		return Z

	##  appends the extruder in use T0 or T1 to every point 
    # @param X X coordinates from the extract class deck
    # @param Y Y coordinates from the extract class deck
    # @param end_index End index from the extract class deck
    # @param indices_to_keep Indices of the points that passed the distance check calculation
	def T(self,X,Y,extruder,end_index,indices_to_keep):
		i=0
		T=[]
		for j in range(0,len(extruder[0])):
			while X[1][i]<extruder[1][j]:
				T.append(extruder[0][j-1])
				i=i+1
			# for the last layer
			if X[1][i]>extruder[1][-1]:
				for k in range(i,len(X[0])):
					T.append(extruder[0][-1])
		if len(T)!=len(X[0]):
			print 'X and T coordinates does not match'
		if len(T)!=len(Y[0]):
			print 'Y and T coordinates does not match'

		T_to_keep=[x for i,x in enumerate(T) if i in indices_to_keep]

		return T_to_keep

	## Groups the X,Y,Z in a tuple 
    # @param X X coordinates from the extract class deck
    # @param Y Y coordinates from the extract class deck
    # @param Y Z coordinates from the Zcoord method
	def coordinates(self,X,Y,Z):
		'''Groups the coordinates of every point'''
		XCor=[float(x[1:]) for x in X[0]]
		YCor=[float(x[1:]) for x in Y[0]]
		ZCor=[float(x[4:]) for x in Z]
		return zip(XCor,YCor,ZCor)

	## Checks the distance between consecutive points and removes points that are too close for the Fisnar
    # @param coordinates Coordinates from the coordinates method
    # @param min_dist Minimal distance specified from the YAML class deck
	def DistanceCheck(self,coordinates,min_dist):
		i=0
		indices_to_remove=[]
		# Calculates distance between consecutive points
		while i<(len(coordinates)-1):

			dist=math.sqrt((coordinates[i+1][0]-coordinates[i][0])**2
					+(coordinates[i+1][1]-coordinates[i][1])**2
					+(coordinates[i+1][2]-coordinates[i][2])**2)
			j=i
			# If the distance is greater than the minimal distance, checks the next distance
			if dist>min_dist:
				i=i+1
				# Last satifactory distance
				last_i=i
			else:
				# While the distance is inferior than the minimal distance, removes the point and checks the distance again  
				while dist<min_dist:
					j=j+1
					# If the last distance is inferior than the minimal distance, remove all the points past the last satisfactory distance
					if j+1>=len(coordinates)-1:
						for k in range(last_i,len(coordinates)):
							indices_to_remove.append(k)
						# Quits the loop
						dist=min_dist+1
						i=k 
					else:
						indices_to_remove.append(j)
						dist=math.sqrt((coordinates[j+1][0]-coordinates[i][0])**2
							+(coordinates[j+1][1]-coordinates[i][1])**2
							+(coordinates[j+1][2]-coordinates[i][2])**2)
						if dist>min_dist:
								i=j+1
								# Last satisfactory distance
								last_i=i
		# determines what indices too keep
		indices_to_keep=[i for i,x in enumerate(coordinates) if i not in indices_to_remove]
		# Gives the coordinates corresponding to the indices to keep
		new_coord=[x for i,x in enumerate(coordinates) if i in indices_to_keep]
		D=[]
		# Calculates the distance between the new coordinates, print the minimal distance
		for i in range(0,len(new_coord)-1):
			dist=math.sqrt((new_coord[i+1][0]-new_coord[i][0])**2
					+(new_coord[i+1][1]-new_coord[i][1])**2
					+(new_coord[i+1][2]-new_coord[i][2])**2)
			D.append(dist)
		# If some points are too close the system will exit
		if dist<min_dist:
			print dist,'distance chek failed : points too close'
			sys.exit(1)
		else :
			print 'distance check passed'

		return new_coord,indices_to_keep

	## Modifies the G status from the Gcode to match the status of the fisnar
    # @param sublayers Sublayers printed, from the extract class deck
    # @param end_index End index of the gcode from the extract class deck
    # @param indices_to_keep Indicies of the distance checked points, for the distance check method
	def modG(self,G,sublayers,end_index,indices_to_keep):
		# If a sublayer is support,the G status of the sublayer is set to G0:
		value = 'support'
		# Finds the indicies of 'support' in the sublayer list:
		indices_in_sublayer = [i for i, x in enumerate(sublayers[0]) if x == value]
		indices_end=[i+1 for i in indices_in_sublayer]
		# Finds the start Gcode indicies of the sublayers to modify :
		limit1= [x for i,x in enumerate(sublayers[1]) if i in indices_in_sublayer]
		# Finds the end Gcode indicies of the sublayers to modify:
		limit2= [x for i,x in enumerate(sublayers[1]) if i in indices_end]
		# If there is no 'support' the list indices will be empty:
		mod_G=list(G[0]) 
		if len(indices_in_sublayer)==0:
			mod_G= mod_G
		else:
			# If the last sublayer is support, we add the end_index, to limit2:
			if max(indices_end)>(len(sublayers[1])-1):
				limit2.append(end_index)
			for i in range(0,len(limit1)):
				G_indices_to_modify=[index for index,x in enumerate(G[1]) if limit1[i]<x<limit2[i]]
				for i in G_indices_to_modify:
					mod_G[i]='G0'

		# If a G0 is written in the middle of a sublayer, the sublayer is set to G0
		G0_indices= [index for index,x in enumerate(G[0]) if x=='G0']
		G0_limit1=[x for i,x in enumerate(G[1]) if i in G0_indices]
		G0_limit2=[]
		for i in range(0,len(G0_limit1)):
			if G0_limit1[i]>max(sublayers[1]):
				G0_limit2.append(end_index)
			else:
				limit3 = [x for index,x in enumerate(sublayers[1]) if x>G0_limit1[i]]
				limit3 = min(limit3)
				G0_limit2.append(limit3)

		for i in range(0,len(G[1])):
			for j in range(0,len(G0_limit1)):
				if G0_limit1[j]<=G[1][i]<=G0_limit2[j]:
					mod_G[i]='G0'

		if len(mod_G)!=len(G[0]):
			print 'Modified G status length does not match points matrix length'

		# Keeps only the G for the points that passed the distance check
		mod_G=[x for i,x in enumerate(mod_G) if i in indices_to_keep]

		return mod_G

    ## Generates the fishnar multimaterial printing status 
    # @param T Extruder in use for every point, from the extract class deck
	def status(self,T):
		status=[]
		for i in range(0,len(T)):
			if i==0:
				status.append('MultiCPStartPoint')
			elif i==len(T)-1: 
				status.append('MultiCPEndPoint')
			elif (T[i]=='T1' and T[i+1]=='T0')|(T[i]=='T0' and T[i+1]=='T1'):
				status.append('MultiCPEndPoint')
			elif T[i]=='T0':
				status.append('D01LinePassing')
			elif T[i]=='T1':
				status.append('D02LinePassing')

		for i in range(1,len(T)-2):
			if status[i]=='MultiCPEndPoint':
				status[i+1]='MultiCPStartPoint'

		return status

	## Generates the IO status for every point, 1 if extrusion takes place, 0 otherwise
	# @param X X coordinates from the extract class deck
	# @param E E matches from the extract class deck
    # @param indices_to_keep Indicies of the distance checked points, for the distance check method
	def IO(self,X,E,indices_to_keep):
		j=0
		IO=[0]*len(X[1])
		for i in range(0,len(X[1])-1):
			if X[1][i]<E[1][j]<X[1][i+1]:
				IO[i]=1
				j+=1
			else:
				IO[i]=0

		IO=[x for i,x in enumerate(IO) if i in indices_to_keep]

		return IO

	## Generates the speed for every point
	# @param mod_G Modified G status given by the mod_G function 
	# @param travel_speed Travel speed from the YAML deck
    # @param print_speed Print speed from the YALM deck
    # @param IO IO, extrusion status given by the IO method
	def speed(self,mod_G,travel_speed,print_speed,IO):
		speed=[]

		for i in range(0,len(IO)):
			if IO[i]==0:
				speed.append(travel_speed)
			else:
				speed.append(print_speed)

		return speed,mod_G

	## Generates the speed for every point
	# @param Coord_to_keep distance checked coordinates as given by the distance check method 
	# @param angle Rotation angle from the YAML deck
	def rotation(self,Coord_to_keep,angle):
		Rotation=[angle]*len(Coord_to_keep)
		return Rotation





