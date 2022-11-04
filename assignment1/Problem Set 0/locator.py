from typing import Any, Set, Tuple
from grid import Grid
import utils

def locate(grid: Grid, item: Any) -> Set[Tuple[int,int]]:
    '''
    This function takes a 2D grid and an item
    It should return a list of (x, y) coordinates that specify the locations that contain the given item
    To know how to use the Grid class, see the file "grid.py"  
    '''
    #TODO: ADD YOUR CODE HERE
    # utils.NotImplemented()
    coordinates: Set[Tuple[int,int]]={()}
    coordinates.clear()
    for itr1 in range(grid.width):
        for itr2 in range(grid.height):
            if(grid.__getitem__((itr1,itr2)) == item):
                coordinates.add((itr1,itr2))
                
    return coordinates
