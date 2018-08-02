# -*- coding: utf-8 -*-

class Calibrate():

	def __init__(self,generated_deck,yaml_deck):

		self.coord=Calibrate.coord(self,generated_deck['coord_to_keep'],
			generated_deck['mod_G_to_keep'],
			yaml_deck['X_init'],yaml_deck['Y_init'],yaml_deck['Z_init'],
			yaml_deck['X_trans'],yaml_deck['Y_trans'])


	def coord(self,distance_checked_coordinates,mod_G,X_init,Y_init,Z_init,X_trans,Y_trans):
		Xfishnar=[]
		Yfishnar=[]
		Zfishnar=[]
		for i in range(0,len(distance_checked_coordinates)):
			X= distance_checked_coordinates[i][0]+X_init-distance_checked_coordinates[0][0]
			Xfishnar.append(X)
			Y=distance_checked_coordinates[i][1]+Y_init-distance_checked_coordinates[0][1]
			Yfishnar.append(Y)
			Z= -(distance_checked_coordinates[i][2])+Z_init
			Zfishnar.append(Z)

			if mod_G[i]=='G0':
				Xfishnar[i]+=X_trans
				Yfishnar[i]+=Y_trans

		return zip(Xfishnar,Yfishnar,Zfishnar)