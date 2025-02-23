import bisect, sys
import numpy as np
from math import radians, cos, sin, asin, sqrt

from SearchProblem import *
from SearchAnimator import *

## ############################ #
## Uninformed Search Algorithms #
## ############################ #

def graph_search(problem, fringe, callback):
    """Search through the successors of a problem to find a goal.
    The argument fringe is some kind of empty container.
    If two paths reach a state, only use the best one. [Fig. 3.5]"""
    Node.nodecount = 0
    closed = {}    
    fringe.append(Node(problem.initial))
    while fringe:
        node = fringe.pop()
        if problem.goal_test(node.state):
            callback(problem.graph,node,fringe,closed,True)
            return node
        if node.state not in closed:
            closed[node.state] = True
            fringe.extend(node.expand(problem))
            callback(problem.graph,node,fringe,closed,False)
    return None

def breadth_first_graph_search(problem,callback):
    """Search the shallowest nodes in the search tree first. [p 77]"""
    ### YOU IMPLEMENT THIS ###
    Node.nodecount = 0
    closed = {}
    queue = FIFOQueue()
    queue.append(Node(problem.initial))
    while queue:
        node = queue.pop()
        if problem.goal_test(node.state):
            callback(problem.graph,node,queue,closed,True)
            return node
        if node.state not in closed:
            closed[node.state] = True 
            queue.extend(node.expand(problem))
            callback(problem.graph,node,queue,closed,False)
    return None

            

def depth_first_graph_search(problem,callback):
    """Search the deepest nodes in the search tree first. [p 78]"""
    ### YOU IMPLEMENT THIS ###
    Node.nodecount = 0
    closed = {}
    stack = Stack()
    stack.append(Node(problem.initial))
    while stack:
        node = stack.pop()
        if problem.goal_test(node.state):
            callback(problem.graph,node,stack,closed,True)
            return node
        if node.state not in closed:
            closed[node.state] = True 
            stack.extend(node.expand(problem))
            callback(problem.graph,node,stack,closed,False)
    return None

def depth_limited_search(problem, limit, callback):
    """Depth-first search with a depth limit. [p 81]"""
    ### YOU IMPLEMENT THIS ###	
    Node.nodecount = 0
    closed = {}
    stack = Stack()
    stack.append(Node(problem.initial))
    cutoff = False
    while stack:
        node = stack.pop()
        if problem.goal_test(node.state):
            callback(problem.graph,node,stack,closed,True)
            return node
        if node.state not in closed:
            closed[node.state] = True 
        if node.depth < limit:
            stack.extend(node.expand(problem))
        if node.depth >= limit:
            cutoff = True
        callback(problem.graph,node,stack,closed,False)
    if cutoff:
        return 'cutoff'
    return None

def iterative_deepening_search(problem,callback):
    """Iterative deepening using depth limited search [p 81]"""
    ### YOU IMPLEMENT THIS ###
    for depth in range(1, sys.maxsize):
        result = depth_limited_search(problem, depth, callback)
        if result != None and result != 'cutoff':
            return result

   
## ###################################### #
## Informed (Heuristic) Search Algorithms #
## ###################################### #

def best_first_graph_search(problem, f, callback):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have depth-first search."""
    ### YOU IMPLEMENT THIS ###
    Node.nodecount = 0
    closed = {}
    queue = PriorityQueue(f=f)
    queue.append(Node(problem.initial))
    while queue:
        node = queue.pop()
        #print(node.state, problem.h(node))
        if problem.goal_test(node.state):
            callback(problem.graph,node,queue,closed,True)
            return node
        if node.state not in closed:
            closed[node.state] = True 
            queue.extend(node.expand(problem))
            callback(problem.graph,node,queue,closed,False)
    return None

def greedy_best_first_graph_search(problem, callback):
    """Best-first graph search with f(n)=h(n). [p 85]"""
    ### YOU IMPLEMENT THIS ###
    best_first_graph_search(problem, lambda n: problem.h(n), callback)
    
    
def astar_search(problem, callback, h=None):
    """Best-first graph search with f(n) = g(n)+h(n). [p 85]"""
    ### YOU IMPLEMENT THIS ###
    best_first_graph_search(problem, lambda n: problem.h(n) + n.path_cost, callback)


## Main loop
if __name__ == "__main__":
    algs = {"BFS":breadth_first_graph_search,
            "DFS":depth_first_graph_search,
            "IDS":iterative_deepening_search,
            "greedy":greedy_best_first_graph_search,
            "A*":astar_search}
    animate = SearchAnimator(algs)
    animate.run()
