import math
import graph
import random
import sys
import os
import matplotlib.pyplot as plt
import numpy as np



# tests the heuristics on the graphs in the graphs older given by the indices 
def testHeuristics(indices,p1,p2,p3):
    heuristics = ["swap","twoopt","greedy","custom"]
    results = np.zeros((len(indices),len(heuristics)))
    tours = [[[]]]
    for i in range(len(indices)):
        print("Iteration: " + str(i))
        filename  = "graphs/test_"+str(indices[i])
        g = graph.Graph(-1,filename)
        

        currTours = []
        # swap
        g.swapHeuristic()
        results[i,0] = (g.tourValue())
        currTours.append(g.perm)
        g.resetPerm()

        # two-opt
        g.TwoOptHeuristic()
        results[i,1] = (g.tourValue())
        currTours.append(g.perm)
        g.resetPerm()  

        # greedy
        g.Greedy()
        results[i,2] = (g.tourValue())
        currTours.append(g.perm)
        g.resetPerm() 

        # EPIC
        g.EPICHeuristic(p1,p2,p3)
        results[i,3] = (g.tourValue())
        currTours.append(g.perm)

        tours.append(currTours)
    return (results,tours)
def loadEuclidianGraph(filename):
    f = open(filename,'r')

    X = []
    Y = []
    point = f.readline().strip().split()
    while point != []:
        x,y = point
        X.append(float(x))
        Y.append(float(y))
        point = f.readline().strip().split()
    return (X,Y)

def plotTSP(X,Y,permutation=[],color='b',drawPoints=True):
    # we make sure we, loop around

    ordX = [None] * (len(X) + 1)
    ordY = [None] * (len(Y) + 1)
    if permutation == []:
        ordX = X
        ordY = Y
    else: 
        permutation.append(permutation[0])

        for i,p in enumerate(permutation):
            ordX[i] = X[p]
            ordY[i] = Y[p]
            plt.annotate(str(p),(X[p]-0.5,Y[p]-0.5))

    sequenceColors = ['k' for x in range(len(X))]
    sequenceColors[0] = 'r'
    sequenceColors[1] = 'y'
    sequenceColors[-1] = 'b'
    if drawPoints:
        plt.scatter(ordX[0:-1],ordY[0:-1],c=sequenceColors, zorder=1)
        
    if permutation != []:
        plt.plot(ordX,ordY,color,zorder=0)

# writes files with random graphs with random sizes,and widths (test_n[0],test_n[2],test_n[3].. etc)
# -1 on argument indicates random
def generateTestGraphs(n,sizes):
    for i in n:
        nodes = sizes[i]
        width = nodes * 2
        try:
            randomUniformGraph("graphs/test_" + str(i),nodes,width)
        except:
            continue        

# generates random square metric TSP graph, writes it to filename and returns the points
def randomUniformGraph(filename,n,width):
    
    f = open(filename,'x')
    points = set()
    
    while len(points) < n:
        x = int(random.random() * width)
        y = int(random.random() * width)
        points.add((x,y))

    for (x,y) in points:
        f.write(str(x) + " " + str(y) + os.linesep)
    return points

if __name__ == "__main__":
    g = graph.Graph(-1,"graphs/test_1")
    g.EPICHeuristic(1000,1,0.5)
    p = g.perm

    X,Y = loadEuclidianGraph("graphs/test_1")
    
    plotTSP(X,Y,p,'k')
    print(g.tourValue())
    g.resetPerm()
    g.TwoOptHeuristic()
    print("TwoOpt:",g.tourValue())
    #plotTSP(X,Y,g.perm,'b--',False)
    plt.show()
def randomUniformGraphKnownOptimal(filename,n,width,optimal):
    return null