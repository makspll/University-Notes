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
        self.perm = [x for x in range(self.n)] if self.n > 0 else []
    # Complete as described in the spec, to calculate the cost of the
    # current tour (as represented by self.perm).
    def tourValue(self):
        return sum([ self.dists[self.perm[i]][self.perm[(i+1) % self.n]] for i in range(self.n)])

    # Attempt the swap of cities i and i+1 in self.perm and commit
    # commit to the swap if it improves the cost of the tour.
    # Return True/False depending on success.
    def trySwap(self,i):
        # will not work when the graph has 2 nodes or less, where swapping doesn't affect the cost
        if self.n <= 2:
            return False

        # we only need to consider the impact on the "sub-tour" between i-1 and i+2
        # effectively only the cost between i-1 and i, i and i+1, i+1 and i+2 changes
        

        A = self.perm[(i-1) % self.n]
        B = self.perm[i]
        C = self.perm[(i + 1) % self.n]
        D = self.perm[(i + 2) % self.n]

        costInitial = self.dists[A][B]  + self.dists[C][D]
        costAfter = self.dists[A][C] + self.dists[B][D]

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
        #reversing will not improve the tour if the graph has ony 2 nodes or less
        if self.n <= 2:
            return False

        #the effect of reversing will only change the costs around the edges of the reversed permutation segment
        A = self.perm[(i-1) % self.n]
        B = self.perm[i]
        C = self.perm[j]
        D = self.perm[(j + 1) % self.n]

        costInitial = self.dists[A][B]  + self.dists[C][D]
        costAfter = self.dists[A][C] + self.dists[B][D]
        
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
        if self.n == 0:
            return

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

    # a heuristic which chooses the best option between greedy with lookahead and nearest insertion, then tries a 2-opt improvement up to totOpts times
    # method factor biases the heuristic towards one of the methods (0.5 = equal, 0 = greedy, 1 = nearest insertion)
    def custom(self,totOpts,lookahead,bias):
        if self.n == 0:
            return

        perm = [0]    
        startIdx = 0
        nextIdx = startIdx
        visited = set(perm)
        
        while len(perm) < self.n:      
            # try different lookaheads and pick one which minimies distance per edge
            
            #if bias is 0 or 1, we dont need to try both methods
            
            delta1,delta2,subPathNew1,insertIdx,cityToInsert = sys.float_info.max,sys.float_info.max,[],0,0

            if bias == 0:
                (delta1,subPathNew1) = self.greedyLookahead(nextIdx,lookahead,visited)
            elif bias == 1:
                (delta2,insertIdx,cityToInsert) = self.insertNearest(perm,visited)
            else:
                (delta1,subPathNew1) = self.greedyLookahead(nextIdx,lookahead,visited)
                (delta2,insertIdx,cityToInsert) = self.insertNearest(perm,visited)

            # (cost,subpath) = min([(c,p) for (c,p) in [(cost1,subPath1),(cost2,subPath2)]])
            # pick the method which minimizes the cost increase
            
            if  delta1*bias < delta2*(1-bias):
                newSegment = subPathNew1[1:]
                perm.extend(newSegment)
                visited.update(newSegment)
            else:
                perm.insert(insertIdx,cityToInsert)
                visited.add(cityToInsert)               

            opts = 0
            better = True
            while better and opts < totOpts:
                # do a round of 2-opt untill totOpts or untill it makes no changes
                better = False 
                for j in range(len(perm)):
                    for i in range(j):
                        better = self.tryReverseGiven(perm,i,j)
                opts += 1
                
            nextIdx = perm[-1]
               
        self.perm = perm
    
    # returns shortest path starting on node n with length l and the cost of it
    # r is the distance from minimum if you want a non-shortest path
    # visited is the set of nodes you don't want to explore
    def greedyLookahead(self,n,l,visited):
        if l == 0:
            return (0,[n])
        else:
            explored = visited.copy()
            explored.add(n)

            # we find all subpaths from each neigbhour with length l-1, and find the one which minimizes cost + transitionCost
            neighbours = [idx for (idx,val) in enumerate(self.dists[n]) if idx not in explored]
            
            # in case there are no more visitable nodes, return
            if len(neighbours) == 0:
                return (0,[n])
            else:
                # find shortest subpath with l -1

                smallestCost = sys.float_info.max
                bestPath = None
                for i in neighbours:
                    (c,p) = self.greedyLookahead(i,l-1,explored)
                    c +=self.dists[n][i]

                    if c < smallestCost:
                        p.insert(0,n)
                        bestPath = p
                        smallestCost = c 

                return (smallestCost,bestPath)


    # an insertion heuristic which looks for a point to insert into an existing tours edge
    def insertNearest(self,tour,visited):    
        # select a city not in the subtour (not visited) which is closest to any of the cities in the subtour

        closestCity = -1
        currMin = sys.float_info.max
        for i in range(self.n):
            if i in visited:
                continue
            else:
                for j in range(len(tour)):
                    if i == j:
                        continue

                    dist = self.dists[i][tour[j]]
                    if dist < currMin:
                        currMin = dist
                        closestCity = i

        # find edge in subtour, which minimizes the cost increase when inserting into that edge (between its endpoints)

        # Maybe i misunderstood, and need to check actual edges ?
        insertionIdx = -1
        bestCostIncrease = sys.float_info.max  # the afterCost - beforeCost,s at the current insertion edge  
        for i in range(0,len(tour)):

            a = tour[i]
            b = closestCity
            c = tour[(i+1)% len(tour)]

            
            costDelta = (self.dists[a][b] + self.dists[b][c]) - (self.dists[a][c])

            if costDelta < bestCostIncrease:
                bestCostIncrease = costDelta
                insertionIdx = c

        return (bestCostIncrease,insertionIdx,closestCity)
            
    # try reverse but on a given perm
    def tryReverseGiven(self,perm,i,j):
        #the effect of reversing will only change the costs around the edges of the reversed permutation segment
        preInode = perm[(i-1) % len(perm)]
        iNode = perm[i]
        jNode = perm[j]
        postJnode = perm[(j + 1) % len(perm)]

        costInitial = self.dists[preInode][iNode]  + self.dists[jNode][postJnode]
        costAfter = self.dists[preInode][jNode] + self.dists[iNode][postJnode]
        
        if(costAfter < costInitial):
            perm[i:j+1] = perm[i:j+1][::-1]
            return True
        else:
            return False
    
    def resetPerm(self):
        self.perm = [x for x in range(self.n)]

    

