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
import Control.Monad (msum)





{- NOTES:

-- DO NOT CHANGE THE NAMES OR TYPE DEFINITIONS OF THE FUNCTIONS!
You can write new auxillary functions, but don't change the names or type definitions
of the functions which you are asked to implement.

-- Comment your code.

-- You should submit this file when you have finished the assignment.

-- The deadline is the  10th March 2020 at 3pm.

-- See the assignment sheet and document files for more information on the predefined game functions.
top
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




-- The next function should return all the possible continuations of input search branch through the grid.
-- Remember that the robot can only move up, down, left and right, and can't move outside the grid.
-- The current location of the robot is the head of the input branch.
-- Your function should return an empty list if the input search branch is empty.
-- This implementation of next function does not backtrace branches.

-- since this function is used a  in all functions later on, I will focus on the speed, and even though i could do it in 3 lines, recursion will be the fastest approach here, I am afraid :C
-- NOTE: i know you asked for the auxilary functions to be put at the bottom of the file, however, 95% of mine use less arguments than the originals
-- and so I have to keep them in the main bodies of the calling functions, I used let statements to make the functions read naturally
next::Branch -> Graph ->  [Branch]
next [] _ = []
next _ [] = []
next branch@(currNode:xs) graph = 
    let                 
        -- Finds the successor nodes in reverse-lexicographic order (due to tail-recursion)
        readSuccessorNodes :: Graph -> Int -> [Node] -> [Node]
        readSuccessorNodes [] _ list = list
        readSuccessorNodes graph@(val:xs) col list
            | col >= numNodes = list
            | otherwise       = case val of
                                    0 -> readSuccessorNodes xs (col+1) (list) 
                                    _ -> readSuccessorNodes xs (col+1) (col:list)

        -- Tail-recursively appends each of given succesors to the branch, and in doing so we get
        -- a list of successor branches in lexicographic order, and there is no need to call reverse! *stonks*
        getSuccessorBranches :: [Node] -> [Branch] -> [Branch]
        getSuccessorBranches [] list = list 
        getSuccessorBranches (succNode:xs) list = (getSuccessorBranches xs ((succNode:branch):list))

        -- A subgraph of graph, starting at the row corresponding to currNode
        subGraph = drop (numNodes * currNode) graph 

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

-- type to represent the context of a bfs search
type BfsContext = ([Branch],[Node],Maybe Branch)

-- BIG ASSUMPTION: I am assuming that the initial call to BFS will have at most one branch in the list, to avoid clutter!!
breadthFirstSearch::Graph -> Node->(Branch ->Graph -> [Branch])->[Branch]->[Node]->Maybe Branch
breadthFirstSearch [] _ _ _ _                           = Nothing                                         
breadthFirstSearch _ _ _ [] _                           = Nothing                                          
breadthFirstSearch g goal next ([]:xs) exploredList     = breadthFirstSearch g goal next xs exploredList   -- ignore empty branches, to be robust 
breadthFirstSearch g goal next [startBranch] exploredList 
    | isSolution startBranch goal   = Just startBranch
    | otherwise                     = bfs' [startBranch] exploredList  -- we launch search as normal, with the assumption that the agenda is already generated but not explored yet
        where
            -- the underlying auxilary function
            -- I am representing the side effects of changing the agenda and explored list in the for loop with a tuple,
            -- so that i can scan the agenda from the left and cause those 'intended side effects' for further items
            bfs'::[Branch]->[Node]->Maybe Branch
            bfs' [] _                   = Nothing  -- if the agenda is empty, give up, no solution
            bfs' agenda exploredList    = 
                let
                    -- generates the given branch with given BFS context (agenda,exploredlist,current solution)
                    -- will return a new context after the node is generated 
                    -- we check if a branch is a solution when it's generated
                    generateNode :: BfsContext -> Branch -> BfsContext
                    generateNode (a,el,ms) []            = (a,el,ms)                    -- an empty branch doesnt affect the context
                    generateNode (a,el,Just sol) _       = (a,el,Just sol)              -- if a solution is already found, do nothing more
                    generateNode (agenda,exploredList,currSol) branch@(currNode:xs)
                        | elem currNode exploredList    = (agenda,exploredList,currSol)     -- if node is in explored (or in frontier, so also in explored), ignore it 
                        | checkArrival goal currNode    = (agenda,exploredList,Just branch) 
                        | otherwise = (agenda++[branch],exploredList,currSol)               -- when generating a node we add it to the end of the agenda if its not explored or a solution

                    -- expands the given branch with given context
                    -- will retutn a new context after the node is expanded
                    expandNode :: BfsContext -> Branch -> BfsContext
                    expandNode (([]:xs),el,ms) _        = (xs,el,ms)                    -- skip empty branches in agenda
                    expandNode (a,el,Just x) branch     = (a,el,Just x)                 -- if we already found a solution, no need to expand this node 
                    expandNode ((shallowestBranch:bs),exploredList,currSol) branch@(currNode:xs) =
                        foldl (generateNode) (bs,currNode:exploredList,currSol) (next branch g)  -- when we expand a branch, we generate its successors, and update the frontier and explored list 

                    -- we expand the nodes and change the context as we go, capturing the side effects, return the first context with solution or last context
                    (newAgenda,newExploredList,newSolution) = foldl expandNode (agenda,exploredList,Nothing) agenda
                in 
                    -- if we didn't find the solution we start the search on the next level, i.e. the new agenda
                    case newSolution of
                        Nothing  -> bfs' newAgenda newExploredList
                        Just sol -> Just sol 

-- | Depth-Limited Search:
-- The depthLimitedSearch function is similiar to the depthFirstSearch function,
-- except its search is limited to a pre-determined depth, d, in the search tree.

-- I am assuming that the agenda will always have one branch the first time
depthLimitedSearch::Graph ->Node->(Branch ->Graph-> [Branch])->[Branch]-> Int->[Node]-> Maybe Branch
depthLimitedSearch [] _ _ _ _ _ = Nothing
depthLimitedSearch _ _ _ [] _ _ = Nothing                                  
depthLimitedSearch g goal next [startBranch] d exploredList = dls' startBranch d exploredList 
    where
        -- performs depth limited search with less arguments
        dls'::Branch -> Int -> [Node]-> Maybe Branch
        dls' [] _ _ = Nothing 
        dls' branch@(currNode:xs) d exploredList  -- on depth limit, forget about successors
            | d == 0                         = if checkArrival goal currNode then Just branch else Nothing 
            | checkArrival goal currNode     = Just branch
            | explored currNode exploredList = Nothing 
            | otherwise                      = 
                msum $ 
                    map (\succBranch -> dls' succBranch (d-1) (currNode:exploredList)) $
                        (next branch g) 




 -- | Section 4: Informed search

-- | The cost function calculates the current cost of a trace. The cost for a single transition is given in the adjacency matrix.
-- The cost of a whole trace is the sum of all relevant transition costs.
cost :: Graph ->Branch  -> Int
cost [] _ = 0
cost _ [] = 0
cost _ [initialNode]                = 0 
cost graph (curNode:prevNode:ns)    = 
    let
        -- the address in the graph for the cost between prev and curr node
        indexOfCost = ((prevNode * numNodes) + curNode)
        -- the cost between prev and curr node
        prevToCurrent = graph !! indexOfCost
    in 
        case prevToCurrent of
            0 -> 9999    -- invalid branches, get astronomical costs, because why not
            _ -> prevToCurrent + cost graph (prevNode:ns)
 


    
-- | The getHr function reads the heuristic for a node from a given heuristic table.
-- The heuristic table gives the heuristic (in this case straight line distance) and has one entry per node. It is ordered by node (e.g. the heuristic for node 0 can be found at index 0 ..)  

getHr:: [Int]->Node->Int
getHr hrTable node = hrTable !! node

aStarSearch::Graph->Node->(Branch->Graph -> [Branch])->([Int]->Node->Int)->[Int]->(Graph->Branch->Int)->[Branch]-> [Node]-> Maybe Branch
aStarSearch [] _ _ _ _ _ _ _                                   = Nothing 
aStarSearch g goal next getHr hrTable cost agenda exploredList = ass' agenda exploredList
    where 
        -- auxilary function with less arguments, assumes valid input, goal can be in input
        ass':: [Branch] -> [Node] -> Maybe Branch
        ass' [] _                   = Nothing              -- empty agenda = no solution
        ass' ([]:bs) exploredList   = ass' bs exploredList -- we skip empty branches
        ass' (bestBranch@( currNode:ns ):bs) exploredList               
            | checkArrival goal currNode     = Just bestBranch  
            | explored currNode exploredList = ass' bs exploredList -- to avoid loops, we don't cover identical nodes twice (consistent heuristic means no repetition guaranteed)
            | otherwise = 
                let 
                    evaulationFunction b = (getHr hrTable $ head b) + cost g b
                    newAgenda            = (next bestBranch g) ++ bs            -- we expand the bestBranch and add its children to the agenda
                    sortedBranches       = sortOn evaulationFunction newAgenda  -- next bestBranch is now at head of sortedBranches
                in 
                    ass' sortedBranches (currNode:exploredList)                 -- repeat the process


-- | Section 5: Games
-- See ConnectFour.hs for more detail on  functions that might be helpful for your implementation. 

-- | Section 5.1 Connect Four with a TwistnumNodes

-- The function determines the score of a terminal state, assigning it a value of +1, -1 or 0:
eval :: Game -> Int
eval game  = case checkWin game minPlayer of 
                True -> -1 
                False -> --if MIN didn't win, it's either a draw or a win for MIN
                    if checkWin game maxPlayer
                        then
                            1
                        else 
                            0

-- | The alphabeta function should return the minimax value using alphabeta pruning.
-- The eval function should be used to get the value of a terminal state. 


-- since I am trying to adhere to the pseudocode as closely as possible, I will be mimicking a for loop with a scanl, and will require a 'search state' which
-- is a way of getting 'side effects' by making them planned effects, synnonymous to keeping parameters in a recursion.
alphabeta:: Role -> Game -> Int
alphabeta _ [] = 0 -- just in case
alphabeta player game
    | maxPlayer == player = maxValue game (-2) 2 -- human player is max
    | minPlayer == player = minValue game (-2) 2 -- comp player is min
    where
        -- finds the minimax value of a given game on max players turn
        maxValue:: Game -> Int -> Int -> Int
        maxValue game a b
            | terminal game = eval game
            | otherwise     = 
                let 
                    -- we find the successor/child games in reverse order (turns first)
                    nextGames:: [Game]
                    nextGames = reverse $ movesAndTurns game maxPlayer 

                    -- given the best minimax value so far and the current alpha value and some game we can reach, 
                    -- explore the given game and return the new best minimax value and alpha value after we explore that game
                    getMinimaxAndAlpha :: (Int,Int) ->  Game -> (Int,Int)
                    getMinimaxAndAlpha (bestMinimaxVal,a) game = 
                        let newMinimax = max (bestMinimaxVal) (minValue game a b) 
                        in (newMinimax,max a newMinimax)

                    -- we keep updating v,a with each child game of the given game, if we find any with minimax value that is greater than the current beta (min has a better play)
                    -- we stop looking and pick the last minimax value we accumulated (the maximum minimax value so far) 
                    (bestMinimax,newAlpha) = 
                        takeFirstWithOrLastElem (\(v,a)-> v >= b) $ 
                            scanl getMinimaxAndAlpha (-2,a) nextGames
                            
                in bestMinimax 
        
        -- finds the minimax value of a given game on min players turn
        minValue:: Game -> Int -> Int -> Int
        minValue game a b
            | terminal game = eval game
            | otherwise     = 
                let 
                    -- we parse the successor states, in reverse order (turns first)
                    nextGames:: [Game]
                    nextGames = reverse $ movesAndTurns game minPlayer

                    -- given the best minimax value so far and the current beta value and some game we can reach, 
                    -- explore the given game and return the new best minimax value and alpha value after we explore that game
                    getMinimaxAndBeta:: (Int,Int) ->  Game -> (Int,Int)
                    getMinimaxAndBeta (bestMinimaxVal,b) game =  
                        let newMinimax = min (bestMinimaxVal) (maxValue game a b) 
                        in (newMinimax,min b newMinimax)

                    -- we keep updating v,b with each child game of the given game, if we find any with minimax value that is lesser than the current alpha (max has a better play)
                    -- we stop looking and pick the last minimax value we accumulated (the maximum minimax value so far) 
                    (bestMinimax,newBeta) = 
                        takeFirstWithOrLastElem (\(v,b)-> v <= a) $ 
                            scanl getMinimaxAndBeta (2,b) nextGames

                in bestMinimax 
        
-- | OPTIONAL!
-- You can try implementing this as a test for yourself or if you find alphabeta pruning too hard.
-- If you implement minimax instead of alphabeta, the maximum points you can get is 10% instead of 15%.
-- Note, we will only grade this function IF YOUR ALPHABETA FUNCTION IS EMPTY.
-- The minimax function should return the minimax value of the state (without alphabeta pruning).
-- The eval function should be used to get the value of a terminal state.
minimax:: Role -> Game -> Int
minimax player game
    | maxPlayer == player   = maxMin game
    | otherwise             = minMax game
    where
        minMax game
            | terminal game = eval game
            | otherwise     = 
                let
                    successors = movesAndTurns game compPlayer
                in 
                    minimum (map maxMin successors)

        maxMin game
            | terminal game = eval game
            | otherwise     = 
                let
                    successors = movesAndTurns game humanPlayer
                in 
                    maximum (map minMax successors)
{- Auxiliary Functions
-- Include any auxiliary functions you need for your algorithms below.
-- For each function, state its purpose and comment adequately.
-- Functions which increase the complexity of the algorithm will not get additional scores
-}

-- Utilities --

-- given a list, will iterate through it and return the first Just value it finds, or a nothing if it doesn'tvalidBranches
-- when used on a map which maps depth first search to each branch, will cause the deepest branch to be evaluated first
firstJustOrNothing:: [Maybe a] -> Maybe a
firstJustOrNothing = (fromMaybe Nothing).(find (\result -> not $ isNothing result)) 

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

-- checks if a branches' head is a goal node
isSolution [] _ = False
isSolution (x:xs) goal = checkArrival goal x


-- the legendary graph of bucharest
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

-- /Utilities --


