#! /usr/bin/env python
#
# Version 0.9  (HS 09/03/2020)
#
import numpy as np
import scipy.io


if __name__ == "__main__":
    #                 A                 B                   C                   D
    polyA = np.array([[1.65241, 2.222], [1.92806, 1.71377], [2.51323, 2.1643], [2.35589, 2.73902]])

    #Layer 1
    # the 4 neurons in the 1st layer test weather a point is ahead or behind of each face of the polygon
    directions = polyA - polyA[[1,2,3,0],:]
    normals = directions[:,[1,0]] * np.array([[-1,1]])

    biases = np.sum(normals*polyA,axis=1)[:,None] * -1
    weightsMatrix1 = np.concatenate((biases,normals),axis=1)
    # normalize the weights

    weightsMatrix1 /= np.max(np.abs(weightsMatrix1),axis=1)[:,None]

    #Layer 2

    # The 4D XOR neuron
    # this neuron only returns 1 if all the previous neurons return a 0, meaning the point is not outside any faces

    # any presence in the x vector other than 0 will add a value > -1 meaning the output is 0
    # only all 4 zeros will output a 1
    weightsMatrix2 = np.array([[1,-1,-1,-1,-1]])

    f = open("task2 hNN A weights.txt",'x')

    L1Neurons,L1Dim = weightsMatrix1.shape
    for j in range(L1Neurons):
        for i in range(L1Dim):
            f.write("W(1,"+str(j+1)+','+str(i)+") : " + str(weightsMatrix1[j,i])+'\n')

    L2Neurons,L2Dim = weightsMatrix2.shape
    for j in range(L2Neurons):
        for i in range(L2Dim):
            f.write("W(2,"+str(j+1)+','+str(i)+") : " + str(weightsMatrix2[j,i])+'\n')

def t2():
    # poly 2.1
    PolyB = np.array([[-0.46478,3.19731], [5.65146,4.97528], [3.08446, 2.35946]]) #, [3.68124, -2.26483]
    directionsB = PolyB[[1,2,0],:] - PolyB
    normalsB = directionsB[:,[1,0]] * np.array([[-1,1]])

    biasesB = np.sum(normalsB*PolyB,axis=1)[:,None] * -1
    weightsMatrix1B = np.concatenate((biasesB,normalsB),axis=1)
    # normalize the weights

    weightsMatrix1B /= np.max(np.abs(weightsMatrix1B),axis=1)[:,None]
    print(weightsMatrix1B)

def t22():
    # poly 2.2
    PolyB = np.array([[3.08446, 2.35946],[3.68124, -2.26483],[-0.46478,3.19731]])
    directionsB = PolyB[[1,2,0],:] - PolyB
    normalsB = directionsB[:,[1,0]] * np.array([[-1,1]])

    biasesB = np.sum(normalsB*PolyB,axis=1)[:,None] * -1
    weightsMatrix1B = np.concatenate((biasesB,normalsB),axis=1)
    # normalize the weights

    weightsMatrix1B /= np.max(np.abs(weightsMatrix1B),axis=1)[:,None]
    print(weightsMatrix1B)