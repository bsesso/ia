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
    from game import Directions
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

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """

    frontier = util.Stack()
    frontier.push(problem.getStartState())
    explored = []
    parents = {}

    while (not frontier.isEmpty()):
        currentState = frontier.pop()
        # print "frontier: ", frontier.list
        # print "current:  ", currentState
        if (problem.isGoalState(currentState)):
            child = currentState
            startState = problem.getStartState()
            moves = []
            while (child != startState):
                # print "child:  ", child
                # print "parent: ", parents[child][0]
                moves.insert(0, parents[child][1])
                child = parents[child][0]
            return moves

        explored.append(currentState)
        for successor in problem.getSuccessors(currentState):
            if (not successor[0] in explored):
            # if (not successor[0] in explored) and (not successor[0] in frontier.list):
                frontier.push(successor[0])
                parents[successor[0]] = [currentState, successor[1]]

    return []


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    frontier = util.Queue()
    frontier.push(problem.getStartState())
    explored = []
    parents = {}

    while (not frontier.isEmpty()):
        currentState = frontier.pop()
        if (problem.isGoalState(currentState)):
            child = currentState
            startState = problem.getStartState()
            moves = []
            while (child != startState):
                moves.insert(0, parents[child][1])
                child = parents[child][0]
            return moves

        explored.append(currentState)
        for successor in problem.getSuccessors(currentState):
            if (not successor[0] in explored) and (not successor[0] in frontier.list):
                frontier.push(successor[0])
                parents[successor[0]] = [currentState, successor[1]]

    return []


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    frontier = util.PriorityQueue()
    frontier.push(problem.getStartState(), 0)
    explored = []
    parents = {}
    parents[problem.getStartState()] = [None, None, 0]

    while (not frontier.isEmpty()):
        currentState = frontier.pop()
        if (problem.isGoalState(currentState)):
            child = currentState
            startState = problem.getStartState()
            moves = []
            while (child != startState):
                moves.insert(0, parents[child][1])
                child = parents[child][0]
            return moves

        explored.append(currentState)
        for successor in problem.getSuccessors(currentState):
            child = successor[0]
            cost = successor[2] + parents[currentState][2]
            if (not child in explored) and (not child in map(lambda x: x[2], frontier.heap)):
                frontier.push(child, cost)
                parents[child] = [currentState, successor[1], cost]
            elif (child in map(lambda x: x[2], frontier.heap) and cost < parents[child][2]):
                frontier.update(child, cost)
                parents[child] = [currentState, successor[1], cost]


    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    frontier = util.PriorityQueue()
    frontier.push(problem.getStartState(), 0)
    explored = []
    parents = {}
    parents[problem.getStartState()] = [None, None, 0]

    while (not frontier.isEmpty()):
        currentState = frontier.pop()
        if (problem.isGoalState(currentState)):
            child = currentState
            startState = problem.getStartState()
            moves = []
            while (child != startState):
                moves.insert(0, parents[child][1])
                child = parents[child][0]
            return moves

        explored.append(currentState)
        for successor in problem.getSuccessors(currentState):
            child = successor[0]
            cost = successor[2] + parents[currentState][2]
            if (not child in explored) and (not child in map(lambda x: x[2], frontier.heap)):
                frontier.push(child, cost + heuristic(child, problem))
                parents[child] = [currentState, successor[1], cost]
            elif (child in map(lambda x: x[2], frontier.heap) and cost < parents[child][2]):
                frontier.update(child, cost + heuristic(child, problem))
                parents[child] = [currentState, successor[1], cost]


    return []



def learningRealTimeAStar(problem, heuristic=nullHeuristic):
    """Execute a number of trials of LRTA* and return the best plan found."""
    parents = {}
    h = {}
    currentState = problem.getStartState()
    h[currentState] = heuristic(currentState, problem)
    moves = {}

    while (not problem.isGoalState(currentState)):
        minCost = float("inf")
        for successor in problem.getSuccessors(currentState):
            child = successor[0]
            cost = successor[2]
            if child in h:
                cost += h[child]
            else:
                cost += heuristic(child, problem)
           
            if cost < minCost:
                minCost =  cost
                nextState = child
                move = (successor[1], nextState)

        if minCost > h[currentState]:
            h[currentState] = minCost

        moves[currentState] = move
        currentState = nextState
        if not currentState in h:
            h[currentState] = heuristic(currentState, problem)

    moveList = []
    currentState = problem.getStartState()
    while (not problem.isGoalState(currentState)):
        moveList.append(moves[currentState][0])
        currentState = moves[currentState][1]

    return moveList

    # MAXTRIALS = ...
    

# Abbreviations 
# *** DO NOT CHANGE THESE ***
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
lrta = learningRealTimeAStar
