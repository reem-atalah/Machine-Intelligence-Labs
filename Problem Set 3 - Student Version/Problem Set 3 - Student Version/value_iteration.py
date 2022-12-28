from typing import Dict, Optional
from agents import Agent
from environment import Environment
from mdp import MarkovDecisionProcess, S, A
import json

from helpers.utils import NotImplemented

# This is a class for a generic Value Iteration agent
class ValueIterationAgent(Agent[S, A]):
    mdp: MarkovDecisionProcess[S, A] # The MDP used by this agent for training 
    utilities: Dict[S, float] # The computed utilities
                                # The key is the string representation of the state and the value is the utility
    discount_factor: float # The discount factor (gamma)

    def __init__(self, mdp: MarkovDecisionProcess[S, A], discount_factor: float = 0.99) -> None:
        super().__init__()
        self.mdp = mdp
        self.utilities = {state:0 for state in self.mdp.get_states()} # We initialize all the utilities to be 0
        self.discount_factor = discount_factor
    
    # Given a state, compute its utility using the bellman equation
    # if the state is terminal, return 0
    def compute_bellman(self, state: S) -> float:
        #TODO: Complete this function
        # NotImplemented()
        if self.mdp.is_terminal(state):
            return 0
        else:            
            # Bellman equation for value iteration agent is: U(s) = max_a sum_s' P(s'|s,a) * (R(s,a,s') + gamma * U(s')) 
            # where U(s) is the utility of state s, a is the action, s' is the next state, P(s'|s,a) is the probability of next state s' given state s and action a, R(s,a,s') is the reward for state s, action a and next state s', gamma is the discount factor
            # self.mdp.get_successor(state, action)[next_state]: P(s'|s,a)
            # self.mdp.get_reward(state, action, next_state): R(s,a,s')
            # self.utilities[next_state]: U(s')
            # self.discount_factor: gamma
            # sum([self.mdp.get_successor(state, action)[next_state] * (self.mdp.get_reward(state, action, next_state) + self.discount_factor * self.utilities[next_state]) for next_state in self.mdp.get_successor(state, action)]): sum_s' P(s'|s,a) * (R(s,a,s') + gamma * U(s'))
            # [self.mdp.get_successor(state, action)[next_state] * (self.mdp.get_reward(state, action, next_state) + self.discount_factor * self.utilities[next_state]) for next_state in self.mdp.get_successor(state, action)]: list of sum_s' P(s'|s,a) * (R(s,a,s') + gamma * U(s'))

            return max([sum([self.mdp.get_successor(state, action)[next_state] * (self.mdp.get_reward(state, action, next_state) + self.discount_factor * self.utilities[next_state]) for next_state in self.mdp.get_successor(state, action)]) for action in self.mdp.get_actions(state)])

    
    # Applies a single utility update
    # then returns True if the utilities has converged (the maximum utility change is less or equal the tolerance)
    # and False otherwise
    def update(self, tolerance: float = 0) -> bool:
        #TODO: Complete this function
        # NotImplemented()
        # update the utilities of all the states using the bellman equation and store the new utilities in a temporary dictionary (new_utilities) 
        # then compare the maximum utility change with the tolerance and return True if the maximum utility change is less or equal the tolerance and False otherwise 
        # NOTE: you should not update the utilities of the states directly, instead, you should update the utilities in the temporary dictionary (new_utilities) and then compare the maximum utility change with the tolerance
        # NOTE: you should not compare the utilities of the states directly, instead, you should compare the utilities in the temporary dictionary (new_utilities) with the utilities in the agent (self.utilities)
        # NOTE: you should not update the utilities of the states directly, instead, you should update the utilities in the temporary dictionary (new_utilities) and then update the utilities in the agent (self.utilities)
        new_utilities = {state: self.compute_bellman(state) for state in self.mdp.get_states()}
        max_utility_change = max([abs(new_utilities[state] - self.utilities[state]) for state in self.mdp.get_states()])
        if max_utility_change <= tolerance:
            self.utilities = new_utilities
            return True
        else:
            self.utilities = new_utilities
            return False


    # This function applies value iteration starting from the current utilities stored in the agent and stores the new utilities in the agent
    # NOTE: this function does incremental update and does not clear the utilities to 0 before running
    # In other words, calling train(M) followed by train(N) is equivalent to just calling train(N+M)
    def train(self, iterations: Optional[int] = None, tolerance: float = 0) -> int:
        iteration = 0
        while iterations is None or iteration < iterations:
            iteration += 1
            if self.update(tolerance):
                break
        return iteration
    
    # Given an environment and a state, return the best action as guided by the learned utilities and the MDP
    # If the state is terminal, return None
    def act(self, env: Environment[S, A], state: S) -> A:
        #TODO: Complete this function
        # NotImplemented()
        if self.mdp.is_terminal(state):
            return None
        else:
            # return the action that maximizes the utility of the next state (best action as guided by the learned utilities and the MDP)
            # self.mdp.get_successor(state, action)[next_state]: P(s'|s,a)
            # self.mdp.get_reward(state, action, next_state): R(s,a,s')
            # self.utilities[next_state]: U(s')
            # self.discount_factor: gamma
            # sum([self.mdp.get_successor(state, action)[next_state] * (self.mdp.get_reward(state, action, next_state) + self.discount_factor * self.utilities[next_state]) for next_state in self.mdp.get_successor(state, action)]): sum_s' P(s'|s,a) * (R(s,a,s') + gamma * U(s'))
            # [self.mdp.get_successor(state, action)[next_state] * (self.mdp.get_reward(state, action, next_state) + self.discount_factor * self.utilities[next_state]) for next_state in self.mdp.get_successor(state, action)]: list of sum_s' P(s'|s,a) * (R(s,a,s') + gamma * U(s'))

            return max([action for action in self.mdp.get_actions(state)], key=lambda action: sum([self.mdp.get_successor(state, action)[next_state] * (self.mdp.get_reward(state, action, next_state) + self.discount_factor * self.utilities[next_state]) for next_state in self.mdp.get_successor(state, action)]))
    
    # Save the utilities to a json file
    def save(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'w') as f:
            utilities = {self.mdp.format_state(state): value for state, value in self.utilities.items()}
            json.dump(utilities, f, indent=2, sort_keys=True)
    
    # loads the utilities from a json file
    def load(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'r') as f:
            utilities = json.load(f)
            self.utilities = {self.mdp.parse_state(state): value for state, value in utilities.items()}
