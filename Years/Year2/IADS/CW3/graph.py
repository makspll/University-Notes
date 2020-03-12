import math
import random
import sys


def euclid(p,q):
    x = p[0]-q[0]
    y = p[1]-q[1]
    return math.sqrt(x*x+y*y)
                
class Graph:

    # Complete as described in the specification, taking care of two cases:
    # the -1 case, where we read points in the Euclidean plane, and
    # the n>0 case, where we read a general graph in a different format.
    # self.perm, self.dists, self.n are the key variables to be set up.
    def __init__(self,n,filename):

        # open file reader
        f = open(filename,"r")

        # euclidian mode
        if n == -1:
            self.n = 0
            nodes = []

            for line in f:
                lineStripped = line.strip()

                if lineStripped == '':
                    f.close()
                    break
                else:
                    point = line.split()

                    x = float(point[0])
                    y = float(point[1])

                    nodes.append((x,y))
                    self.n += 1

            self.dists = [[0]*self.n for x in range(self.n)]
            # calculate distances between each node 

            # use the fact dists will be a symmetric square matrix
            # set the upper right triangle parallel to the lower left triangle
            for i in range(self.n):
                # diagonals will be untouched
                for j in range(i):                    
                    
                    distItoJ = euclid(nodes[i],nodes[j])

                    self.dists[i][j] = self.dists[j][i] = distItoJ
        
        # non-euclidian mode
        else:
            # assuming that all n(n+1)/2 edges are provided, and edges are symmetric
            self.n = n
            self.dists = [[0]*self.n for x in range(self.n)]


            for line in f:
                lineStripped = line.strip()

                if lineStripped == '':
                    f.close()
                    break
                else:
                    values = line.split()

                    i = int(values[0])
                    j = int(values[1])
                    dist = int(values[2])

                    self.dists[i][j] = self.dists[j][i] = dist

        # identity permutation perm[i] = i
        self.perm = [x for x in range(self.n)]
    # Complete as described in the spec, to calculate the cost of the
    # current tour (as represented by self.perm).
    def tourValue(self):
        return sum([ self.dists[self.perm[i]][self.perm[(i+1) % self.n]] for i in range(self.n)])

    # Attempt the swap of cities i and i+1 in self.perm and commit
    # commit to the swap if it improves the cost of the tour.
    # Return True/False depending on success.
    def trySwap(self,i):
        # we only need to consider the impact on the "sub-tour" between i-1 and i+2
        # effectively only the cost between i-1 and i, i and i+1, i+1 and i+2 changes
        
        prevN = self.perm[(i-1) % self.n]
        currN = self.perm[i]
        nextN = self.perm[(i + 1) % self.n]
        sndNextN = self.perm[(i + 2) % self.n]

        costInitial = self.dists[prevN][currN]  + self.dists[nextN][sndNextN]
        costAfter = self.dists[prevN][nextN] + self.dists[currN][sndNextN]

        if(costAfter < costInitial):
            nxtIdx = (i+1) % self.n
            self.perm[i],self.perm[nxtIdx] = self.perm[nxtIdx], self.perm[i]
            return True
        else:
            return False

    # Consider the effect of reversiing the segment between
    # self.perm[i] and self.perm[j], and commit to the reversal
    # if it improves the tour value.
    # Return True/False depending on success.              
    def tryReverse(self,i,j):
        #the effect of reversing will only change the costs around the edges of the reversed permutation segment
        preInode = self.perm[(i-1) % self.n]
        iNode = self.perm[i]
        jNode = self.perm[j]
        postJnode = self.perm[(j + 1) % self.n]

        costInitial = self.dists[preInode][iNode]  + self.dists[jNode][postJnode]
        costAfter = self.dists[preInode][jNode] + self.dists[iNode][postJnode]
        
        if(costAfter < costInitial):
            self.perm[i:j+1] = self.perm[i:j+1][::-1]
            return True
        else:
            return False
    
    def swapHeuristic(self):
        better = True
        while better:
            better = False
            for i in range(self.n):
                if self.trySwap(i):
                    better = True

    def TwoOptHeuristic(self):
        better = True
        totalDiff = 0
        while better:
            better = False
            for j in range(self.n-1):
                for i in range(j):
                    if self.tryReverse(i,j):
                        better = True
                

    # Implement the Greedy heuristic which builds a tour starting
    # from node 0, taking the closest (unused) node as 'next'
    # each time.
    def Greedy(self):

        # we always start at 0 
        self.perm[0] = 0
        startIdx = 0
        nextIdx = startIdx
        visited = {startIdx}

        for i in range(1,self.n):
            
            neighbours = [(val,idx) for (idx,val) in enumerate(self.dists[nextIdx]) if idx not in visited ]
            minDist,nextIdx = min(neighbours)

            self.perm[i] = nextIdx
            visited.add(nextIdx)


    # ( O(n-1) *  ) )
    def shortestPathFromNeighbours(self,n,l,visited):
        neighbours = [idx for (idx,val) in enumerate(self.dists[n]) if idx not in visited]

        leastCost = sys.float_info.max
        leastSubPath = []
        for nei in neighbours: 
            (cost,subPath) = self.shortestPathFrom(nei,l-1,visited)
            if(subPath == []):
                continue
            cost += self.dists[n][subPath[0]]
 
            if cost < leastCost:
                leastCost = cost
                leastSubPath = subPath
        return (leastCost,leastSubPath)
        
    # returns shortest path starting on any of the nodes with length l
    def shortestPathFrom(self,n,l,visited):
        if l == 0:
            return (0,[n])
        else:
            explored = visited.copy()
            explored.add(n)
            # find the shortest path with length l -1 starting at any of the nodes
            shortestSubPath = (sys.float_info.max,[])
            
            neighbours = [idx for (idx,val) in enumerate(self.dists[n]) if idx not in explored]

            for idx in neighbours:
                # subpath with l-1 lookahead from neighbour
                (cost,path) = self.shortestPathFrom(idx,l-1,explored)
                cost += self.dists[n][idx]  
        
                if cost < shortestSubPath[0]:
                    path.insert(0,n) 
                    shortestSubPath = (cost,path)
            
            return shortestSubPath

    # a heuristic which either tries a 2-opt improvmenet with probability p or the best between greedy, and greedy with lookahead
    def EPICHeuristic(self,p):

        perm = [0]
        startIdx = 0
        nextIdx = startIdx
        visited = {startIdx}

        while len(perm) < self.n:
            
      
            # try different lookaheads and pick one which minimies distance per edge
            
            (cost2,path2) = self.shortestPathFromNeighbours(nextIdx,2,visited)
            (cost3,path3) = self.shortestPathFromNeighbours(nextIdx,1,visited)

            (_,path) = min([(c,p) for (c,p) in [(cost2/2,path2),(cost3/1,path3)]])
            perm.extend(path)
            nextIdx = perm[-1]
            visited.update(path)

            failed = False
            while failed == False:
                if random.random() < p:
                    # do a round of 2-opt
                    for i in range(len(perm)):
                        for j in range(len(perm)):
                            self.tryReverse(i,j)
                else:
                    failed = True
        self.perm = perm[:self.n]
    
    def GreedyLookahead(self,l):
        # we always start at 0 
        perm = [0]
        startIdx = 0
        nextIdx = startIdx
        visited = {startIdx}

        for i in range((self.n-1)//l):
            # find the shortest subpath of length l

            (cost,path) = self.shortestPathFromNeighbours(nextIdx,l,visited)
    
            perm.extend(path)
            nextIdx = perm[-1]

            visited.update(path)
            

        # find the leftover shortest subpath
        if self.n - len(perm) != 0:
            (cost,path) = self.shortestPathFromNeighbours(perm[-1],self.n - len(perm),visited)
            perm.extend(path)

        self.perm = perm
   
    def resetPerm(self):
        self.perm = [x for x in range(self.n)]

   
