from typing import Tuple
from game import HeuristicFunction, Game, S, A
from helpers.utils import NotImplemented

#TODO: Import any modules you want to use
import math

# All search functions take a problem, a state, a heuristic function and the maximum search depth.
# If the maximum search depth is -1, then there should be no depth cutoff (The expansion should not stop before reaching a terminal state) 

# All the search functions should return the expected tree value and the best action to take based on the search results

# This is a simple search function that looks 1-step ahead and returns the action that lead to highest heuristic value.
# This algorithm is bad if the heuristic function is weak. That is why we use minimax search to look ahead for many steps.
def greedy(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    agent = game.get_turn(state)
    
    terminal, values = game.is_terminal(state)
    if terminal: return values[agent], None

    actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
    value, _, action = max((heuristic(game, state, agent), -index, action) for index, (action , state) in enumerate(actions_states))
    return value, action 

# Apply Minimax search and return the game tree value and the best action
# Hint: There may be more than one player, and in all the testcases, it is guaranteed that 
# game.get_turn(state) will return 0 (which means it is the turn of the player). All the other players
# (turn > 0) will be enemies. So for any state "s", if the game.get_turn(s) == 0, it should a max node,
# and if it is > 0, it should be a min node. Also remember that game.is_terminal(s), returns the values
# for all the agents. So to get the value for the player (which acts at the max nodes), you need to
# get values[0].
def minimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Write this function
    agent = game.get_turn(state) #returns the turn of the player. 0 for player, 1 for monster, 2 for monster 2, etc. 

    terminal, values = game.is_terminal(state) #returns if the state is terminal and return the values for all the agents
    if terminal: return values[agent], None

    if max_depth == 0: #if we have reached the maximum depth
        if agent == 0: #if it is the player's turn (max node) return the heuristic value
            return heuristic(game, state, agent), None
        else: #if it is the monster's turn (min node) return the negative of the heuristic value
            return -heuristic(game, state, agent), None

    #get all the actions and the resulting states
    actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)] 

    if agent == 0: #if it is the player's turn (max node) return the action that leads to the maximum value of the heuristic function 
        value, _, action = max((minimax(game, state, heuristic, max_depth-1)[0], -index, action) for index, (action , state) in enumerate(actions_states))
    else: #if it is the monster's turn (min node) return the action that leads to the minimum value of the heuristic function
        value, _, action = min((minimax(game, state, heuristic, max_depth-1)[0], -index, action) for index, (action , state) in enumerate(actions_states))

    return value, action 

# Apply Alpha Beta pruning and return the tree value and the best action
# Hint: Read the hint for minimax.
def alphabeta(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Write this function
    # NotImplemented() 
    
    def alphabeta_helper(state, alpha, beta, depth):
        agent = game.get_turn(state) #returns the turn of the player. 0 for player, 1 for monster, 2 for monster 2, etc.

        terminal, values = game.is_terminal(state) #returns if the state is terminal and return the values for all the agents
        if terminal: return values[agent], None

        if depth == 0: #if we have reached the maximum depth
            if agent == 0: #if it is the player's turn (max node) return the heuristic value
                return heuristic(game, state, agent), None
            else: #if it is the monster's turn (min node) return the negative of the heuristic value
                return -heuristic(game, state, agent), None

        #get all the actions and the resulting states
        # actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]

        if agent == 0: #if it is the player's turn (max node) return the action that leads to the maximum value of the heuristic function
            max_eval=-math.inf
            max_action=None
            for action in game.get_actions(state):
                eval, _ = alphabeta_helper(game.get_successor(state, action), alpha, beta, depth-1)
                if eval > max_eval:
                    max_eval = eval
                    max_action = action
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, max_action

        else: 
            min_eval=math.inf
            min_action=None
            for action in game.get_actions(state):
                eval, _ = alphabeta_helper(game.get_successor(state, action), alpha, beta, depth-1)
                if eval < min_eval:
                    min_eval = eval
                    min_action = action
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, min_action
   

    return alphabeta_helper(state, -math.inf, math.inf, max_depth)


# Apply Alpha Beta pruning with move ordering and return the tree value and the best action
# Hint: Read the hint for minimax.
def alphabeta_with_move_ordering(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Write this function
    # NotImplemented()
    def alphabeta_helper(state, alpha, beta, depth):
        agent = game.get_turn(state) #returns the turn of the player. 0 for player, 1 for monster, 2 for monster 2, etc.

        terminal, values = game.is_terminal(state) #returns if the state is terminal and return the values for all the agents
        if terminal: 
            if agent == 0:
                return values[agent], None #if it is terminal return the value for the player
            else:
                return -values[agent], None


        if depth == 0: #if we have reached the maximum depth
            if agent == 0: #if it is the player's turn (max node) return the heuristic value
                return heuristic(game, state, agent), None
            else: #if it is the monster's turn (min node) return the negative of the heuristic value
                return -heuristic(game, state, agent), None

        if agent == 0: #if it is the player's turn (max node) return the action that leads to the maximum value of the heuristic function
            #get all the actions and the resulting states
            actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
            #sort the actions based on the heuristic value of the resulting states (descending order for max node, ascending order for min node) 
            sorted_actions_states = sorted(actions_states, key=lambda x: heuristic(game, x[1], agent), reverse=agent==0)
            max_eval=-math.inf
            max_action=None
            for action, state in sorted_actions_states:
                eval, _ = alphabeta_helper(state, alpha, beta, depth-1)
                if eval > max_eval:
                    max_eval = eval
                    max_action = action
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, max_action

        else:
            #get all the actions and the resulting states
            actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
            #sort the actions based on the heuristic value of the resulting states (descending order for max node, ascending order for min node) 
            sorted_actions_states = sorted(actions_states, key=lambda x: -heuristic(game, x[1], agent), reverse=agent==0)
            min_eval=math.inf
            min_action=None
            for action, state in sorted_actions_states:
                eval, _ = alphabeta_helper(state, alpha, beta, depth-1)
                if eval < min_eval:
                    min_eval = eval
                    min_action = action
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, min_action

    return alphabeta_helper(state, -math.inf, math.inf, max_depth) 

# Apply Expectimax search and return the tree value and the best action
# Hint: Read the hint for minimax, but note that the monsters (turn > 0) do not act as min nodes anymore,
# they now act as chance nodes (they act randomly).
def expectimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Write this function
    # NotImplemented()
    # Chance nodes take the average of all available values giving us the ‘expected value’ of the node.
    
    def expectimax_helper(state, depth):
        agent = game.get_turn(state) #returns the turn of the player. 0 for player, 1 for monster, 2 for monster 2, etc.

        terminal, values = game.is_terminal(state) #returns if the state is terminal and return the values for all the agents
        if terminal: 
            if agent == 0:
                return values[agent], None #if it is terminal return the value for the player
            else:
                return -values[agent], None

        if depth == 0: #if we have reached the maximum depth
            if agent == 0: #if it is the player's turn (max node) return the heuristic value
                return heuristic(game, state, agent), None
            else: #if it is the monster's turn (min node) return the negative of the heuristic value
                return -heuristic(game, state, agent), None

        if agent == 0: #if it is the player's turn (max node) return the action that leads to the maximum value of the heuristic function (as minimax)
            max_eval=-math.inf
            max_action=None
            for action in game.get_actions(state):
                eval, _ = expectimax_helper(game.get_successor(state, action), depth-1)
                if eval > max_eval:
                    max_eval = eval
                    max_action = action
            return max_eval, max_action

        else:  #if it is the monster's turn (chance node) return the action that leads to the average value of the heuristic function
            total_eval=0
            for action in game.get_actions(state):
                eval, _ = expectimax_helper(game.get_successor(state, action), depth-1)
                total_eval += eval 

            # assuming all nodes have equal probability of being chosen 
            # we can return any action since they all have the same value
            return total_eval/len(game.get_actions(state)) , action  #return the average value of the heuristic function
   

    return expectimax_helper(state, max_depth)