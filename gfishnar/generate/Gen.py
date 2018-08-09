# -*- coding: utf-8 -*-
import math
import sys
class Gen():

	def __init__(self,deck,yaml_deck):

		self.Z=Gen.Zcoord(self,deck['X'],deck['Y'],deck['layers'],deck['end_index'])

		self.coordinates=Gen.coordinates(self,deck['X'],deck['Y'],self.Z)

		self.distance_checked_coord=Gen.DistanceCheck(self,self.coordinates,yaml_deck['dist_min'])[0]

		self.indices_to_keep=Gen.DistanceCheck(self,self.coordinates,yaml_deck['dist_min'])[1]

		self.mod_G=Gen.modG(self,deck['G'],deck['sublayers'],deck['end_index'],self.indices_to_keep)

		self.T=Gen.T(self,deck['X'],deck['Y'],deck['T'],deck['end_index'])

		self.fisnar_status=Gen.status(self,self.T,self.indices_to_keep)

		self.speed=Gen.speed(self,self.mod_G,self.distance_checked_coord,
			yaml_deck['travel_speed'],yaml_deck['print_speed'])[0]

		self.mod_G_to_keep=Gen.speed(self,self.mod_G,self.distance_checked_coord,
			yaml_deck['travel_speed'],yaml_deck['print_speed'])[1]

		
		self.rotation=Gen.rotation(self,self.distance_checked_coord,yaml_deck['rotation_angle'])

		self.deck={'status':self.fisnar_status
		,'coord_to_keep':self.distance_checked_coord
		,'indices_to_keep':self.indices_to_keep
		,'mod_G_to_keep':self.mod_G_to_keep
		,'Speed':self.speed
		,'rotation':self.rotation
		,'extruder':self.T
	}

	def Zcoord(self,X,Y,layers,end_index):
		'''gets the height of every print point'''
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

	def T(self,X,Y,extruder,end_index):
		'''appends which extruder in use for every print point'''
		i=0
		T=[]
		for j in range(0,len(extruder[0])):
			while X[1][i]<extruder[1][j]:
				T.append(extruder[0][j-1])
				i=i+1
			if X[1][i]>extruder[1][-1]: #for the last layer
				for k in range(i,len(X[0])):
					T.append(extruder[0][-1])
		if len(T)!=len(X[0]):
			print 'X and T coordinates does not match'
		if len(T)!=len(Y[0]):
			print 'Y and T coordinates does not match'
		return T

	def coordinates(self,X,Y,Z):
		'''Groups the coordinates of every point'''
		XCor=[float(x[1:]) for x in X[0]]
		YCor=[float(x[1:]) for x in Y[0]]
		ZCor=[float(x[4:]) for x in Z]
		return zip(XCor,YCor,ZCor)

	def DistanceCheck(self,coordinates,min_dist):
		i=0
		indices_to_remove=[]
		while i<(len(coordinates)-1):

			dist=math.sqrt((coordinates[i+1][0]-coordinates[i][0])**2
					+(coordinates[i+1][1]-coordinates[i][1])**2
					+(coordinates[i+1][2]-coordinates[i][2])**2)
			j=i
<<<<<<< HEAD
			print'i=j=',i
			print 'premier calcul dist=',dist
=======
			print 'premier calcul dist=',dist
			print'i=j=',i
>>>>>>> 7b00c303acfb88904442bfa4c572615a03e2f862
			if dist>min_dist:
				i=i+1
				last_i=i
			else:
				while dist<min_dist:
					j=j+1
					print'entre dans while j=',j
					if j+1>=len(coordinates)-1:
						for k in range(last_i,len(coordinates)):
							indices_to_remove.append(k)
							print 'on enleve',k
						dist=min_dist+1
						i=k #quits the loop
					else:
						indices_to_remove.append(j)
<<<<<<< HEAD
						print 'point',j,'is removed'
=======
>>>>>>> 7b00c303acfb88904442bfa4c572615a03e2f862
						dist=math.sqrt((coordinates[j+1][0]-coordinates[i][0])**2
							+(coordinates[j+1][1]-coordinates[i][1])**2
							+(coordinates[j+1][2]-coordinates[i][2])**2)
						if dist>min_dist:
								i=j+1
								last_i=i

		indices_to_keep=[i for i,x in enumerate(coordinates) if i not in indices_to_remove]
		new_coord=[x for i,x in enumerate(coordinates) if i in indices_to_keep]
		D=[]
		for i in range(0,len(new_coord)-1):
			dist=math.sqrt((new_coord[i+1][0]-new_coord[i][0])**2
					+(new_coord[i+1][1]-new_coord[i][1])**2
					+(new_coord[i+1][2]-new_coord[i][2])**2)
			D.append(dist)
		print 'minimal distance=',min(D)
		if dist<min_dist:
<<<<<<< HEAD
			print dist,'distance chek failed : points too close'
=======
			print dist,'erreur distance trop petite'
>>>>>>> 7b00c303acfb88904442bfa4c572615a03e2f862

		return new_coord,indices_to_keep

	def modG(self,G,sublayers,end_index,indices_to_keep):
		'''modifies the G status from the Gcode to match the Fishnar G status'''  
		#si sublayer est support mettre G0:
		value = 'support'
		#finds the indicies of 'support' in the sublayer list:
		indices_in_sublayer = [i for i, x in enumerate(sublayers[0]) if x == value]
		indices_end=[i+1 for i in indices_in_sublayer]
		#finds the start Gcode indicies of the sublayer  to modify :
		limit1= [x for i,x in enumerate(sublayers[1]) if i in indices_in_sublayer]
		#finds the end Gcode indicies of the sublayer to modify:
		limit2= [x for i,x in enumerate(sublayers[1]) if i in indices_end]
		#if there is no 'support' the list indices will be empty:
		mod_G=list(G[0]) #pour avoir une copie de G sans alterer l'object G si on ecrit mod_G=G
		if len(indices_in_sublayer)==0:
			mod_G= mod_G # ne rien changer
		else:
			#if the last sublayer is support, we add the end_index to limit2:
			if max(indices_end)>(len(sublayers[1])-1): #-1 car commence par 0
				limit2.append(end_index)
			for i in range(0,len(limit1)):#de 0 à len-1
				G_indices_to_modify=[index for index,x in enumerate(G[1]) if limit1[i]<x<limit2[i]]
				for i in G_indices_to_modify:
					mod_G[i]='G0'

		#si on trouve G0 ecrit au milieu toute la sublayer devient G0:
		G0_indices= [index for index,x in enumerate(G[0]) if x=='G0']
		G0_limit1=[x for i,x in enumerate(G[1]) if i in G0_indices]
		G0_limit2=[]
		for i in range(0,len(G0_limit1)):
			if G0_limit1[i]>max(sublayers[1]): #last element of sublayers
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

		mod_G=[x for i,x in enumerate(mod_G) if i in indices_to_keep]

		return mod_G

	def status(self,T_brut,indices_to_keep):
		'''generates the fishnar multimaterial printing status'''
		status=[]
		T=[x for i,x in enumerate(T_brut) if i in indices_to_keep]
		for i in range(0,len(T)):
			if i==0: #first point printed
				status.append('MultiCPStartPoint')
			elif i==len(T)-1: #last point printed
				status.append('MultiCPEndPoint')
			elif (T[i]=='T1' and T[i+1]=='T0')|(T[i]=='T0' and T[i+1]=='T1'):
				status.append('MultiCPEndPoint')
			elif T[i]=='T0':
				status.append('D01LinePassing')
			elif T[i]=='T1':
				status.append('D02LinePassing')
		# a start point always follows an endPoint inside the G-CODE:
		for i in range(1,len(T)-2):
			if status[i]=='MultiCPEndPoint':
				status[i+1]='MultiCPStartPoint'

		return status

	def speed(self,mod_G,distance_checked_coord,travel_speed,print_speed):
		speed=[]
		for i in range(0,len(mod_G)):
			if mod_G[i]=='G0':
				speed.append(travel_speed)
			else:
				speed.append(print_speed)

		return speed,mod_G

	def rotation(self,Coord_to_keep,angle):
		Rotation=[angle]*len(Coord_to_keep)
		return Rotation





