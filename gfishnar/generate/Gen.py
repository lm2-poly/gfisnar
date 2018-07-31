# -*- coding: utf-8 -*-
import math

class Gen():

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

	def coordinates(self,X,Y,Z):
		'''Groups the coordinates of every point'''
		XCor=[float(x[1:]) for x in X[0]]
		YCor=[float(x[1:]) for x in Y[0]]
		ZCor=[float(x[4:]) for x in Z]
		return zip(XCor,YCor,ZCor)

	def distance(self,coordinates,min_dist):
		''' calculates the distance between consecutive points in the G-code'''
		D=[]
		for i in range(0,len(coordinates)-1):
			dist=math.sqrt((coordinates[i+1][0]-coordinates[i][0])**2
				+(coordinates[i+1][1]-coordinates[i][1])**2
				+(coordinates[i+1][2]-coordinates[i][2])**2)
			dist=abs(dist)
			D.append(dist)
		distance_indices_to_keep=[i for i,x in enumerate(D) if D[i]>min_dist]
		distance_checked_coord=[x for i,x in enumerate(coordinates) if i in distance_indices_to_keep]
		#if the last distance check is passed, append our last coord:
		if max(distance_indices_to_keep)==len(D)-1:
			distance_checked_coord.append(coordinates[-1])

		return distance_checked_coord

	def modG(self,G,sublayers,end_index):
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

		return mod_G

	def status(self,mod_G):
		'''generates the fishnar multimaterial printing status'''
		status=[]
		for i in range(0,len(mod_G)):
			if i==0: #first point printed
				status.append('MultiCPStartPoint')
			elif i==len(mod_G)-1: #last point printed
				status.append('MultiCPEndPoint')
			elif (mod_G[i]=='G1' and mod_G[i+1]=='G0')|(mod_G[i]=='G0' and mod_G[i+1]=='G1'):
				status.append('MultiCPEndPoint')
			elif mod_G[i]=='G1':
				status.append('D01LinePassing')
			elif mod_G[i]=='G0':
				status.append('D02LinePassing')
		# add Start point if we find and end point inside the G-CODE:
		for i in range(1,len(mod_G)-2):
			if status[i]=='MultiCPEndPoint':
				status[i+1]='MultiCPStartPoint'

		return status






