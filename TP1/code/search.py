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

def searchAlgorithmWithoutPriority(problem, data_structure):
    #Shared code between BFS and DFS

    s = problem.getStartState() # starting state
    data_structure.push([(s, '', 1)]) # Initial state
    V = [] # Visited states
    
    while not data_structure.isEmpty():
        s = data_structure.pop()
        last_node = s[-1][0] 

        if problem.isGoalState(last_node): 
            return [path[1] for path in s if path[1] != '']
        elif last_node not in V: 
            V.append(last_node)
            C = problem.getSuccessors(last_node)
            for successor in C:
                if successor[0] not in V: 
                    new_path = list(s)
                    new_path.append(successor) # Add the successor to the new path
                    data_structure.push(new_path) 
    return [] #empty list?

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

    L = Stack() # LIFO data structure
    return searchAlgorithmWithoutPriority(problem, L)
    

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""


    '''
        INSÉREZ VOTRE SOLUTION À LA QUESTION 2 ICI
    '''
    # Inspired by https://stackoverflow.com/a/25583948
    from util import Queue
    
    L = Queue() # LIFO data structure
    return searchAlgorithmWithoutPriority(problem, L)


def uniformCostSearch(problem):
    """Search the node of least total cost first."""


    '''
        INSÉREZ VOTRE SOLUTION À LA QUESTION 3 ICI
    '''

    from util import PriorityQueue
    
    s = problem.getStartState() # starting state
    L = PriorityQueue()
    L.push([(s, '', 1)], 0) # Initial state
    V = [] # Visited states
    
    while not L.isEmpty():
        s = L.pop()
        last_node = s[-1][0] 

        if problem.isGoalState(last_node): 
            return [path[1] for path in s if path[1] != '']
        elif last_node not in V: 
            V.append(last_node)
            C = problem.getSuccessors(last_node)
            for successor in C:
                if successor[0] not in V: 
                    new_path = list(s)
                    new_path.append(successor) # Add the successor to the new path
                    priority_path = problem.getCostOfActions([path[1] for path in new_path if path[1] != ''])
                    L.push(new_path, priority_path) # Add new path to the queue
    return [] #empty list?       

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
    s = problem.getStartState() # starting state
    L = PriorityQueue() 
    L.push([(s, '', 1)], 0)
    V = [] # Visited states
    
    while not L.isEmpty():
        s = L.pop()
        last_node = s[-1][0] 

        if problem.isGoalState(last_node): 
            return [path[1] for path in s if path[1] != '']
        elif last_node not in V: 
            V.append(last_node)
            C = problem.getSuccessors(last_node)
            for successor in C:
                if successor[0] not in V: # If successor hasn't been visited yet c
                    new_path = list(s)
                    new_path.append(successor) # Add the successor to the new path
                    estimate_cost = heuristic(last_node, problem)
                    combo_cost = problem.getCostOfActions([path[1] for path in new_path if path[1] != '']) + estimate_cost
                    L.push(new_path, combo_cost) # Add new path to the queue 
    return [] 

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
