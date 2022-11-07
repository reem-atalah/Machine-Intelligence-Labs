from hashlib import new
from itertools import count
from pickle import NONE
from turtle import position
from typing import Any, Dict, Set, Tuple, List
from problem import Problem
from mathutils import Direction, Point
from helpers import utils

#TODO: (Optional) Instead of Any, you can define a type for the parking state
ParkingState = Tuple[Point] #(x,y)
# An action of the parking problem is a tuple containing an index 'i' and a direction 'd' where car 'i' should move in the direction 'd'.
ParkingAction = Tuple[int, Direction]

# This is the implementation of the parking problem
class ParkingProblem(Problem[ParkingState, ParkingAction]):
    passages: Set[Point]    # A set of points which indicate where a car can be (in other words, every position except walls).
    cars: Tuple[Point]      # A tuple of points where state[i] is the position of car 'i'. 
    slots: Dict[Point, int] # A dictionary which indicate the index of the parking slot (if it is 'i' then it is the slot of car 'i') for every position.
                            # if a position does not contain a parking slot, it will not be in this dictionary.
    width: int              # The width of the parking slot.
    height: int             # The height of the parking slot.

    # This function should return the initial state
    def get_initial_state(self) -> ParkingState:
        #TODO: ADD YOUR CODE HERE
        # initial state is the initial Point/place of all cars
        initial_state = self.cars
        return initial_state
    
    # This function should return True if the given state is a goal. Otherwise, it should return False.
    def is_goal(self, state: ParkingState) -> bool:
        #TODO: ADD YOUR CODE HERE
        # We reach goal when all cars are on their correct slots
        # For each value of i, states(Points)[i]=slots[i] -where i is the car number-
        for point in self.slots:
            if state[self.slots[point]] != point:
                return False
        return True
    
    # This function returns a list of all the possible actions that can be applied to the given state
    def get_actions(self, state: ParkingState) -> List[ParkingAction]:
        #TODO: ADD YOUR CODE HERE
        # List to append all actions could be occured, each for each car
        actions = []

        # index to trace which car we're talking about
        index=0

        # for each car
        for point in state:
            # see all possible directions (R,L,U,D)
            for direction in Direction:

                # add the direction to car[i]'s current position
                # direction.to_vector(): change the direction to vector point
                position = point+ direction.to_vector()
                
                check = True

                # Disallow walking into walls, walk in points have dots only
                if position not in self.passages: continue

                # Disallow walking on another car
                # can't go to point where another car is already there
                for i in range(len(state)):
                    # check for all car states positions that aren't same as the position I want to go through 
                    if position == state[i]:
                        check = False
                        break
                
                # if true, then no car in this position and it's a valid path
                # so append the direction that causes this path, and the correct car index
                if check : actions.append((index,direction.__str__()))
            index+=1
        return actions
    
    # This function returns a new state which is the result of applying the given action to the given state
    def get_successor(self, state: ParkingState, action: ParkingAction) -> ParkingState:
        #TODO: ADD YOUR CODE HERE
        # convert state tuple to list, to acces it easily
        stateList =list(state)

        # action[0] : index of the car we want to apply action on it
        # stateList[action[0]]: get current position then update it
        # action[1]: has the direction that is possible to be applied
        # action[1].to_vector(): change the direction to vector point
        stateList[action[0]]= stateList[action[0]]+action[1].to_vector()

        # return state after updating the position with the new action applied
        return tuple(stateList)

    
    # This function returns the cost of applying the given action to the given state
    def get_cost(self, state: ParkingState, action: ParkingAction) -> float:
        #TODO: ADD YOUR CODE HERE
        # Apply the action as in get_successor()
        position = state[action[0]]+ action[1].to_vector()

        # check if the new position is on one the parking slots.
        if position in self.slots:
            # action[0] : index of the car we are appling action on it
            # if the index of slot we're at, not equal to index of car applied the action
            # then it's penalized with cost=101 otherwise cost is 1 only
            if self.slots[position] == action[0]:
                return 1
            else: return 101
        else: return 1
    
     # Read a parking problem from text containing a grid of tiles
    @staticmethod
    def from_text(text: str) -> 'ParkingProblem':
        passages =  set()
        cars, slots = {}, {}
        lines = [line for line in (line.strip() for line in text.splitlines()) if line]
        width, height = max(len(line) for line in lines), len(lines)
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char != "#":
                    passages.add(Point(x, y))
                    if char == '.':
                        pass
                    elif char in "ABCDEFGHIJ":
                        cars[ord(char) - ord('A')] = Point(x, y)
                    elif char in "0123456789":
                        slots[int(char)] = Point(x, y)
        problem = ParkingProblem()
        problem.passages = passages
        problem.cars = tuple(cars[i] for i in range(len(cars)))
        problem.slots = {position:index for index, position in slots.items()}
        problem.width = width
        problem.height = height
        return problem

    # Read a parking problem from file containing a grid of tiles
    @staticmethod
    def from_file(path: str) -> 'ParkingProblem':
        with open(path, 'r') as f:
            return ParkingProblem.from_text(f.read())
    
