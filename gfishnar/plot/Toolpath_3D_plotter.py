#-*- coding: utf-8 -*-
#@author: aziz-yamar.gueye@polyml.ca

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

## Class to plot toolpath
class Toolpath_3D_plotter():

	## Constructor
    # @param coordinates The coordinates to plot ; list of points XYZ
    def __init__(self,coordinates):
        fig = plt.figure()
        ax1 = fig.add_subplot(111,projection='3d')

        x = [point[0] for point in coordinates]
        y = [point[1] for point in coordinates]
        z = [point[2] for point in coordinates]

        ax1.plot3D(x,y,z)
        ax1.set_xlabel('x')
        ax1.set_ylabel('y')
        ax1.set_zlabel('z');
        plt.show()
