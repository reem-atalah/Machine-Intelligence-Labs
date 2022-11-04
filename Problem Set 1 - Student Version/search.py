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
    # utils.NotImplemented()
    node = initial_state
    pathsQueue = []
    pathsQueue.append('u')

    if problem.is_goal(node): return []
    frontier= deque()
    frontier.append(node)
    explored = set()
    
    while frontier:
        if not frontier: return None
        node = frontier.popleft() #FIFO
        explored.add(node)
        # print(node, type(node))
        path = pathsQueue.pop(0)
        for action in problem.get_actions(node):
            child = problem.get_successor(node,action)
            if child not in explored and child not in frontier:
                newPath = list(path)
                newPath.append(action)
                pathsQueue.append(newPath)
                if problem.is_goal(child): 
                    return newPath[1:]
                frontier.append(child)


def DepthFirstSearchUtil(problem: Problem[S, A], explored: set,pathsQueue: List, node: S) -> Solution:
    if node not in explored:
        explored.add(node)
        path = pathsQueue.pop(0)
        for action in problem.get_actions(node):
            child = problem.get_successor(node,action)
            if child not in explored:
                newPath = list(path)
                newPath.append(action)
                pathsQueue.append(newPath)
                if problem.is_goal(child):
                    return newPath[1:]
                p= DepthFirstSearchUtil(problem, explored, pathsQueue,child)
                if p: return p #check if p none, check another nodes instead of returning
                

def DepthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    node = initial_state
    pathsQueue = []
    pathsQueue.append('u')

    if problem.is_goal(node): return []
    explored = set()

    return DepthFirstSearchUtil(problem, explored, pathsQueue, node)  
    
def UniformCostSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    # utils.NotImplemented()
    node = initial_state
    costTotal=0
    step = 1
    frontier= queue.PriorityQueue()
    explored = set()
    frontier.put((0,step,node,[]))
    
    while frontier.queue:
        node = list(frontier.get()) # node[0] = cost, node[1] = step, node[2]=state, node[3] = path
        if problem.is_goal(node[2]): 
            return node[3]
        explored.add(node[2])
        path = node[3]
        for action in problem.get_actions(node[2]):
            inFrontier=0
            child = problem.get_successor(node[2],action)
            if child not in explored :
                # cost
                costTotal = node[0] + problem.get_cost(node[2], action)
                # update node if it has less cost in another place 
                for fronty in list(frontier.queue):
                    fronty = list(fronty)
                    if child == fronty[2] :
                        inFrontier = 1 # don't add it again down
                        if costTotal < fronty[0]:
                            frontier.queue.remove(tuple(fronty))
                            newPath = list(path)
                            newPath.append(action)
                            step +=1
                            frontier.put((costTotal, step,child,newPath)) 
                            break
                if not inFrontier:
                # path
                    newPath = list(path)
                    newPath.append(action)
                    frontier.put((costTotal , step, child, newPath))
                    step +=1

def AStarSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    #TODO: ADD YOUR CODE HERE
    # utils.NotImplemented()
    node = initial_state
    costTotal=0
    step = 1
    frontier= queue.PriorityQueue()
    explored = set()
    frontier.put((0+heuristic(problem,node),step,0,heuristic(problem,node),node,[]))
    
    while frontier.queue:
        node = list(frontier.get()) # node[0] = cost, node[1] = step, node[2]=state, node[3] = path, node[4] = heuristic
        if problem.is_goal(node[4]): 
            return node[5]
        explored.add(node[4])
        path = node[5]
        for action in problem.get_actions(node[4]):
            inFrontier=0
            child = problem.get_successor(node[4],action)
            if child not in explored :
                # cost
                costTotal = node[2] + problem.get_cost(node[4], action) 
                # update node if it has less cost in another place 
                for fronty in list(frontier.queue):
                    fronty = list(fronty)
                    if child == fronty[4] :
                        inFrontier = 1 # don't add it again down
                        if ( costTotal+ heuristic(problem,child) ) < (fronty[2]+fronty[3]):
                            frontier.queue.remove(tuple(fronty))
                            newPath = list(path)
                            newPath.append(action)
                            step +=1
                            frontier.put((costTotal+heuristic(problem,child) ,step, costTotal+heuristic(problem,child),child,newPath)) 
                            break
                if not inFrontier:
                    # path
                    newPath = list(path)
                    newPath.append(action)
                    frontier.put((costTotal +heuristic(problem,child) , step,costTotal ,heuristic(problem,child), child, newPath))
                    step +=1


def BestFirstSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    #TODO: ADD YOUR CODE HERE
    # utils.NotImplemented()
    node = initial_state
    costTotal=0
    step = 1
    frontier= queue.PriorityQueue()
    explored = set()
    frontier.put((0+heuristic(problem,node),step,0,heuristic(problem,node),node,[]))
    
    while frontier.queue:
        node = list(frontier.get()) # node[0] = cost, node[1] = step, node[2]=state, node[3] = path, node[4] = heuristic
        if problem.is_goal(node[4]): 
            return node[5]
        explored.add(node[4])
        path = node[5]
        for action in problem.get_actions(node[4]):
            inFrontier=0
            child = problem.get_successor(node[4],action)
            if child not in explored :
                # cost
                costTotal = node[2] + problem.get_cost(node[4], action) 
                # update node if it has less cost in another place 
                for fronty in list(frontier.queue):
                    fronty = list(fronty)
                    if child == fronty[4] :
                        inFrontier = 1 # don't add it again down
                        if ( costTotal+ heuristic(problem,child) ) < (fronty[2]+fronty[3]):
                            frontier.queue.remove(tuple(fronty))
                            newPath = list(path)
                            newPath.append(action)
                            step +=1
                            frontier.put((costTotal+heuristic(problem,child) ,step, costTotal+heuristic(problem,child),child,newPath)) 
                            break
                if not inFrontier:
                    # path
                    newPath = list(path)
                    newPath.append(action)
                    frontier.put((costTotal +heuristic(problem,child) , step,costTotal ,heuristic(problem,child), child, newPath))
                    step +=1

