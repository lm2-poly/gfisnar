#-*- coding: utf-8 -*-
#@author: aziz-yamar.gueye@polyml.ca

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import pdb

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

	## Stores the X Y Z Coordinates for each layer
    # @param extract_deck The deck from extract class
    # @param final_reversed_points the points from Reverse method
    def layer_coordinates(self, extract_deck, final_reversed_points):
        layers = extract_deck['layers']
        plots = []
        for layer_index in range(0,len(layers[1])-1):
            for (x,y,z,i) in final_reversed_points:
                if layers[1][layer_index]< i <layers[1][layer_index+1]:
                    plot = [x,y,z,layer_index]
                    plots.append(plot)
                if layer_index == len(layers[0])-1:
                    if layers[1][layer_index] < i:
                        plot = [x,y,z,layer_index]
                        plots.append(plot)
        return plots

	## Plots the layer that has been specified
    # @param layer_to_plot the layer to plot
    # @param plots coordinates from layer_coordinates method
    def layer_plot(self,layer_to_plot,plots):
        fig2 = plt.figure()
        ax2 = fig2.add_subplot(111,projection='3d')

        x = [point[0] for point in plots if point[3] == layer_to_plot-1]
        y = [point[1] for point in plots if point[3] == layer_to_plot-1]
        z = [point[2] for point in plots if point[3] == layer_to_plot-1]

        ax2.plot3D(x,y,z)
        ax2.set_xlabel('x')
        ax2.set_ylabel('y')
        ax2.set_zlabel('z');
        plt.show()
        return fig2
