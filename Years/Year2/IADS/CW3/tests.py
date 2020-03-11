import math
import graph

import sys

if __name__ == "__main__":
    g = graph.Graph(-1,"cities50")
    print(g.tourValue())
    g.swapHeuristic()
    print("swap:" + str(g.tourValue()))
    print(g.perm)

    g.TwoOptHeuristic()
    print("twoOpt:" + str(g.tourValue()))
    print(g.perm)

    g.Greedy()
    print("greedy:" + str(g.tourValue()))
    print(g.perm)

    g.Custom(4)
    print("custom:" + str(g.tourValue()))
    print(g.perm)

