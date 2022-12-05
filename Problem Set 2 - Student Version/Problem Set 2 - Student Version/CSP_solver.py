from typing import Any, Dict, List, Optional
from CSP import Assignment, BinaryConstraint, Problem, UnaryConstraint
from helpers.utils import NotImplemented

# This function should apply 1-Consistency to the problem.
# In other words, it should modify the domains to only include values that satisfy their variables' unary constraints.
# Then all unary constraints should be removed from the problem (they are no longer needed). -------------------
# The function should return False if any domain becomes empty. Otherwise, it should return True.
def one_consistency(problem: Problem) -> bool:
    #TODO: Write this function
    # NotImplemented()
    for constraint in problem.constraints:
        if(type(constraint) == UnaryConstraint):
            variable = constraint.variable # get the variable of the constraint 
            values = problem.domains[variable].copy() # get the domain of the variable 
            accepted_values = [] # create a list to store the accepted values
            for value in values: # check each value in the domain of the variable
                dicty ={variable: value} # create a dictionary with the variable and its value
                if constraint.is_satisfied(dicty): # check if the dictionary is consistent with the constraints
                    accepted_values.append(value) # if yes, add the value to the list of accepted values
            problem.domains[variable] = set(accepted_values) # update the domain of the variable to be the list of accepted values
            if len(problem.domains[variable]) == 0: # if the domain is empty, return false
                return False
    problem.constraints = [constraint for constraint in problem.constraints if type(constraint) == BinaryConstraint] # remove the unary constraints from the problem
    return True
            

# This function should implement forward checking
# The function is given the problem, the variable that has been assigned and its assigned value and the domains of the unassigned values
# The function should return False if it is impossible to solve the problem after the given assignment, and True otherwise.
# In general, the function should do the following:
#   - For each binary constraints that involve the assigned variable:
#       - Get the other involved variable.
#       - If the other variable has no domain (in other words, it is already assigned), skip this constraint.
#       - Update the other variable's domain to only include the values that satisfy the binary constraint with the assigned variable.
#   - If any variable's domain becomes empty, return False. Otherwise, return True.
# IMPORTANT: Don't use the domains inside the problem, use and modify the ones given by the "domains" argument 
#            since they contain the current domains of unassigned variables only.
def forward_checking(problem: Problem, assigned_variable: str, assigned_value: Any, domains: Dict[str, set]) -> bool:
    #TODO: Write this function
    # NotImplemented()
    for constraint in problem.constraints:
        if(type(constraint) == BinaryConstraint) and (assigned_variable in constraint.variables):
            other_variable = constraint.get_other(assigned_variable)
            accepted_values = []
            if domains.get(other_variable) != None:
                for value in domains[other_variable]:
                    dicty = {assigned_variable: assigned_value, other_variable: value}
                    if constraint.is_satisfied(dicty):
                        accepted_values.append(value)
                domains[other_variable] = set(accepted_values)
                if len(domains[other_variable]) == 0:
                    return False
    return True

# This function should return the domain of the given variable order based on the "least restraining value" heuristic.
# IMPORTANT: This function should not modify any of the given arguments.
# Generally, this function is very similar to the forward checking function, but it differs as follows:
#   - You are not given a value for the given variable, since you should do the process for every value in the variable's
#     domain to see how much it will restrain the neigbors domain
#   - Here, you do not modify the given domains. But you can create and modify a copy.
# IMPORTANT: If multiple values have the same priority given the "least restraining value" heuristic, 
#            order them in ascending order (from the lowest to the highest value).
# IMPORTANT: Don't use the domains inside the problem, use and modify the ones given by the "domains" argument 
#            since they contain the current domains of unassigned variables only.
def least_restraining_values(problem: Problem, variable_to_assign: str, domains: Dict[str, set]) -> List[Any]:
    #TODO: Write this function
    NotImplemented()

# This function should return the variable that should be picked based on the MRV heuristic.
# IMPORTANT: This function should not modify any of the given arguments.
# IMPORTANT: Don't use the domains inside the problem, use and modify the ones given by the "domains" argument 
#            since they contain the current domains of unassigned variables only.
# IMPORTANT: If multiple variables have the same priority given the MRV heuristic, 
#            order them in the same order in which they appear in "problem.variables".
def minimum_remaining_values(problem: Problem, domains: Dict[str, set]) -> str:
    #TODO: Write this function
    # NotImplemented()
    res = None
    for variable in problem.variables:
        if len(domains[variable]) == 0:
            continue        
        if res == None:
            res = variable
        elif len(domains[variable]) < len(domains[res]):
            res = variable
    return res
    

# This function should solve CSP problems using backtracking search with forward checking.
# The variable ordering should be decided by the MRV heuristic.
# The value ordering should be decided by the "least restraining value" heurisitc.
# Unary constraints should be handled using 1-Consistency before starting the backtracking search.
# This function should return the first solution it finds (a complete assignment that satisfies the problem constraints).
# If no solution was found, it should return None.
# IMPORTANT: To get the correct result for the explored nodes, you should check if the assignment is complete only once using "problem.is_complete"
#            for every assignment including the initial empty assignment, EXCEPT for the assignments pruned by the forward checking.
#            Also, if 1-Consistency deems the whole problem unsolvable, you shouldn't call "problem.is_complete" at all.
def solve(problem: Problem) -> Optional[Assignment]:
    #TODO: Write this function
    NotImplemented()