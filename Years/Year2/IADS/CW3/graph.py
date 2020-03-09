import math
import random

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

    # generate initial population
    # we get the first chromosome using our greedy heuristic, and mutate it untill we fill the entire population
    def initialPop(size):
        self.Greedy()
        pop = [self.perm]

        # fill pop with mutations of a "good" permutation
        while (len(pop) < size):
            pop.append(self.Mutate(pop[0]))
        return pop
    # given two solution chromosomes, performs a crossover operation and yields a new chromosome of the same length
    def Crossover(x,y):

    # given a chromosome, mutates it and returns a new one
    # uses HPRM mutation operator 
    # (Abdoun & Chakir 2012 - A New Mutation Operator for Solving an NP-Complete Problem: Travelling Salesman Problem)
    # https://www.researchgate.net/publication/282732991_A_New_Mutation_Operator_for_Solving_an_NP-Complete_Problem_Travelling_Salesman_Problem
    def Mutate(x,mutationChance):
        nX = x[:]
        
        n = len(x)

        # pick 2 mutation points s.t. 0 <= a <= b <= n
        a = random.randint(0,n)
        b = random.randint(a,n)

        while a >= b:
            # swap bits at mutation points
            nX[a],nX[b] = nX[b],nX[a]

            # chance to mutate 
            p = random.uniform(0,1)
            if p < mutationChance:
                # choose random index
                j = random.randint(0,n)
                # permute elements at a and j
                nX[a],nX[j] = nXx[j],nX[a]
                a += 1
                b -= 1
        return nX
    # returns the fitness value of a given chromosome
    def Evaluate(x):

    # given a list of chromosome selects a portion of them according to evolutionary heuristics
    def Select(xs):

    # I will use genetic algorithms, since they're amazing, fun and good
    # I will represent the problem using the path representation method
    def Custom(self,popSize,crossoverChance,mutationChance):

