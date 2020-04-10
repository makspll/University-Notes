#! /usr/bin/env python
#
# Version 0.9  (HS 09/03/2020)
#
import numpy as np
import scipy.io
import matplotlib.pyplot as plt
import task2_sNN_AB as t2

# no of points is the square of the width of the graph
width = 1000

#calculate mesh
xs = np.linspace(-3,6,num=width)
ys = np.linspace(-3,6,num=width)

pointsX,pointsY = len(xs),len(ys)

X,Y = np.meshgrid(xs,ys)

# 2-by-width-by-width
coordinate_grid = np.stack((X.ravel(), Y.ravel()),axis=1)
Z = t2.task2_sNN_AB(coordinate_grid).reshape(pointsX,pointsY)
fig,ax = plt.subplots(1)
plt.xlim(-3,6)
plt.ylim(-3,6)
plt.gca().set_aspect('equal',adjustable='box')
ax.contourf(X,Y,Z,levels=1,colors=['w','r'])

ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("Decision Boundaries with sneurons")
plt.show()