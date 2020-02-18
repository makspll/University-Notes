-- Inf2d Assignment 1 2017-2018
-- Matriculation number:
-- {-# OPTIONS -Wall #-}

module Main where 
import Data.List (sortBy,sortOn, elemIndices, elemIndex,find,permutations)
import ConnectFourWithTwist
import Data.Maybe (isNothing,fromMaybe,isJust)
import Debug.Trace (trace)
import Control.DeepSeq
import Test.QuickCheck

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
numNodes = 5


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
        -- A subgraph of graph, starting at the row corresponding to currNode
        subGraph = drop (numNodes * currNode) graph 

        -- Finds the successor nodes in reverse-lexicographic order (due to tail-recursion)
        readSuccessorNodes :: Graph -> Int -> [Node] -> [Node]
        readSuccessorNodes [] _ list = list
        readSuccessorNodes graph@(val:xs) col list
            | col >= numNodes = list
            | otherwise = case val of
                            0 -> readSuccessorNodes xs (col+1) (list) 
                            _ -> readSuccessorNodes xs (col+1) (col:list)

        -- Tail-recursively appends each of given succesors to the branch, and in doing so we get
        -- a list of successor branches in lexicographic order, and there is no need to call reverse!
        getSuccessorBranches :: [Node] -> [Branch] -> [Branch]
        getSuccessorBranches [] list = list 
        getSuccessorBranches (succNode:xs) list = (getSuccessorBranches xs ((succNode:branch):list))

        in getSuccessorBranches (readSuccessorNodes subGraph 0 []) []


-- |The checkArrival function should return true if the current location of the robot is the destination, and false otherwise.
checkArrival::Node -> Node -> Bool
checkArrival destination curNode = destination == curNode


explored::Node-> [Node] ->Bool
explored point exploredList = elem point exploredList

test_graph_1 :: Graph
test_graph_1 = [0,1,1,1,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,1 ,0,0,0,0,0]
{-|
    0
    |
1   2   3
        |
        4
-}
test_graph_2 :: Graph
test_graph_2 = [0,1,1,1,0, 0,0,0,0,1, 0,0,0,0,0, 0,0,0,0,0 ,0,0,0,0,0]
{-|
    0
    |
1   2   3
|
4
-}
test_graph_3 :: Graph
test_graph_3 = [0,2,1,0,0 ,0,0,0,0,4, 0,0,0,1,0, 0,0,0,0,4 ,0,0,0,0,0]
{-|
    0
    |
  1   2   
  |   |
  |   3
  |   |
  |  /
   4
-}
test_graph_3_heuristic :: [Int]
test_graph_3_heuristic = [4,4,3,4,0]

test_graph_4 :: Graph
test_graph_4 = --A,T,Z,O,S,L,M,D,C,R,F,P,B
                [0,118,75,0,140,0,0,0,0,0,0,0,0, --A
                 118,0,0,0,0,111,0,0,0,0,0,0,0, --T
                 75,0,0,71,0,0,0,0,0,0,0,0,0, --Z
                 0,0,71,0,151,0,0,0,0,0,0,0,0, --O
                 140,0,0,151,0,0,0,0,0,80,99,0,0, --S
                 0,111,0,0,0,0,70,0,0,0,0,0,0, --L
                 0,0,0,0,0,70,0,75,0,0,0,0,0, --M
                 0,0,0,0,0,0,75,0,120,0,0,0,0, --D
                 0,0,0,0,0,0,0,120,0,146,0,138,0, --C
                 0,0,0,0,80,0,0,0,146,0,0,97,0, --R
                 0,0,0,0,99,0,0,0,0,0,0,0,211, --F
                 0,0,0,0,0,0,0,0,138,97,0,0,101, --P
                 0,0,0,0,0,0,0,0,0,0,211,101,0] --B                    
test_graph_4_heuristic :: [Int]
test_graph_4_heuristic = [366,329,374,380,253,244,241,242,160,193,176,100,0]

debug = True
-- Section 3 Uniformed Search
-- | Breadth-First Search
-- The breadthFirstSearch function should use the next function to expand a node,
-- and the checkArrival function to check whether a node is a destination position.
-- The function should search nodes using a breadth first search order.



-- the state of the search, its agenda, explored nodes and solution if it was found, used to fold over the nodes
type SearchState = ([Branch],[Node],Maybe Branch)

breadthFirstSearch::Graph -> Node->(Branch ->Graph -> [Branch])->[Branch]->[Node]->Maybe Branch
breadthFirstSearch [] _    _    _      _ = Nothing  -- if the graph is empty, there are no nodes
breadthFirstSearch _  _    _    []     _ = Nothing
breadthFirstSearch g goal next ([]:xs) exploredList  = breadthFirstSearch g goal next xs exploredList   -- if the agenda is empty, we don't know where to start
breadthFirstSearch g goal next agenda@(fa:xs) exploredList 
    | any (isSolution) agenda = find isSolution agenda -- if solution is in agenda already, return it
    | otherwise = bfs' g  goal next agenda exploredList -- if it isn't we can continue as normal
        where
            -- checks if a branches' head is a goal node
            isSolution [] = False
            isSolution (x:xs) = checkArrival goal x

            -- the underlying auxilary function
            bfs':: Graph -> Node->(Branch ->Graph -> [Branch])->[Branch]->[Node]->Maybe Branch
            bfs' _  _    _    []     _ = Nothing  -- if the agenda is empty, there is no path to the goal node
            bfs' g  goal next agenda exploredList = 
                let
  
                    -- extends the given search state given a child branch/node to be generated
                    generateNode :: SearchState -> Branch -> SearchState
                    generateNode (a,el,ms) [] = (a,el,ms)--empty branches are skipped
                    generateNode (a,el,Just sol) _ = (a,el,Just sol) -- if a solution is already found, do nothing more
                    generateNode (agenda,exploredList,maybeSol) branch@(currNode:xs)
                        | elem currNode exploredList = (agenda,exploredList,maybeSol)`debugP` (show "in frontier or agenda: " ++ show branch) -- if node is in explored (or in frontier, so also in explored), ignore it 
                        | checkArrival goal currNode = (agenda,exploredList,Just branch) `debugP`  (show "is goal : " ++ show branch)-- if 
                        | otherwise = (agenda++[branch],exploredList,maybeSol) `debugP` (show "generating: " ++ show branch)

                    -- extends the given search state given a new branch/node to be extended
                    expandNode :: SearchState -> Branch -> SearchState
                    expandNode (([]:xs),el,ms) _ = (xs,el,ms) `debugP`(show "empty agenda: ")
                    expandNode (a,e,Just x) branch = (a,e,Just x) `debugP` (show "solution found: " ++ show branch)-- if we already found a solution, no need to expand this node 
                    expandNode ((shallowestBranch:bs),exploredList,maybeSol) branch@(currNode:xs)
                        = foldl (generateNode) (bs,currNode:exploredList,maybeSol) (next branch g)  `debugP` (show "expanding: " ++ show branch)

                    -- we get either the first search state which has a solution found, or one generated by the last element in the agenda
                    (newAgenda,newExploredList,newMaybeSolution) = takeFirstWithOrLastElem (\(_,_,ms) -> isJust ms) $ 
                                                                    scanl expandNode (agenda,exploredList,Nothing) agenda
                in 
                    case newMaybeSolution of
                        Nothing  -> bfs' g goal next newAgenda newExploredList
                        Just sol -> Just sol 

-- | Depth-Limited Search:
-- The depthLimitedSearch function is similiar to the depthFirstSearch function,
-- except its search is limited to a pre-determined depth, d, in the search tree.
depthLimitedSearch::Graph ->Node->(Branch ->Graph-> [Branch])->[Branch]-> Int->[Node]-> Maybe Branch
depthLimitedSearch []   _    _                     _  _            _ = Nothing
depthLimitedSearch _    _    _                     [] _            _ = Nothing                                  
depthLimitedSearch g goal next agenda@(currBranch:bs) d exploredList = firstJustOrNothing $ map (\branch -> dfs' g goal next branch d exploredList) agenda -- we launch dfs on each branch in the agenda
    where
        -- performs depth first search with only one starting branch
        dfs'::Graph ->Node->(Branch ->Graph-> [Branch])->Branch-> Int->[Node]-> Maybe Branch
        dfs' _ _ _ [] _ _ = Nothing 
        dfs' g goal next branch@(currNode:xs) d exploredList 
            | d == 0                         = if checkArrival goal currNode 
                                                then Just branch 
                                                else Nothing -- on depth limit, forget about successors
            | checkArrival goal currNode     = Just branch
            | explored currNode exploredList = Nothing 
            | otherwise                      = firstJustOrNothing $ 
                                                map (\succBranch -> dfs' g goal next succBranch (d-1) (currNode:exploredList) `debugP` ("expanding:" ++ show succBranch)) (next branch g) 



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
aStarSearch g goal next getHr hrTable cost ([]:bs) exploredList = aStarSearch g goal next getHr hrTable cost bs exploredList --we skip empty branches
aStarSearch g goal next getHr hrTable cost (firstBranch:bs) exploredList
    | checkArrival goal currNode     = Just firstBranch `debugP` ("goal: " ++ show firstBranch++ "frontier:" ++ show bs)
    | explored currNode exploredList = aStarSearch g goal next getHr hrTable cost (bs) exploredList `debugP` ("explored: " ++ show firstBranch ++ "frontier:" ++ show bs)
    | otherwise = let 
                    evaulationFunction branch = (getHr hrTable $ head branch) + cost g branch -- we sort branches (without the one we just expanded) on evaluation function in ascending order  
                    sortedBranches = sortOn evaulationFunction (expandedFrontier ++ bs)
                    in aStarSearch g goal next getHr hrTable cost (sortedBranches) (currNode:exploredList) `debugP` ("expanding: " ++ show firstBranch++ "frontier:" ++ show sortedBranches)
        where
            -- The node at the head of the deepest branch in the search
            currNode = head firstBranch
            -- The successive branches of the current Node (can be empty)
            expandedFrontier = next firstBranch g


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
    | maxPlayer player = maxValue game (-2) 2 -- human player is max
    | minPlayer player = minValue game (-2) 2 -- comp player is min
    where
        maxValue:: Game -> Int -> Int -> Int
        maxValue game a b
            | terminal game = eval game
            | otherwise = let 
                            v = -2 -- symbolic neg infinity
                            stopCondition:: (Int,Int) -> Bool
                            stopCondition (val,alpha) = val >= b -- we will use a scanl to traverse the options so we can halt early  

                            nextStates:: [Game]
                            nextStates = moves game humanPlayer

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
                            nextStates = moves game compPlayer
                            
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
    | maxPlayer player = maxMin game
    | otherwise = minMax game
    where
        minMax game
            | terminal game = eval game
            | otherwise = let
                            successors = moves game compPlayer
                            in minimum (map maxMin successors)
        maxMin game
            | terminal game = eval game
            | otherwise = let
                            successors = moves game humanPlayer
                            in maximum (map minMax successors)
{- Auxiliary Functions
-- Include any auxiliary functions you need for your algorithms below.
-- For each function, state its purpose and comment adequately.
-- Functions which increase the complexity of the algorithm will not get additional scores
-}

-- given a list, will iterate through it and return the first Just value it finds, or a nothing if it doesn't
-- when used on a map which maps depth first search to each branch, will cause the deepest branch to be evaluated first
firstJustOrNothing:: [Maybe a] -> Maybe a
firstJustOrNothing = (fromMaybe Nothing).(find (\result -> not $ isNothing result)) 

takeFirst::(a->Bool) -> [a] -> a
takeFirst = undefined--takeFirst chooseCondition list = find(\)


-- will take the first element satisfying the condition, or the last element if none do (last wont be checked)
takeFirstWithOrLastElem:: (a-> Bool) -> [a] -> a
takeFirstWithOrLastElem cond [x] = x
takeFirstWithOrLastElem cond (x:xs) = if cond x then x else takeFirstWithOrLastElem cond xs 

main = do let sol =  map (next [0]) (take 99999999 $ permutations [0,1,2,0,0,0,0,1,0,0,0,0,0,0,0,0])
            in sol `deepseq` putStrLn "completed profiling"