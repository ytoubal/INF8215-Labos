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
    visited = set()
    s = problem.getStartState()
    L = Stack()
    L.push([(s, '', 1)])
    
    while not L.isEmpty():
        s = L.pop()
        last_node = s[-1] 
        if problem.isGoalState(last_node[0]): return [path[1] for path in s if path[1] != '']
        else: 
            C = problem.getSuccessors(last_node[0])
            for successor in C:
                if successor not in visited: 
                    new_path = list(s)
                    new_path.append(successor) # Add the successor to the new path
                    L.push(new_path) # Add new path to the queue
                    visited.add(successor) 
    return [] #empty list?

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""


    '''
        INSÉREZ VOTRE SOLUTION À LA QUESTION 2 ICI
    '''
    # Inspired by https://stackoverflow.com/a/25583948
    from util import Queue
    
    s = problem.getStartState() # starting state
    L = Queue() # FIFO data structure
    L.push([(s, '', 1)]) # Initial state
    V = set() # Visited states

    while not L.isEmpty():
        s = L.pop() # First element of queue
        last_node = s[-1] # Last node of the path

        if problem.isGoalState(last_node[0]): # If we reached the end state
            return [path[1] for path in s if path[1] != ''] # Return the path to the end state
        else:
            C = problem.getSuccessors(last_node[0])
            for successor in C:
                if successor not in V: # If successor hasn't been visited yet c
                    new_path = list(s)
                    new_path.append(successor) # Add the successor to the new path
                    L.push(new_path) # Add new path to the queue
                    V.add(successor) # Mark the successor as visited       
    return       


def uniformCostSearch(problem):
    """Search the node of least total cost first."""


    '''
        INSÉREZ VOTRE SOLUTION À LA QUESTION 3 ICI
    '''

    from util import PriorityQueue
    
    s = problem.getStartState() # starting state
    L = PriorityQueue() # FIFO data structure
    L.push([(s, '', 1)], 0) # Initial state
    V = set() # Visited states

    while not L.isEmpty():
        s = L.pop() # First element of queue
        last_node = s[-1] # Last node of the path

        if problem.isGoalState(last_node[0]): # If we reached the end state
            return [path[1] for path in s if path[1] != ''] # Return the path to the end state
        else:
            C = problem.getSuccessors(last_node[0])
            for successor in C:
                if successor not in V: # If successor hasn't been visited yet c
                    new_path = list(s)
                    new_path.append(successor) # Add the successor to the new path
                    priority_path = problem.getCostOfActions([path[1] for path in new_path if path[1] != ''])
                    L.push(new_path, priority_path) # Add new path to the queue
                    V.add(successor) # Mark the successor as visited       
    return       

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
    V = set() # Visited states
    
    while not L.isEmpty():
        s = L.pop() # First element of queue
        last_node = s[-1] # Last node of the path

        if problem.isGoalState(last_node[0]): # If we reached the end state
            return [path[1] for path in s if path[1] != ''] # Return the path to the end state
        else:
            C = problem.getSuccessors(last_node[0])
            for successor in C:
                if successor not in V: # If successor hasn't been visited yet c
                    new_path = list(s)
                    new_path.append(successor) # Add the successor to the new path
                    estimate_cost = heuristic(last_node[0], problem)
                    combo_cost = problem.getCostOfActions([path[1] for path in new_path if path[1] != '']) + estimate_cost
                    L.push(new_path, combo_cost) # Add new path to the queue
                    V.add(successor) # Mark the successor as visited       
    return  

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
