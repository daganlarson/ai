import random 
import math
from collections import defaultdict
from Game import State, Game
import sys

C = 1.4

## Utility to find element of seq that maximizes fn
def argmax(seq, fn):
    return seq[max(enumerate([fn(x) for x in seq]),key=lambda p:p[1])[0]]

## Choose a random legal move
def random_decision(state, game):
    return random.choice(game.legal_moves(state))


## MiniMax decision (figure 5.3)
def minimax_decision(state: State, game: Game):
    player = game.to_move(state)

    def max_value(state : State):
        ### ... you fill this in ...
        ### Hint: you can make use of
        ###   game.terminal_test(state)
        ###   game.utility(state,player)
        ###   game.sucessors(state)
        if game.terminal_test(state):
            return game.utility(state, player), None
        
        utility = -sys.maxsize

        for newAction, newState in game.successors(state):
            newUtility, newAction = min_value(newState)
            if newUtility > utility:
                utility = newUtility
                action = newAction
        
        return utility, action


    def min_value(state: State):
        ### ... you fill this in ...
        if game.terminal_test(state):
            return game.utility(state, player), None
        
        utility = sys.maxsize

        for newAction, newState in game.successors(state):
            newUtility, newAction = max_value(newState)
            if newUtility < utility:
                utility = newUtility
                action = newAction
        
        return utility, action
        
    # Body of minimax_decision starts here:
    action, state = argmax(game.successors(state), lambda x: min_value(x[1]))
    return action

##
## MiniMax with Alpha-Beta pruning (figure 5.7)
## 
def alphabeta_decision(state: State, game: Game):

    player = game.to_move(state)

    def max_value(state: State, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player), None
        
        utility = -sys.maxsize

        for newAction, newState in game.successors(state):
            newUtility, aAction = min_value(newState, alpha, beta)
            if newUtility > utility:
                utility = newUtility
                action = newAction 
                alpha = max([alpha, utility])

            if utility >= beta:
                return utility, action
            
        return utility, action

    def min_value(state, alpha, beta):
        ### ... you fill this in ...
        if game.terminal_test(state):
            return game.utility(state, player), None
        
        utility = sys.maxsize 

        for newAction, newState in game.successors(state):
            newUtility, aAction = max_value(newState, alpha, beta)
            if newUtility < utility:
                utility = newUtility
                action = newAction
                beta = min([beta, utility])
            if utility <= alpha:
                return utility, action 
        
        return utility, action 


    action, state = argmax(game.successors(state),
                           lambda x: min_value(x[1], float('-inf'), float('inf')))
    return action

##
## MiniMax with Alpha-Beta pruning, cutoff and evaluation (section 5.4.2)
##
def alphabeta_cutoff_decision(state, game, d=4):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""

    player = game.to_move(state)

    def max_value(state, alpha, beta, depth):
        if game.terminal_test(state):
            return game.utility(state, player), None 
        elif depth >= d:
            return eval(state, beta), None
        
        utility = -sys.maxsize
        action = None

        for newAction, newState in game.successors(state):
            newUtility, _ = min_value(newState, alpha, beta, depth + 1)
            if newUtility > utility:
                utility = newUtility
                action = newAction
            alpha = max([alpha, utility])
            if utility >= beta:
                return utility, action
        
        return utility, action 

    def min_value(state, alpha, beta, depth):
        if game.terminal_test(state) or depth >= d:
            if game.terminal_test(state):
                return game.utility(state, player), None 
            else:
                return eval(state, alpha, beta), None
        
        utility = sys.maxsize 
        action = None

        for newAction, newState in game.successors(state):
            newUtility, aAction = max_value(newState, alpha, beta, depth + 1)
            if newUtility < utility:
                utility = newUtility
                action = newAction
            beta = min([beta, utility])
            if utility <= alpha:
                return utility, action 
        
        return utility, action 

    def eval(state, alpha, beta):
        return alpha + beta / 2
        
    action, state = argmax(game.successors(state),
                           lambda x: min_value(x[1], float('-inf'), float('inf'), 0))
    return action

## Simulate a game starting at state, returning utility
## Uses a random playout policy
def simulate(state, game):
    while True:
        if game.terminal_test(state):
            return game.utility(state,game.to_move(state))            
        a,s  = random.choice(game.successors(state))
        state = game.make_move(a,state)
    
def pure_mc_decision(state, game, nplayouts=10):
    score = dict()
    for a,s in game.successors(state):
        score[a] = 0
        for _ in range(nplayouts):
            score[a] += simulate(s,game)
    return max(score, key=score.get)

class MCTS_Node:
    def __init__(self,state,parent=None):
        self.state = state        
        self.parent=parent
        self.children = []
        
## Monte Carlo Tree Search (fig 5.11 on page 163)
def mcts_decision(state, game, nplayouts=10):
    tree = MCTS_Node(state)
    # A dictionary that maps states to playout count
    N = defaultdict(int)
    # A dictionary that maps states to total playout utility
    U = defaultdict(int)    

    ## Find a leaf of tree using UCT selection policy
    def select(node: MCTS_Node):
        while len(node.children) != 0:
            if len(node.children) < len(game.successors(node.state)):
                return node
            
            node = argmax(node.children, utc)

        return node

    def utc(child):
        try: 
            return U[child] / N[child] + C * math.sqrt(math.log2(N[child.parent]) / N[child]) 
        except ZeroDivisionError:
            return 0
        
    ## Grow the search tree by generating children of this node
    def expand(node: MCTS_Node):
        expandedStates = []
        for child in node.children:
            expandedStates.append(child.state)

        for move, state in game.successors(node.state):
            if state not in expandedStates:
                newNode = MCTS_Node(state, node)
                node.children.append(newNode)
                U[state] = 0
                N[state] = 0
                return newNode
        
        return node
            
    ## send reward back up the tree
    def backpropagate(result,node):
        ## ... you fill this in ...
        while node.parent != None:
            N[node.state] += 1
            U[node.state] += result
            node = node.parent

    for _ in range(nplayouts):
        leaf = select(tree)
        child = expand(leaf)
        result = simulate(child.state,game)
        backpropagate(result,child)

    moves = game.successors(state)
    score = [U[s]/N[s] if N[s] != 0 else float('-inf') for a,s in moves]
    maxindex = max(enumerate(score),key=lambda x:x[1])[0]

    ## return the move from state with best relative score
    return moves[maxindex][0]


