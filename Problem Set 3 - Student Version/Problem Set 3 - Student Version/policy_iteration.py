from typing import Dict, Optional
from agents import Agent
from environment import Environment
from mdp import MarkovDecisionProcess, S, A
import json
import numpy as np

from helpers.utils import NotImplemented

# This is a class for a generic Policy Iteration agent
class PolicyIterationAgent(Agent[S, A]):
    mdp: MarkovDecisionProcess[S, A] # The MDP used by this agent for training
    policy: Dict[S, A]
    utilities: Dict[S, float] # The computed utilities
                                # The key is the string representation of the state and the value is the utility
    discount_factor: float # The discount factor (gamma)

    def __init__(self, mdp: MarkovDecisionProcess[S, A], discount_factor: float = 0.99) -> None:
        super().__init__()
        self.mdp = mdp
        # This initial policy will contain the first available action for each state,
        # except for terminal states where the policy should return None.
        self.policy = {
            state: (None if self.mdp.is_terminal(state) else self.mdp.get_actions(state)[0])
            for state in self.mdp.get_states()
        }
        self.utilities = {state:0 for state in self.mdp.get_states()} # We initialize all the utilities to be 0
        self.discount_factor = discount_factor
    
    # Given the utilities for the current policy, compute the new policy
    def update_policy(self):
        #TODO: Complete this function
        # make dictionary to store policy and update policy at the end of all states
        policy = {} 
        for state in self.mdp.get_states():
            if self.mdp.is_terminal(state):
                policy[state] = None
            else:
                max_utility = float('-inf')
                best_policy = None
                for action in self.mdp.get_actions(state):
                    # get transition prob and state
                    utility_v = self.mdp.get_successor(state, action)
                    utility = 0
                    # use reward, discount_factor, and utilities to calculate utility
                    for next_state, prob in utility_v.items():
                        # get reward
                        reward = self.mdp.get_reward(state, action, next_state)
                        utility += prob * (reward + self.discount_factor  * self.utilities[next_state])
                    # utility = sum(prob * self.utilities[next_state] for next_state, prob in utility_v.items())
                    if utility > max_utility:
                        max_utility = utility
                        best_policy = action # best policy is achieved when using the action that maximizes the utility
                policy[state] = best_policy
        self.policy = policy
    # Given the current policy, compute the utilities for this policy
    # Hint: you can use numpy to solve the linear equations. We recommend that you use numpy.linalg.lstsq
    
    def update_utilities(self):
        #TODO: Complete this function
        # NotImplemented()
        states = self.mdp.get_states()
        num_states = len(states)
        # A is a square matrix of size num_states x num_states that represents the linear equations to solve for the utilities of each state in the MDP
        A = np.zeros((num_states, num_states))
        # b is a vector of size num_states that represents the right hand side of the linear equations to solve for the utilities of each state in the MDP
        b = np.zeros(num_states)

        # Fill in the values of A and b to solve the linear equations 
        for i, state in enumerate(states):
            stating = {state: 0 for state in self.mdp.get_states()}
            stating[state] = 1
            dummy_b = 0
            if self.policy[state] is not None:
                # don't update A and B directly, use dummy dictionary to store the values
                # self.policy[state] : action to be taken
                for next_state,prob in self.mdp.get_successor(state, self.policy[state]).items() :
                    # get_transition_prob
                    stating[next_state] -= prob * self.discount_factor
                    dummy_b += prob * self.mdp.get_reward(state, self.policy[state], next_state)
            A[i] = np.array(list(stating.values()))
            b[i] = dummy_b
        # solve the linear equations using numpy.linalg.lstsq
        self.utilities = dict(zip(states, np.linalg.lstsq(A, b, rcond=None)[0]))
    
    # Applies a single utility update followed by a single policy update
    # then returns True if the policy has converged and False otherwise
    def update(self) -> bool:
        #TODO: Complete this function
        # NotImplemented()
        old_policy = self.policy.copy()
        # policy evaluation and policy improvement 
        self.update_utilities()
        self.update_policy()
        return old_policy == self.policy

    # This function applies value iteration starting from the current utilities stored in the agent and stores the new utilities in the agent
    # NOTE: this function does incremental update and does not clear the utilities to 0 before running
    # In other words, calling train(M) followed by train(N) is equivalent to just calling train(N+M)
    def train(self, iterations: Optional[int] = None) -> int:
        iteration = 0
        while iterations is None or iteration < iterations:
            iteration += 1
            if self.update():
                break
        return iteration
    
    # Given an environment and a state, return the best action as guided by the learned utilities and the MDP
    # If the state is terminal, return None
    def act(self, env: Environment[S, A], state: S) -> A:
        #TODO: Complete this function
        # NotImplemented()
        if self.mdp.is_terminal(state):
            return None
        # return best_action according to the utilities and the MDP for the given state 
        return self.policy[state]
    
    # Save the utilities to a json file
    def save(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'w') as f:
            utilities = {self.mdp.format_state(state): value for state, value in self.utilities.items()}
            policy = {
                self.mdp.format_state(state): (None if action is None else self.mdp.format_action(action)) 
                for state, action in self.policy.items()
            }
            json.dump({
                "utilities": utilities,
                "policy": policy
            }, f, indent=2, sort_keys=True)
    
    # loads the utilities from a json file
    def load(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'r') as f:
            data = json.load(f)
            self.utilities = {self.mdp.parse_state(state): value for state, value in data['utilities'].items()}
            self.policy = {
                self.mdp.parse_state(state): (None if action is None else self.mdp.parse_action(action)) 
                for state, action in data['policy'].items()
            }
