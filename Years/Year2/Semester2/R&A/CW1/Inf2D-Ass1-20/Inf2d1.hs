-- Inf2d Assignment 1 2017-2018
-- Matriculation number:
-- {-# OPTIONS -Wall #-}

module Inf2d1 where
import Data.List (sortBy, elemIndices, elemIndex)
import ConnectFourWithTwist

-- additional imports
-- for utilities
import Data.List (sortOn,find)
import Data.Maybe (isNothing,fromMaybe,isJust)






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
numNodes = 13


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



-- Section 3 Uniformed Search
-- | Breadth-First Search
-- The breadthFirstSearch function should use the next function to expand a node,
-- and the checkArrival function to check whether a node is a destination position.
-- The function should search nodes using a breadth first search order.



-- the state of the search, its agenda, explored nodes and solution if it was found, used to fold over the nodes
type SearchState = ([Branch],[Node],Maybe Branch)

breadthFirstSearch::Graph -> Node->(Branch ->Graph -> [Branch])->[Branch]->[Node]->Maybe Branch
breadthFirstSearch [] _    _    _      _ = Nothing  -- we can't traverse an empty graph
breadthFirstSearch _  _    _    []     _ = Nothing
breadthFirstSearch g goal next ([]:xs) exploredList  = breadthFirstSearch g goal next (validBranches xs g) exploredList   -- if the agenda is empty, we don't know where to start
breadthFirstSearch g goal next agenda@(fa:xs) exploredList 
    | any (isSolution) agenda = find isSolution agenda -- if solution is in agenda already, return it
    | otherwise = bfs' (validBranches agenda g) exploredList -- if it isn't we can continue as normal
        where
            -- checks if a branches' head is a goal node
            isSolution [] = False
            isSolution (x:xs) = checkArrival goal x

            -- the underlying auxilary function
            -- since I am trying to stick to the pseudocode, and I cannot have side effects
            -- I need searchState, to represent the parameters changing (without using recursion at each level)
            bfs'::[Branch]->[Node]->Maybe Branch
            bfs' []     _            = Nothing  -- if the agenda is empty, there is no path to the goal node
            bfs' agenda exploredList = 
                let
  
                    -- modifies the given search state given a child branch/node to be generated
                    generateNode :: SearchState -> Branch -> SearchState
                    generateNode (a,el,ms) [] = (a,el,ms)--empty branches are skipped
                    generateNode (a,el,Just sol) _ = (a,el,Just sol) -- if a solution is already found, do nothing more
                    generateNode (agenda,exploredList,maybeSol) branch@(currNode:xs)
                        | elem currNode exploredList = (agenda,exploredList,maybeSol)-- if node is in explored (or in frontier, so also in explored), ignore it 
                        | checkArrival goal currNode = (agenda,exploredList,Just branch) 
                        | otherwise = (agenda++[branch],exploredList,maybeSol)

                    -- modifies the given search state given a new branch/node to be extended
                    expandNode :: SearchState -> Branch -> SearchState
                    expandNode (([]:xs),el,ms) _ = (xs,el,ms) 
                    expandNode (a,el,Just x) branch = (a,el,Just x) -- if we already found a solution, no need to expand this node 
                    expandNode ((shallowestBranch:bs),exploredList,maybeSol) branch@(currNode:xs)
                        = foldl (generateNode) (bs,currNode:exploredList,maybeSol) (next branch g)

                    -- we drop the search states untill either we find one with a solution, or the last one
                    (newAgenda,newExploredList,newMaybeSolution) = takeFirstWithOrLastElem (\(_,_,ms) -> isJust ms) $ 
                                                                    scanl expandNode (agenda,exploredList,Nothing) agenda
                in 
                    case newMaybeSolution of
                        Nothing  -> bfs' newAgenda newExploredList
                        Just sol -> Just sol 

-- | Depth-Limited Search:
-- The depthLimitedSearch function is similiar to the depthFirstSearch function,
-- except its search is limited to a pre-determined depth, d, in the search tree.
depthLimitedSearch::Graph ->Node->(Branch ->Graph-> [Branch])->[Branch]-> Int->[Node]-> Maybe Branch
depthLimitedSearch []   _    _                     _  _            _ = Nothing
depthLimitedSearch _    _    _                     [] _            _ = Nothing                                  
depthLimitedSearch g goal next agenda@(currBranch:bs) d exploredList = firstJustOrNothing $  -- we launch dls on each valid branch in the agenda
                                                                        map (\branch -> dls' branch d exploredList) (validBranches agenda g)
    where
        -- performs depth limited search with only one starting branch
        dls'::Branch -> Int -> [Node]-> Maybe Branch
        dls' [] _ _ = Nothing 
        dls' branch@(currNode:xs) d _  -- on depth limit, forget about successors
            | d == 0                         = if checkArrival goal currNode 
                                                then Just branch 
                                                else Nothing 
            | checkArrival goal currNode     = Just branch
            | explored currNode exploredList = Nothing 
            | otherwise                      = firstJustOrNothing $ 
                                                map (\succBranch -> dls' succBranch (d-1) (currNode:exploredList) ) (next branch g) 




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
aStarSearch [] _ _ _ _ _ _ _ = Nothing 
aStarSearch g goal next getHr hrTable cost agenda exploredList = ass' (validBranches agenda g) exploredList -- validate the input
    where 
        ass':: [Branch] -> [Node] -> Maybe Branch
        ass' [] _  = Nothing                             -- empty agenda = no solution
        ass' ([]:bs) exploredList = ass' bs exploredList -- we skip empty branches
        ass' (bestBranch@(currNode:ns):bs) exploredList               
            | checkArrival goal currNode     = Just bestBranch
            | explored currNode exploredList = ass' bs exploredList 
            | otherwise = 
                let 
                    evaulationFunction branch = (getHr hrTable $ head branch) + cost g branch 
                    sortedBranches = sortOn evaulationFunction $ (next bestBranch g) ++ bs
                in 
                    -- we expand the node with smallest evaluation function first
                    ass' sortedBranches (currNode:exploredList)


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
alphabeta _ [] = 0 -- just in case
alphabeta player game
    | maxPlayer player = maxValue game (-2) 2 -- human player is max
    | minPlayer player = minValue game (-2) 2 -- comp player is min
    where
        maxValue:: Game -> Int -> Int -> Int
        maxValue game a b
            | terminal game = eval game
            | otherwise = let 
                            -- we parse the successor states, in reverse order (turns first)
                            nextStates:: [Game]
                            nextStates = reverse $ movesAndTurns game humanPlayer 

                            -- given the current v,a and the next state, calculate the new value of v,a after exploring the state
                            expandSearch :: (Int,Int) ->  Game -> (Int,Int)
                            expandSearch (prevVal,prevAlpha) state
                                | newVal <= prevAlpha = (newVal,prevAlpha)
                                | otherwise = (newVal,max prevAlpha newVal)
                                    where 
                                        newVal = max (prevVal) (minValue state prevAlpha b)

                            -- we keep updating v,a with each successor state, untill we find a value better 
                            -- than the current best choice for min, then we prune
                            (lastVal,lastAlpha) = takeFirstWithOrLastElem (\(v,a)-> v >= b) $ 
                                                    scanl expandSearch (-2,a) nextStates
                            in lastVal 

        minValue:: Game -> Int -> Int -> Int
        minValue game a b
            | terminal game = eval game
            | otherwise = let 
                            -- we parse the successor states, in reverse order (turns first)
                            nextStates:: [Game]
                            nextStates = reverse $ movesAndTurns game compPlayer

                            -- given the current v,b and the next state, calculate the new value of v,b after exploring the state
                            expandSearch:: (Int,Int) ->  Game -> (Int,Int)
                            expandSearch (prevVal,prevBeta) state
                                | newVal >= prevBeta = (newVal,prevBeta)
                                | otherwise = (newVal,min prevBeta newVal)
                                    where 
                                        newVal = min (prevVal) (maxValue state a prevBeta)

                            -- we keep updating v,b with each successor state, untill we find a value better 
                            -- than the current best choice for max, then we prune
                            (lastVal,lastBeta) = takeFirstWithOrLastElem (\(v,b)-> v <= a) $ 
                                                    scanl expandSearch (2,b) nextStates
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
                            successors = movesAndTurns game compPlayer
                            in minimum (map maxMin successors)
        maxMin game
            | terminal game = eval game
            | otherwise = let
                            successors = movesAndTurns game humanPlayer
                            in maximum (map minMax successors)
{- Auxiliary Functions
-- Include any auxiliary functions you need for your algorithms below.
-- For each function, state its purpose and comment adequately.
-- Functions which increase the complexity of the algorithm will not get additional scores

propMini player game = (player == 1 || player == 0) && length game == 16 ==> o1 == o2
    where
        o1 = minimax player game
        o2 = alphabeta player game
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

-- returns list of branches without any invalid branches (i.e. paths which are not allowed)
validBranches:: [Branch] -> Graph -> [Branch]
validBranches branches graph = filter (validBranch) branches
    where
        first:: [a] -> Maybe a
        first [] = Nothing
        first (x:xs) = Just x

        getsFromTo:: Node -> Node -> Bool
        getsFromTo node1 node2 = any (\b -> first b == Just node1) (next [node2] graph)

        validBranch branch = all (uncurry getsFromTo) (zip branch (tail branch))

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

-- the legendary graph
test_graph_4 :: Graph
               --0,1,2,3,4,5,6,7,8,9,10,11,12
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