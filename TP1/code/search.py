# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

from game import Directions
import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

# Inspired by https://stackoverflow.com/a/25583948
def searchAlgorithmWithoutPriority(problem, pathList):
    #Shared code between BFS and DFS
    state = problem.getStartState() # starting state
    pathList.push([(state, '', 1)])
    visitedStates = []
    
    while not pathList.isEmpty():
        state = pathList.pop()
        lastNode = state[-1][0] 

        if problem.isGoalState(lastNode): 
            return [path[1] for path in state if path[1] != '']
        elif lastNode not in visitedStates: 
            successorList = problem.getSuccessors(lastNode)
            visitedStates.append(lastNode)
            for successor in successorList:
                if successor[0] not in visitedStates: 
                    newPath = state[:]
                    newPath.append(successor)
                    pathList.push(newPath) 
    return []

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """

    '''
        INSÉREZ VOTRE SOLUTION À LA QUESTION 1 ICI
    '''
    from util import Stack
    # LIFO data structure
    return searchAlgorithmWithoutPriority(problem, Stack())
    

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""


    '''
        INSÉREZ VOTRE SOLUTION À LA QUESTION 2 ICI
    '''
    from util import Queue
    # FIFO data structure
    return searchAlgorithmWithoutPriority(problem, Queue())


def uniformCostSearch(problem):
    """Search the node of least total cost first."""


    '''
        INSÉREZ VOTRE SOLUTION À LA QUESTION 3 ICI
    '''

    from util import PriorityQueue
    
    state = problem.getStartState() # starting state
    pathList = PriorityQueue()
    pathList.push([(state, '', 1)], 0)
    visitedStates = []
    
    while not pathList.isEmpty():
        state = pathList.pop()
        lastNode = state[-1][0] 

        if problem.isGoalState(lastNode): 
            return [path[1] for path in state if path[1] != '']
        elif lastNode not in visitedStates: 
            visitedStates.append(lastNode)
            successorList = problem.getSuccessors(lastNode)
            for successor in successorList:
                if successor[0] not in visitedStates: 
                    newPath = state[:]
                    newPath.append(successor)
                    priorityPath = problem.getCostOfActions([path[1] for path in newPath if path[1] != ''])
                    pathList.update(newPath, priorityPath) # Add new path to the list
    return []      

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    '''
        INSÉREZ VOTRE SOLUTION À LA QUESTION 4 ICI
    '''
    from util import PriorityQueue
    state = problem.getStartState() # starting state
    pathList = PriorityQueue() 
    pathList.push([(state, '', 1)], 0)
    visitedStates = []

    while not pathList.isEmpty():
        state = pathList.pop()
        lastNode = state[-1][0] 
        if problem.isGoalState(lastNode):
            return [path[1] for path in state if path[1] != '']
        elif lastNode not in visitedStates: 
            visitedStates.append(lastNode)
            successorList = problem.getSuccessors(lastNode)
            for successor in successorList:
                if successor[0] not in visitedStates: 
                    newPath = state[:]
                    newPath.append(successor)
                    priorityCost = problem.getCostOfActions([path[1] for path in newPath if path[1] != '']) + heuristic(successor[0], problem)
                    pathList.update(newPath, priorityCost) # Add new path to the list 
    return [] 

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
