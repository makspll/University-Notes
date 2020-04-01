import math
import graph
import random
import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import time


if __name__ == "__main__":
    print("READ MY DEFINITION!")
    # to graph results they first need to be saved to appropriate files,
    # but to test the heuristics we first generate some graps like so:

    # GENERATING GRAPHS

    # generateTestGraphs(n,sizes,type=-1):
    # where n is an array of indices, for the test names, (test_n[0],test_n[1])
    # sizes being a list of graph sizes where test n[i] has size sizes[i]
    # type -1 is euclidian,0 is metric, 1 is non-metric
    # for example:
    #   generateTestGraphs([x for x in range(500)],[((x//5)*1)+1 for x in range(500)],-1)
    # is what I used to generate the euclidian test graphs

    # GENERATING RESULT FILES

    # Example of how result files were generated after test graphs were generated 

        # testName= "ER_s5+1n-10_1_0.5B"
        # os.makedirs(("results/" + testName), exist_ok=True)

        # (results,tours,times) = testHeuristics([x for x in range(500)],10,1,0.5,[-1 for x in range(500)])

        # np.savetxt('results/'+testName+'/results.csv',results,delimiter=',')
        # np.save('results/'+testName+'/tours.npy',tours,allow_pickle=True)
        # np.savetxt('results/'+testName+'/times.csv',times,delimiter=',')
    
    # GRAPHING DATA

    # to graph the data call any of the lambda functions defined above, or use the graphData function

# below are the functions used to graph some of the results
# this asumes there is data in a "results" folder where each subfolder is named as in the "set" variables
# within the subfolders there should be files named "results.csv", "times.csv" and "tours.npy" containing coma delimited tour values, runtimes and the permutations stored as a pickled npy object
# the folders are named with a rough convention where the first few letters are either ER,MR or NMR signalling the type of graphs the tests were performed on,
# the next symbols being something along the lines of "s5+1n"  meaning step of 5 node increase of 1, i.e. every 5 tests we increase graph size by 1,
# and then the 3 parameters for custom - for example "1_1_0" means 1 totOpts, 1 lookahead, 0 bias
# examples of how data is generated and graphed are above in the main function

#comparing all heuristics
title1 = "Performance of heuristics"

setA = ["ER_s5+1n-10_1_0.5"]
labelA = ["ER"]
setB = ["MR_s5+1n-10_1_0.5"]
labelB = ["MR"]
setC = ["NMR_s5+1n-10_1_0.5"]
labelC = ["NMR"]

testHeurs = lambda : graphData(setA+setB+setC,labelA + labelB + labelC,[0,1,2,3],title1,type=1,errbars=True)
testHeurs1 = lambda : graphData(setA,labelA,[0,1,2,3],title1,type=1)
testHeurs2 = lambda : graphData(setB,labelB,[0,1,2,3],title1,type=1)
testHeurs3 = lambda : graphData(setC,labelC,[0,1,2,3],title1,type=1)

testHeursSize = lambda : graphData(setA+setB+setC,labelA + labelB + labelC,[0,1,2,3],title1,type=2)
testHeursSize1 = lambda : graphData(setA,labelA,[0,1,2,3],title1,type=2)
testHeursSize2 = lambda : graphData(setB,labelB,[0,1,2,3],title1,type=2)
testHeursSize3 = lambda : graphData(setC,labelC,[0,1,2,3],title1,type=2)


testHeursRuntime =  lambda : graphData(setA+setB+setC,labelA + labelB + labelC,[0,1,2,3],title1,type=5,errbars=True)
testHeursRuntime1 =  lambda : graphData(setA,labelA,[0,1,2,3],title1,type=5,errbars=True)
testHeursRuntime2 =  lambda : graphData(setB,labelB,[0,1,2,3],title1,type=5,errbars=True)
testHeursRuntime3 =  lambda : graphData(setC,labelC,[0,1,2,3],title1,type=5,errbars=True)

#effects of changing opts
title2 = "Effects of changing number of 2-opt runs"

set1 = ["ER_s5+1n-0_1_0.5","ER_s5+1n-1_1_0.5","ER_s5+1n-2_1_0.5","ER_s5+1n-3_1_0.5","ER_s5+1n-4_1_0.5","ER_s5+1n-5_1_0.5","ER_s5+1n-10_1_0.5","ER_s5+1n-100_1_0.5","ER_s5+1n-1000_1_0.5","ER_s5+1n-10000_1_0.5"]
label1 = ["ER:0","ER:1","ER:2","ER:3","ER:4","ER:5","ER:10","ER:100","ER:1000","ER:10000"]
set2 = ["MR_s5+1n-0_1_0.5","MR_s5+1n-1_1_0.5","MR_s5+1n-2_1_0.5","MR_s5+1n-3_1_0.5","MR_s5+1n-4_1_0.5","MR_s5+1n-5_1_0.5","MR_s5+1n-10_1_0.5","MR_s5+1n-100_1_0.5","MR_s5+1n-1000_1_0.5","MR_s5+1n-10000_1_0.5"]
label2 = ["MR:0","MR:1","MR:2","MR:3","MR:4","MR:5","MR:10","MR:100","MR:1000","MR:10000"]
set12 =  ["MR_s5+1n-0_1_0.5","MR_s5+1n-1_1_0.5","MR_s5+1n-2_1_0.5","MR_s5+1n-3_1_0.5","MR_s5+1n-4_1_0.5","MR_s5+1n-5_1_0.5","MR_s5+1n-10_1_0.5","MR_s5+1n-100_1_0.5","MR_s5+1n-1000_1_0.5","MR_s5+1n-10000_1_0.5"]
label12 = ["NMR:0","NMR:1","NMR:2","NMR:3","NMR:4","NMR:5","NMR:10","NMR:100","NMR:1000","NMR:10000"]

testOpts = lambda : graphData(set1+set2+set12, label1 + label2 + label12,[3],title2,type=1)
testOpts1 = lambda : graphData(set1,label1,[3],title2,type=1)
testOpts2 = lambda : graphData(set2,label2,[3],title2,type=1)
testOpts3 = lambda : graphData(set12,label12,[3],title2,type=1)

testOptsSize = lambda : graphData(set1+set2+set12, label1 + label2 + label12,[3],title2,type=2)
testOptsSize1 = lambda : graphData(set1,label1,[3],title2,type=2)
testOptsSize2 = lambda : graphData(set2,label2,[3],title2,type=2)
testOptsSize3 = lambda : graphData(set12,label12,[3],title2,type=2)

testOptsRuntime = lambda : graphData(set1+set2+set12, label1 + label2 + label12,[3],title2,type=5)
testOptsRuntime1 = lambda : graphData(set1,label1,[3],title2,type=5)
testOptsRuntime2 = lambda : graphData(set2,label2,[3],title2,type=5)
testOptsRuntime3 = lambda : graphData(set12,label12,[3],title2,type=5)

#effects of changing bias
title3 = "Effect of changing bias"
set3 = ["ER_s5+1n-10_1_0","ER_s5+1n-10_1_0.1","ER_s5+1n-10_1_0.2","ER_s5+1n-10_1_0.3","ER_s5+1n-10_1_0.4","ER_s5+1n-10_1_0.5","ER_s5+1n-10_1_0.6","ER_s5+1n-10_1_0.7","ER_s5+1n-10_1_0.8","ER_s5+1n-10_1_0.9","ER_s5+1n-10_1_1"]
label3 = ["ER:0","ER:0.1","ER:0.2","ER:0.3","ER:0.4","ER:0.5","ER:0.5","ER:0.6","ER:0.7","ER:0.8","ER:0.9","ER:1"]
set4 = ["MR_s5+1n-10_1_0","MR_s5+1n-10_1_0.1","MR_s5+1n-10_1_0.2","MR_s5+1n-10_1_0.3","MR_s5+1n-10_1_0.4","MR_s5+1n-10_1_0.5","MR_s5+1n-10_1_0.6","MR_s5+1n-10_1_0.7","MR_s5+1n-10_1_0.8","MR_s5+1n-10_1_0.9","MR_s5+1n-10_1_1"]
label4 = ["MR:0","MR:0.1","MR:0.2","MR:0.3","MR:0.4","MR:0.5","MR:0.5","MR:0.6","MR:0.7","MR:0.8","MR:0.9","MR:1"]
set34 =  ["NMR_s5+1n-10_1_0","NMR_s5+1n-10_1_0.1","NMR_s5+1n-10_1_0.2","NMR_s5+1n-10_1_0.3","NMR_s5+1n-10_1_0.4","NMR_s5+1n-10_1_0.5","NMR_s5+1n-10_1_0.6","NMR_s5+1n-10_1_0.7","NMR_s5+1n-10_1_0.8","NMR_s5+1n-10_1_0.9","NMR_s5+1n-10_1_1"]
label34 = ["NMR:0","NMR:0.1","NMR:0.2","NMR:0.3","NMR:0.4","NMR:0.5","NMR:0.5","NMR:0.6","NMR:0.7","NMR:0.8","NMR:0.9","NMR:1"]

testBias = lambda : graphData(set3+set4+set34,label3 + label4+ label34,[3],title3,type=1)
testBias1 = lambda : graphData(set3,label3,[3],title3,type=1)
testBias2 = lambda : graphData(set4,label4,[3],title3,type=1)
testBias3 = lambda : graphData(set34,label34,[3],title3,type=1)

testBiasSize = lambda : graphData(set3+set4+set34,label3 + label4+ label34,[3],title3,type=2)
testBiasSize1 = lambda : graphData(set3,label3,[3],title3,type=2)
testBiasSize2 = lambda : graphData(set4,label4,[3],title3,type=2)
testBiasSize3 = lambda : graphData(set34,label34,[3],title3,type=2)

testBiasFullGreedy = lambda : graphData(["ER_s5+1n-10_1_0","ER_s5+1n-10_1_0.5"],["ER:0","ER:0.5"],[0,1,2,3],title3,type=1)
#effects of changing lookahead
title4 = "Effect of changing lookahead"

set5 = ["ER_s5+1n-10_1_0.5","ER_s5+1n-10_2_0.5","ER_s5+1n-10_3_0.5"]
label5 = ["ER:1","ER:2","ER:3"]
set6 = ["MR_s5+1n-10_1_0.5","MR_s5+1n-10_2_0.5","MR_s5+1n-10_3_0.5"]
label6 = ["MR:1","MR:2","MR:3"]
set7 = ["MR_s5+1n-10_1_0.5","MR_s5+1n-10_2_0.5","MR_s5+1n-10_3_0.5"]
label7 = ["NMR:1","NMR:2","NMR:3"]

testLookahead = lambda : graphData(set5+set6+set7,label5+label6+label7,[3],title4,type=1)
testLookahead1 = lambda : graphData(set5,label5,[3],title4,type=1)
testLookahead2 = lambda : graphData(set6,label6,[3],title4,type=1)
testLookahead3 = lambda : graphData(set7,label7,[3],title4,type=1)

testLookaheadSize = lambda : graphData(set5+set6+set7,label5+label6+label7,[3],title4,type=2)
testLookaheadSize1 = lambda : graphData(set5,label5,[3],title4,type=2)
testLookaheadSize2 = lambda : graphData(set6,label6,[3],title4,type=2)
testLookaheadSize3 = lambda : graphData(set7,label7,[3],title4,type=2)


testLookaheadRuntime = lambda : graphData(set5+set6+set7,label5+label6+label7,[3],title4,type=5)
testLookaheadRuntime1 = lambda : graphData(set5,label5,[3],title4,type=5)
testLookaheadRuntime2 = lambda : graphData(set6,label6,[3],title4,type=5)
testLookaheadRuntime3 = lambda : graphData(set7,label7,[3],title4,type=5)

# writes files with random graphs with random sizes,and widths (test_n[0],test_n[2],test_n[3].. etc)
# -1 on argument indicates random
def generateTestGraphs(n,sizes,type=-1):
    for i in range(len(n)):
        nodes = sizes[i]
        width = nodes * 2
        if type == -1:
            try:
                randomUniformGraph("graphs/test_" + str(n[i]),nodes,width)
            except:
                continue    
        elif type == 0:
            try:
                randomMetricGraph("graphs/test_" + str(n[i]),nodes,width)
            except:
                continue    
        else:
            try:
                randomGraph("graphs/test_" + str(n[i]),nodes,width)
            except:
                continue 

# tests the heuristics on the graphs in the graphs older given by the indices 
# then return the numpy array of tour values, and times as well as an array of tours
def testHeuristics(indices,p1,p2,p3,modes):
    heuristics = ["swap","twoopt","greedy","custom"]
    results = np.zeros((len(indices),len(heuristics)))
    tours = []
    times = np.zeros((len(indices),len(heuristics)))

    for i in range(len(indices)):
        print("Iteration: " + str(i))
        filename  = "graphs/test_"+str(indices[i])
        print(i,)
        g = graph.Graph(modes[i],filename)

        currTours = []
        # swap
        times[i,0] = timeFunction(lambda: g.swapHeuristic())
        results[i,0] = (g.tourValue())
        currTours.append(g.perm)
        g.resetPerm()

        # two-opt
        times[i,1] = timeFunction(lambda: g.TwoOptHeuristic())
        results[i,1] = (g.tourValue())
        currTours.append(g.perm)
        g.resetPerm()  

        # greedy
        times[i,2] = timeFunction(lambda: g.Greedy())
        results[i,2] = (g.tourValue())
        currTours.append(g.perm)
        g.resetPerm() 

        # EPIC
        times[i,3] = timeFunction(lambda:g.custom(p1,p2,p3))
        results[i,3] = (g.tourValue())
        currTours.append(g.perm)

        print([heuristics[x] +':'+ str(round(times[i,x],2)) for x in range(4)])
        tours.append(currTours)
    return (results,np.array(tours),times)

# will graph data for analysis,
# assumes data is in folders named fnames, each containing files:
# results.csv the Nx4 matrix of tour length results
# times.csv the Nx4 matrix of execution times of each heuristic
# tours.npy Nx4x* array tours generated by each heuristic
# cols is a set of up to 4 indices, indicating the heuristics to be compared 
# type
# Bar : 1 = graph average cost of all graphs of each heuritic in each file over the given rows as bar graph
#     : 2 = graph average cost of graph against the size of graph for each heuristic over given rows
#     : 3 = graph the costs of each heuristic from all files for each test number
#     : 4 = graph runtime against test number for each heuristic in each file over given rows
#     : 5 = graph average runtime against the size of graph for each heuristic over given rows
#     : 6 = graph a TSP problem at a single row for up to 4 heuristics, if not given a graphPath, will look for corresponding graph in graphs/euclidian
# fnames follow format: ER_s5+1n-10_1_0.5
#                      euclidianRandom/graphs start at 0 nodes add 1 every 5 rows/3 parameters to custom
def graphData(fnames,labels,cols,title,rows=[],type=1,graphPath="",errbars=False,trendLines=False,onlyTrends=False,trendDegree=3):
    plt.rc('text',usetex=True)
    plt.rc('font',family='serif')
    # python list containing numpy arrays
    data = []
    routes = []
    names = {0:"swap",1:"twoopt",2:"greedy",3:"custom"}
    colorsH = {0:(0, 0.24705882352941178, 0.3607843137254902),1:(0.47843137254901963, 0.3176470588235294, 0.5843137254901961)
                ,2:(0.9372549019607843, 0.33725490196078434, 0.4588235294117647)
                ,3:(1.0, 0.6509803921568628, 0)}
    colorsSeq = [(0, 0.24705882352941178, 0.3607843137254902),(0.47843137254901963, 0.3176470588235294, 0.5843137254901961),(0.9372549019607843, 0.33725490196078434, 0.4588235294117647),(1.0, 0.6509803921568628, 0)]

    for filename in fnames:
        
        fileToUse = ''

        if type == 1 or type == 2 or type == 3 or type == 6:
            fileToUse = "results.csv"
        elif type == 4 or type == 5:
            fileToUse = "times.csv"
        else:
            fileToUse = "tours.npy"

        path = 'results/' + filename + '/'
        try:
            r = np.load(path + "tours.npy",allow_pickle=True)
            d = np.loadtxt(path + fileToUse,delimiter=',')[:,cols]
            if rows != []:
                data.append(d[rows])
                routes.append(r[rows])
            else:
                data.append(d)
                routes.append(r)
            print(r[rows])

        except Exception as E:
            labels.pop(0)
            print(E)
            print("could not load:" + filename + " excluding from graph")
    

    # once we have the data, we pre-process it and graph it
    if type == 1:
        # calculate the averages of each file on the columns
        averages = np.zeros((len(fnames),len(cols)))
        stds = np.zeros((len(fnames),len(cols)))
        for i,d in enumerate(data):
            averages[i] = np.mean(d,axis=0)
            stds[i] = np.std(d,axis=0)
        
        # set parameters
        space_between_subgraphs = 0.5
        sub_bars_num = len(cols)
        sub_bar_width = 0.5/sub_bars_num

        labelsX = np.arange(0,len(fnames))

        fig,ax = plt.subplots()
        
        rects = []
        for i in range(len(cols)):
            offset = sub_bar_width/2 if (sub_bars_num % 2 == 0) else 0

            barHeights = averages[:,i]
            barErrs = stds[:,i]

            barXs = labelsX + offset + ((i - sub_bars_num//2) * sub_bar_width)
            
            rect = None

            if errbars:
                rect = ax.bar(barXs,barHeights,sub_bar_width,yerr=barErrs,color=colorsH[cols[i]],label=names[cols[i]])
            else:
                rect = ax.bar(barXs,barHeights,sub_bar_width,color=colorsH[cols[i]],label=names[cols[i]])
            for i in range(len(barXs)): 
                ax.text(barXs[i], barHeights[i] + 0.05,
                    str(round(barHeights[i],2)),
                    ha='center', va='bottom')
            rects.append(rect)
        
        #  Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('Average Tour Cost')
        ax.set_title(title)
        ax.set_xticks(labelsX)
        ax.set_xticklabels(labels)
        ax.legend()

        fig.tight_layout()
        plt.show()

    elif type == 2 or type == 5:
        # we extract size data, will have len(fnames) entries with lists of test sizes
        sizes = []
        for routeData in routes:
            s = [] 
            for row in routeData:
                s.append(len(row[0]))
            sizes.append(s)

        # now we average the values vertically for rows in data which had the same test graph size
        sizeToRowsList = []
        for i,sizesList in enumerate(sizes):
            sizeToRows = {}
            for j,s in enumerate(sizesList):
                if s in sizeToRows:
                    sizeToRows[s].append(data[i][j])    
                else:
                    sizeToRows[s] = [data[i][j]]
            sizeToRowsList.append(sizeToRows)

        fig,ax = plt.subplots()

        #each different file might have different number of graphs so we graph them separately
        for fileI,sizeToRows in enumerate(sizeToRowsList):
            # now we can iterate over all sizes and graph
            X = np.arange(len(sizeToRows.keys()))
            Y = np.zeros((len(sizeToRows.keys()),len(cols)))
            Stds = np.zeros((len(sizeToRows.keys()),len(cols)))

            for i,s in enumerate(sizeToRows.keys()):
                Y[i] = (np.mean(sizeToRows[s],axis=0))
                Stds[i] = (np.std(sizeToRows[s],axis=0))
            
            for i in range(len(cols)):
                label = labels[fileI] + '-' + names[cols[i]]

                if not(onlyTrends):
                    if errbars:
                        ax.errorbar(X,Y[:,i],yerr=Stds[:,i],label=label)
                    else:
                        ax.plot(X,Y[:,i],label=label)
                    
                if trendLines:
                    # calc the best trendline
                    
                    z = np.polyfit(X, Y[:,i],trendDegree)
                    p = np.poly1d(z)
                    plt.plot(X,p(X),'--',label=poly2latex(p))

        #  Add some text for labels, title and custom x-axis tick labels, etc.
        ylabel = "Average Tour Cost"
        if type == 5:
            ylabel = "Runtime in seconds"

        ax.set_ylabel(ylabel)
        ax.set_xlabel('Number of nodes')
        ax.set_title(title)
        # ax.set_xticks(labelsX)
        # ax.set_xticklabels(labels)
        ax.legend()

        fig.tight_layout()

        plt.show()
    elif type == 3 or type == 4:

        fig,ax = plt.subplots()
        print(data)
        #each different file might have different number of graphs so we graph them separately
        for fileI in range(len(data)):
            # now we can iterate over all sizes and graph
            X = np.arange(len(d))
            Y = None

            print(Y)
            for i in range(len(cols)):
                label = labels[fileI] + '-' + names[cols[i]]
                Y = data[fileI][:,i]

                if not(onlyTrends):
                    if errbars:
                        ax.errorbar(X,Y,yerr=Stds[:,i],label=label)
                    else:
                        ax.plot(X,Y,label=label)
                    
                if trendLines:
                    # calc the best trendline
                    
                    z = np.polyfit(X, Y[:,i],trendDegree)
                    p = np.poly1d(z)
                    plt.plot(X,p(X),'--',label=poly2latex(p))


        #  Add some text for labels, title and custom x-axis tick labels, etc.
        ylabel = "Tour Cost"
        if(type == 4):
            ylabel = "Runtime in seconds"
        ax.set_ylabel(ylabel)
        ax.set_xlabel('Test Number')
        ax.set_title(title)
        ax.legend()

        fig.tight_layout()

        plt.show()
  
    elif type == 6:
        #we graph routes at first row in rows for all heuristics in the first file

        concernedRoutes = routes[0][0]
        concernedData = data[0][0]
        graph = "graphs/euclid/test_" + str(rows[0]) if graphPath == "" else graphPath
        X,Y = loadEuclidianGraph(graph)
        # if not given file path to graph assume it's a euclidian graph and it is in a known folder

        xlen = 2 if len(cols) >= 2 else 1
        ylen = 1 if len(cols) <= 2 else 2

        fig,axes = plt.subplots(ylen, xlen)

        for i,ax in enumerate(axes.flat):
            permutation = concernedRoutes[cols[i]]
            ordX = [None] * (len(X) + 1)
            ordY = [None] * (len(Y) + 1)
            
            #wrap around
            permutation.append(permutation[0])

            for j,p in enumerate(permutation):
                ordX[j] = X[p]
                ordY[j] = Y[p]

            sequenceColors = ['k' for x in range(len(X))]
            sequenceColors[0] = 'r'
            sequenceColors[1] = 'y'
            sequenceColors[-1] = 'b'

            ax.scatter(ordX[0:-1],ordY[0:-1],c=sequenceColors, zorder=1)
            ax.plot(ordX,ordY,color='k',zorder=0)
            
            ax.set_title(names[cols[i]] +' '+ str(round(concernedData[cols[i]],1)))

        fig.tight_layout()
        plt.show()
            

    else:
        return
    return

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
    plt.show()

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

# generates random metric not necessarily euclidian graph, writes it to filename in the non-euclidian format
def randomMetricGraph(filename,n,width):
    f = open(filename,'x')
    # to generate metrics satisfying the inequality we chose a value x 
    # and give each edge any value in the range [x,2x], meaning that all possible triangles
    # will follow the triangle inequality, since the long edge will be at most the same length as its other edges

    # we choose x so that 2x == width, 
    x = width/2

    for i in range(n):
        for j in range(i):
            dist = random.randint(x,2*x)
            f.write(str(i) + ' ' + str(j) + ' ' + str(dist) + os.linesep)
# Generates completely random graph, by just randomising distances, with maximum distance set by width
def randomGraph(filename,n,width):
    f = open(filename,'x')
    # to generate metrics satisfying the inequality we chose a value x 
    # and give each edge any value in the range [x,2x], meaning that all possible triangles
    # will follow the triangle inequality, since the long edge will be at most the same length as its other edges

    # we choose x so that 2x == width, 

    for i in range(n):
        for j in range(i):
            dist = random.randint(0,width)
            f.write(str(i) + ' ' + str(j) + ' ' + str(dist) + os.linesep)

# utility to convert a polynomial coefficient array into a latex expression
def poly2latex(p):
    coefs = p.coef  # List of coefficient, sorted by increasing degrees
    res = ""  # The resulting string
    for i, a in enumerate(coefs):
        if int(a) == a:  # Remove the trailing .0
            a = int(a)
        if i == 0:  # First coefficient, no need for X
            if a > 0:
                res += "{a} + ".format(a=np.format_float_scientific(a,exp_digits=1,precision=1))
            elif a < 0:  # Negative a is printed like (a)
                res += "({a}) + ".format(a=np.format_float_scientific(a,exp_digits=1,precision=1))
            # a = 0 is not displayed 
        elif i == 1:  # Second coefficient, only X and not X**i
            if a == 1:  # a = 1 does not need to be displayed
                res += "X + "
            elif a > 0:
                res += "{a} \;X + ".format(a=np.format_float_scientific(a,exp_digits=1,precision=1))
            elif a < 0:
                res += "({a}) \;X + ".format(a=np.format_float_scientific(a,exp_digits=1,precision=1))
        else:
            if a == 1:
                # A special care needs to be addressed to put the exponent in {..} in LaTeX
                res += "X^{i} + ".format(i="{%d}" % i)
            elif a > 0:
                res += "{a} \;X^{i} + ".format(a=np.format_float_scientific(a,exp_digits=1,precision=1), i="{%d}" % i)
            elif a < 0:
                res += "({a}) \;X^{i} + ".format(a=np.format_float_scientific(a,exp_digits=1,precision=1), i="{%d}" % i)
    return "$" + res[:-3] + "$" if res else ""

def shade(RGB,shade,component):
    R = RGB[0] if component != 0 else (((RGB[0] * 255) + shade) % 255)/255
    G = RGB[1] if component != 1 else (((RGB[1] * 255) + shade) % 255)/255
    B = RGB[2] if component != 2 else (((RGB[2] * 255) + shade) % 255)/255

    return (R,G,B)



def timeFunction(func):
    start_time = time.time()
    func()
    return time.time() - start_time
