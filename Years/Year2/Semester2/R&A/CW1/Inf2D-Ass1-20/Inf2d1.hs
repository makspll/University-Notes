-- Inf2d Assignment 1 2017-2018
-- Matriculation number:
-- {-# OPTIONS -Wall #-}


--module Inf2d1 where
module Main where
import Data.List (sortBy,sortOn, elemIndices, elemIndex,find)
import ConnectFourWithTwist
import Data.Maybe (isNothing,fromMaybe)
import Debug.Trace (trace)



{- NOTES:

-- DO NOT CHANGE THE NAMES OR TYPE DEFINITIONS OF THE FUNCTIONS!
You can write new auxillary functions, but don't change the names or type definitions
of the functions which you are asked to implement.

-- Comment your code.

-- You should submit this file when you have finished the assignment.

-- The deadline is the  10th March 2020 at 3pm.

-- See the assignment sheet and document files for more information on the predefined game functions.

-- See the README for description of a user interface to test your code.

-- See www.haskell.org for haskell revision.

-- Useful haskell topics, which you should revise:
-- Recursion
-- The Maybe monad
-- Higher-order functions
-- List processing functions: map, fold, filter, sortBy ...

-- See Russell and Norvig Chapters 3 for search algorithms,
-- and Chapter 5 for game search algorithms.

-}

-- Section 1: Uniform Search

-- 6 x 6 grid search states

-- The Node type defines the position of the robot on the grid.
-- The Branch type synonym defines the branch of search through the grid.
type Node = Int
type Branch = [Node]
type Graph= [Node]

numNodes::Int
numNodes = 4



-- 


-- The next function should return all the possible continuations of input search branch through the grid.
-- Remember that the robot can only move up, down, left and right, and can't move outside the grid.
-- The current location of the robot is the head of the input branch.
-- Your function should return an empty list if the input search branch is empty.
-- This implementation of next function does not backtrace branches.

next::Branch -> Graph ->  [Branch]
next [] _ = []
next _ [] = []
next branch@(currNode:xs) graph = 
    let 
        -- Get a graph, starting at the row corresponding to current head node of the branch
        currNodeRow = drop (numNodes * currNode) graph
        -- Get a list of successor nodes from this node
        reachableNodes = [ col |(col,val)<-zip [0..] currNodeRow, val /= 0, col <= numNodes]
        -- Prepend the branch to each successor
        possibleBranches = map (\succNode -> succNode:branch) (reachableNodes) 
        
        in possibleBranches
        

-- |The checkArrival function should return true if the current location of the robot is the destination, and false otherwise.
checkArrival::Node -> Node -> Bool
checkArrival destination curNode = destination == curNode


explored::Node-> [Node] ->Bool
explored point exploredList = elem point exploredList

test_graph_1 :: Graph
test_graph_1 = [0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0]
test_graph_2 :: Graph
test_graph_2 = [0,1,1,1,0, 0,0,0,0,1, 0,0,0,0,0, 0,0,0,0,0 , 0,0,0,0,0]
test_graph_3 :: Graph
test_graph_3 = [0,2,1,0,0 ,0,0,0,0,4, 0,0,0,1,0, 0,0,0,0,4, 0,0,0,0,0]
test_graph_3_heuristic :: [Int]
test_graph_3_heuristic = [4,4,3,4,0]
debug = True
-- Section 3 Uniformed Search
-- | Breadth-First Search
-- The breadthFirstSearch function should use the next function to expand a node,
-- and the checkArrival function to check whether a node is a destination position.
-- The function should search nodes using a breadth first search order.

breadthFirstSearch::Graph -> Node->(Branch ->Graph -> [Branch])->[Branch]->[Node]->Maybe Branch

breadthFirstSearch [] _ _ _ _ = Nothing
breadthFirstSearch _ _ _ [] _ = Nothing 
breadthFirstSearch graph goal next ([]:otherBranches) exploredList = 
    breadthFirstSearch graph goal next otherBranches exploredList -- if we encounter empty branch, we skip it
breadthFirstSearch graph goal next (firstBranch:otherBranches) exploredList
    | checkArrival goal currNode = Just firstBranch 
    | explored currNode exploredList = 
        breadthFirstSearch graph goal next otherBranches exploredList 
    | otherwise = -- place the expanded branches at the end of the 'queue'
        breadthFirstSearch graph goal next (otherBranches++expandedFrontier) (currNode:exploredList) `debugP` ("expanding: " ++ show firstBranch) 
        where
            -- The current node at the beggining of the queue (i.e. first expanded at this depth)
            currNode = head firstBranch
            -- The successive branches of the current node (can have empty branches)
            expandedFrontier = next firstBranch graph


-- | Depth-Limited Search:
-- The depthLimitedSearch function is similiar to the depthFirstSearch function,
-- except its search is limited to a pre-determined depth, d, in the search tree.
depthLimitedSearch::Graph ->Node->(Branch ->Graph-> [Branch])->[Branch]-> Int->[Node]-> Maybe Branch
depthLimitedSearch [] _ _ _ _ _ = Nothing
depthLimitedSearch _ _ _ [] _ _= Nothing                                      
depthLimitedSearch graph goal next [branch] d exploredList 
    | d == 0 = if checkArrival goal currNode then Just branch else Nothing
    | checkArrival goal currNode = Just branch
    | explored currNode exploredList = Nothing -- if we reach an explored node, we 'backtrack' the recursion
    | otherwise = 
        -- We lazilly evaluate the successor branches of the first branch, meaning we only evaluate one path at a time
        firstResultOrNothing $ 
        map (\succBranch -> depthLimitedSearch graph goal next [succBranch] (d-1) (currNode:exploredList) `debugP` ("recursing into:" ++ show succBranch)) expandedFrontier
        where
            -- The node at the head of the deepest branch in the search
            currNode = head branch
            -- The successive branches of the current Node (can be empty)
            expandedFrontier = next branch graph

--HELPER
debugP = flip trace 
 -- | Section 4: Informed search


-- | AStar Helper Functions

-- | The cost function calculates the current cost of a trace. The cost for a single transition is given in the adjacency matrix.
-- The cost of a whole trace is the sum of all relevant transition costs.
cost :: Graph ->Branch  -> Int
cost [] _ = 0
cost _ [] = 0
cost gr [initialNode] = 0
cost gr (curNode:prevNode:ns) = prevToCur + cost gr (prevNode:ns)
    where prevToCur = gr !! ((prevNode * numNodes) + curNode)
          
 


    
-- | The getHr function reads the heuristic for a node from a given heuristic table.
-- The heuristic table gives the heuristic (in this case straight line distance) and has one entry per node. It is ordered by node (e.g. the heuristic for node 0 can be found at index 0 ..)  
getHr:: [Int]->Node->Int
getHr hrTable node = hrTable !! node   


-- | A* Search
-- The aStarSearch function uses the checkArrival function to check whether a node is a destination position,
---- and a combination of the cost and heuristic functions to determine the order in which nodes are searched.
---- Nodes with a lower heuristic value should be searched before nodes with a higher heuristic value.

aStarSearch::Graph->Node->(Branch->Graph -> [Branch])->([Int]->Node->Int)->[Int]->(Graph->Branch->Int)->[Branch]-> [Node]-> Maybe Branch
aStarSearch _ _ _ _ _ _ [] _ = Nothing
aStarSearch [] _ _ _ _ _ _ _ = Nothing
aStarSearch graph goal next getHr hrTable cost ([]:bs) exploredList =
    aStarSearch graph goal next getHr hrTable cost bs exploredList --we skip empty branches
aStarSearch graph goal next getHr hrTable cost (firstBranch:bs) exploredList
    | checkArrival goal currNode = Just firstBranch
    | explored currNode exploredList = aStarSearch graph goal next getHr hrTable cost (bs) exploredList
    | otherwise = let 
                    evaulationFunction branch = (getHr hrTable $ head branch) + cost graph branch -- we sort branches (without the one we just expanded) on evaluation function in ascending order  
                    sortedBranches = sortOn evaulationFunction (expandedFrontier ++ bs)
                    in aStarSearch graph goal next getHr hrTable cost (sortedBranches) (currNode:exploredList) `debugP` ("expanding: " ++ show firstBranch)
        where
            -- The node at the head of the deepest branch in the search
            currNode = head firstBranch
            -- The successive branches of the current Node (can be empty)
            expandedFrontier = next firstBranch graph

-- | Section 5: Games
-- See ConnectFour.hs for more detail on  functions that might be helpful for your implementation. 



-- | Section 5.1 Connect Four with a Twist

 

-- The function determines the score of a terminal state, assigning it a value of +1, -1 or 0:
eval :: Game -> Int
eval game  = -- I know you hint at using terminal, but you explicitly state that this function is used to classify a "terminal state" so I am assuming it's terminal
                case checkWin game compPlayer of -- checking comp first, because lets not kid ourselves, it will probably win more
                    True -> -1 
                    False -> if checkWin game humanPlayer --if MIN didn't win, it's either a draw or a win for MIN
                                then
                                    1
                                else 
                                    0


-- | The alphabeta function should return the minimax value using alphabeta pruning.
-- The eval function should be used to get the value of a terminal state. 
alphabeta:: Role -> Game -> Int
alphabeta player game
    | player == maxPlayer = maxValue game (-2) 2 -- human player is max
    | player == minPlayer = minValue game (-2) 2 -- comp player is min
    where
        maxValue:: Game -> Int -> Int -> Int
        maxValue game a b
            | terminal game = eval game
            | otherwise = let 
                            v = -2 -- symbolic neg infinity
                            stopCondition:: (Int,Int) -> Bool
                            stopCondition (val,alpha) = val >= b -- we will use a scanl to traverse the options so we can halt early  

                            nextStates:: [Game]
                            nextStates = moves game maxPlayer

                            newAlpha:: Int -> Int -> Int
                            newAlpha prevAlpha val = if val >= b then val else max prevAlpha val
    
                            valsAndAlphas = 
                                scanl (\(prevVal,prevAlpha) nxtState -> 
                                    (max prevVal $ minValue nxtState prevAlpha b ,newAlpha prevAlpha prevVal)) (v,a) nextStates-- recurse depth-first
                            
                            (lastVal,lastAlpha) = takeFirstWithOrLastElem stopCondition valsAndAlphas 
                            in lastVal 
        
        minValue:: Game -> Int -> Int -> Int
        minValue game a b
            | terminal game = eval game
            | otherwise = let 
                            v = 2 -- symbolic pos infinity
                            stopCondition:: (Int,Int) -> Bool
                            stopCondition (val,beta) = val <= a -- we will use a scanl to traverse the options so we can halt early  

                            nextStates:: [Game]
                            nextStates = moves game minPlayer
                            
                            newBeta:: Int -> Int -> Int
                            newBeta prevBeta val = if val <= a then val else min prevBeta val

                            valsAndBetas = 
                                scanl (\(prevVal,prevBeta) nxtState -> 
                                    (min prevVal $ maxValue nxtState a prevBeta,newBeta prevBeta prevVal)) (v,b) nextStates-- recurse depth-first
                            
                            (lastVal,lastBeta) = takeFirstWithOrLastElem stopCondition valsAndBetas
                            in lastVal
        
-- | OPTIONAL!
-- You can try implementing this as a test for yourself or if you find alphabeta pruning too hard.
-- If you implement minimax instead of alphabeta, the maximum points you can get is 10% instead of 15%.
-- Note, we will only grade this function IF YOUR ALPHABETA FUNCTION IS EMPTY.
-- The minimax function should return the minimax value of the state (without alphabeta pruning).
-- The eval function should be used to get the value of a terminal state.
minimax:: Role -> Game -> Int
minimax player game
    | player == maxPlayer = maxMin game
    | otherwise = minMax game
    where
        minMax game
            | terminal game = eval game
            | otherwise = let
                            successors = moves game minPlayer
                            in minimum (map maxMin successors)
        maxMin game
            | terminal game = eval game
            | otherwise = let
                            successors = moves game maxPlayer
                            in maximum (map minMax successors)
{- Auxiliary Functions
-- Include any auxiliary functions you need for your algorithms below.
-- For each function, state its purpose and comment adequately.
-- Functions which increase the complexity of the algorithm will not get additional scores
-}

-- given a list, will iterate through it and return the first Just value it finds, or a nothing if it doesn't
-- when used on a map which maps depth first search to each branch, will cause the deepest branch to be evaluated first
firstResultOrNothing:: [Maybe a] -> Maybe a
firstResultOrNothing = (fromMaybe Nothing).(find (\result -> not $ isNothing result)) 

takeFirst::(a->Bool) -> [a] -> a
takeFirst = undefined--takeFirst chooseCondition list = find(\)


-- will take the first element satisfying the condition, or the last element if none do (last wont be checked)
takeFirstWithOrLastElem:: (a-> Bool) -> [a] -> a
takeFirstWithOrLastElem cond [x] = x
takeFirstWithOrLastElem cond (x:xs) = if cond x then x else takeFirstWithOrLastElem cond xs 

main = do putStrLn $ show $minimax 0 [-1 | x <- [1..16]]