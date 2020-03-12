import math
import graph
import random
import sys
import os
import matplotlib.pyplot as plt

# tests the heuristics on metric graphs
def testHeuristics(n):
    averages = [0,0,0,0]
    names = ["swap","twoopt","greedy","EPICHeuristic"]
    for i in range(n):
        print("Iteration: " + str(i))
        print(averages)
        filename  = "graphs/test_"+str(n)
        g = graph.Graph(-1,filename)
        
        # swap
        g.swapHeuristic()
        averages[0] += (g.tourValue())
        g.resetPerm()

        # two-opt
        g.TwoOptHeuristic()
        averages[1] += (g.tourValue())
        g.resetPerm()  

        # greedy
        g.Greedy()
        averages[2] += (g.tourValue())
        g.resetPerm() 

        # EPIC
        g.EPICHeuristic(0.8)
        averages[3] += (g.tourValue())
        
    averages = [x/n for x in averages] 
    print([names[i] + ":" + str(x) for (i,x) in enumerate(averages)])
    return averages

# writes n files with random graphs with random sizes,and widths (test_1,test_2,test_3.. etc)
# -1 on argument indicates random
def generateTestGraphs(n,sizes):
    for i in range(n):
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
    testHeuristics(49)