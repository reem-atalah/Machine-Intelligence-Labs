from inspect import stack
from mimetypes import init
from queue import Empty, Queue
import queue
from typing import List
from problem import HeuristicFunction, Problem, S, A, Solution
from collections import deque
from helpers import utils

#TODO: Import any modules you want to use
# All search functions take a problem and a state
# If it is an informed search function, it will also receive a heuristic function
# S and A are used for generic typing where S represents the state type and A represents the action type

# All the search functions should return one of two possible type:
# 1. A list of actions which represent the path from the initial state to the final state
# 2. None if there is no solution

def BreadthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    # It searches all nodes in each level
    # which processes all nodes above shallowest solution
    node = initial_state

    # if the root is the goal then return no direction 
    if problem.is_goal(node): return []

    # frontier: the set of leaf nodes available for expansion at any given point
    # Use queue for forintier, to append 
    frontier= deque()

    # append the root to the frontier
    frontier.append(node)

    # initialize explored set to have all explored node so that we won't consider them again
    explored = set()

    # pathsQueue has list of paths for each node
    # each path has actions to go from the root to the node
    # make the path as queue to be same as the frontier 
    # so pop from frontier, gets same index node as pop from pathsQueue
    pathsQueue = []

    # dummy initialization for first pop
    pathsQueue.append('u')

    # loop on frontier size, as we have nodes not expanded yet
    while frontier:
        # if frontier is empty, then there is no goal
        if not frontier: return None

        #use popleft instead pop to have FIFO(First In First Out) logic
        node = frontier.popleft() 

        # add the poped/expanded node from frontier into the explored set
        explored.add(node)

        # pop out the path of the parent node
        # pop(0): to pop from left, pop first element according to the last iteration
        path = pathsQueue.pop(0)

        # possible actions on this node
        for action in problem.get_actions(node):

            # get the child node that is produced from the action applied
            child = problem.get_successor(node,action)

            # we don't consider node that is already explored or arleady in the list to be expanded later
            if child not in explored and child not in frontier:

                # initialize a new path for each node, which has the parent path action
                nodePath = list(path)

                # append to the parent path, the action required for the child path
                nodePath.append(action)

                # append the whole actions of the node as a list for this node in the queue for all paths of all nodes
                pathsQueue.append(nodePath)
                # add goal test here not when the node is chosen for expansion
                # to return before having extra node
                if problem.is_goal(child): 
                    # return the path of the node without the first initialization
                    return nodePath[1:]

                # append the new node to be expanded
                frontier.append(child)


              

def DepthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    # It takes a branch and go through it until being finished
    # then return from down to up, to consider another node
     
    node = initial_state

    # if the root is the goal then return no direction 
    if problem.is_goal(node): return []

    # I didn't need to use frontier, the most important is not to have a node that is arleady expanded

    # initialize explored set to have all explored node so that we won't consider them again
    explored = set()

    # pathsQueue has list of paths for each node
    # each path has actions to go from the root to the node
    # make the path as queue to be same as the frontier 
    # so pop from frontier, gets same index node as pop from pathsQueue
    pathsQueue = []

    # dummy initialization for first pop
    pathsQueue.append('u')


    # Recursicve path for getting the deepest node for each node
    def DepthFirstSearchUtil(problem: Problem[S, A], explored: set,pathsQueue: List, node: S) -> Solution:
        if node not in explored:
            # as soon as we enter the node, then add it to explored, don't assign it again
            explored.add(node)

            # same as BreadthFirst
            path = pathsQueue.pop(0)
            for action in problem.get_actions(node):
                child = problem.get_successor(node,action)
                if child not in explored:
                    nodePath = list(path)
                    nodePath.append(action)
                    pathsQueue.append(nodePath)
                    if problem.is_goal(child):
                        return nodePath[1:]

                    # reached a node? go to its first child
                    p= DepthFirstSearchUtil(problem, explored, pathsQueue,child)
                    if p: return p #if p = none, check another nodes instead of returning
                    # now, we have the path of deep node of the goal
  
    # the path got from the recursion is the goal path
    return DepthFirstSearchUtil(problem, explored, pathsQueue, node)  
    
def UniformCostSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    # take the nodes that has less cost, untill reach the goal

    node = initial_state

    # for UniformCostSearch, we need to consider the accumulate cost of node, from root to it
    costTotal=0

    # step, used to break the tie, of having identical costs
    step = 1

    # for frontier, use PriorityQueue
    # where we put the priority according to cost of path and first in node
    frontier= queue.PriorityQueue()

    # initialize explored set to have all explored node so that we won't consider them again
    explored = set()

    # put in frontier: the cost of action, step, the node itself, the path
    # cost of root is 0
    # add the path to the frontier, so that we can easily get out the correct path for he correct node
    # now, no need for pathsQueue
    frontier.put((0,step,node,[]))
    
    while frontier.queue:
        # turn the priorityQueue to list to access its indexes
        # .get(): pop out the first element (highest priority) in the frontier
        node = list(frontier.get()) # node[0] = cost, node[1] = step, node[2]=state, node[3] = path
        
        # goal test is done when the node is expanded In case a better path is found to a node in the frontier
        if problem.is_goal(node[2]): 
            return node[3]
        explored.add(node[2])
        path = node[3]
        for action in problem.get_actions(node[2]):
            inFrontier=0
            child = problem.get_successor(node[2],action)
            if child not in explored :
                # cost of child node = cost of the node + cost of parent node (node[2])
                # calculate the accumulative cost (cost of node + cost of all branches from itself untill root)
                costTotal = node[0] + problem.get_cost(node[2], action)
                
                # update node if it has less cost in another place 
                for fronty in list(frontier.queue):
                    # turn tuple values in frontier to list, to access it's index
                    fronty = list(fronty)

                    # if we found a node that has name as the child
                    if child == fronty[2] :
                        inFrontier = 1 # don't add it again down
                        # check if the child has lower cost than the node in frontier
                        if costTotal < fronty[0]:
                            # yse? then replace it
                            # first remove the node
                            frontier.queue.remove(tuple(fronty))
                            # change its path according to the new path of the child
                            newnodePath = list(path)
                            newnodePath.append(action)
                            # update the step, as it represents when it entered
                            step +=1
                            # put the child in the priority queue
                            frontier.put((costTotal, step,child,newnodePath)) 

                            # we can never find this node again, after first finding it
                            # so break from this updating loop
                            break

                # if not updated, then add the node to the prontier, as usual
                if not inFrontier:
                # path
                    nodePath = list(path)
                    nodePath.append(action)
                    frontier.put((costTotal , step, child, nodePath))
                    step +=1

def AStarSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    #TODO: ADD YOUR CODE HERE
    # in addition to UCS, 
    # add the heuristic value to be considered in cost to choose the node acc. to the priority of lower cost
    # but do not add the heuristic in the accumulative cost


    node = initial_state
    costTotal=0
    step = 1
    frontier= queue.PriorityQueue()
    explored = set()

    # add the heuristic value to be considered in cost to choose the node acc. to the priority of lower cost
    # but do not add the heuristic in the accumulative cost
    # put also the actual cost and heuritic cost with the node, 
    frontier.put((0+heuristic(problem,node),step,0,heuristic(problem,node),node,[]))
    
    # all same as UCS, except at comparing cost
    while frontier.queue:
        node = list(frontier.get()) # node[0] = totalcost, node[1] = step, node[2]=cost, node[3] = heuristic, node[4] = stateNode, node[5]=path
        if problem.is_goal(node[4]): 
            return node[5]
        explored.add(node[4])
        path = node[5]
        for action in problem.get_actions(node[4]):
            inFrontier=0
            child = problem.get_successor(node[4],action)
            if child not in explored :
                # calculate the cost with the actual cost (no heuristic)
                costTotal = node[2] + problem.get_cost(node[4], action) 
                # update node if it has less cost in another place 
                for fronty in list(frontier.queue):
                    fronty = list(fronty)
                    if child == fronty[4] :
                        inFrontier = 1 # don't add it again down
                        # we consider for the lowest accumulative cost+heuristic
                        # to update the node on the frontier
                        if ( costTotal+ heuristic(problem,child) ) < (fronty[2]+fronty[3]):
                            frontier.queue.remove(tuple(fronty))
                            nodePath = list(path)
                            nodePath.append(action)
                            step +=1
                            frontier.put((costTotal+heuristic(problem,child) ,step, costTotal,heuristic(problem,child),child,nodePath)) 
                            break
                if not inFrontier:
                    # path
                    nodePath = list(path)
                    nodePath.append(action)
                    frontier.put((costTotal +heuristic(problem,child) , step,costTotal ,heuristic(problem,child), child, nodePath))
                    step +=1


def BestFirstSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    #TODO: ADD YOUR CODE HERE
    # no need for accumulative cost, as we calculate cost from heuritic only, which isn't addable
    node = initial_state
    step = 1
    frontier= queue.PriorityQueue()
    explored = set()
    frontier.put((heuristic(problem,node),step,node,[]))
    
    while frontier.queue:
        node = list(frontier.get()) # node[0] = heuristic, node[1] = step, node[2]=state, node[3] = path
        if problem.is_goal(node[2]): 
            return node[3]
        explored.add(node[2])
        path = node[3]
        for action in problem.get_actions(node[2]):
            inFrontier=0
            child = problem.get_successor(node[2],action)
            if child not in explored :
                # update node if it has less cost in another place 
                for fronty in list(frontier.queue):
                    fronty = list(fronty)
                    if child == fronty[2] :
                        inFrontier = 1 # don't add it again down
                        # compare costs with heuristic
                        if heuristic(problem,child)  < fronty[0]:
                            frontier.queue.remove(tuple(fronty))
                            nodePath = list(path)
                            nodePath.append(action)
                            step +=1
                            frontier.put((heuristic(problem,child) ,step, child,nodePath)) 
                            break
                if not inFrontier:
                    # path
                    nodePath = list(path)
                    nodePath.append(action)
                    frontier.put((heuristic(problem,child) , step, child, nodePath))
                    step +=1

