# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def traverse(problem, frontier, heuristic, astar):
    """
    This method is used to traverse the graph, and return the path for DFS, BFS, UCS, and A* algorithms.
    Given the similarities among the algorithms, I thought using a method for all four would be practical.
    The method takes four arguments.
    problem being the original argument given by the assignment.
    frontier being the respective data structure being used in a given algorithm
    heuristic is only passed by A*, otherwise it's None.
    and astar is a boolean value to tell the method whether to consider a heuristic.
    """
    explored = set([])
    try:  # for DFS and BFS
        frontier.push((problem.getStartState(), [], 0))
    except:  # for UCS and A*
        frontier.push((problem.getStartState(), [], 0), 0)
    while not frontier.isEmpty():  # while nodes are to be expanded
        state, path, cost = frontier.pop()  # pop state, and current path into individual variables
        if state not in explored:  # only begin if the state hasn't already been explored
            explored.add(state)  # add current node to explored set
            if problem.isGoalState(state):  # if we reach a goal state, return the path
                return path
            for children, updated_path, updated_cost in problem.getSuccessors(state):  # expand
                if children not in explored:  # if node hasn't been explored, push onto frontier
                    try:  # for DFS and BFS
                        frontier.push((children, path + [updated_path], cost + updated_cost))  # update paths/costs
                    except:  # for UCS and A*
                        if astar:  # for A* algorithm, incorporating a heuristic in the cost value.
                            heuristic_value = heuristic(children, problem)
                            frontier.push((children, path + [updated_path], cost + updated_cost), cost +
                                          updated_cost + heuristic_value)
                        else:  # for UCS
                            frontier.push((children, path + [updated_path], cost + updated_cost), cost + updated_cost)

    return []  # return empty list if no path found


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    frontier = util.Stack()  # create stack for DFS
    return traverse(problem, frontier, None, False)


def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    frontier = util.Queue()  # create queue for BFS
    return traverse(problem, frontier, None, False)


def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    frontier = util.PriorityQueue()  # create Priority queue for UCS
    return traverse(problem, frontier, None, False)


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    frontier = util.PriorityQueue()  # create priority queue for A*
    return traverse(problem, frontier, heuristic, True)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
