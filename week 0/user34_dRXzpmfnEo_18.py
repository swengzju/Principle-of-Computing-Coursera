"""
Clone of 2048 game.
"""

import poc_2048_gui        
import random
# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.    
OFFSETS = {UP: (1, 0), 
           DOWN: (-1, 0), 
           LEFT: (0, 1), 
           RIGHT: (0, -1)} 
   
def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    initiallist = [0] * len(line)
    var_i = 0
    for var_j in range(len(line)):
        if line[var_j]!=0:
            initiallist[var_i] = line[var_j]
            var_i += 1    
    flag = [False] * len(line)

    for var_k in range(len(line)):
        if initiallist[var_k]!= 0 and flag[var_k] == False:
            for var_l in range(var_k+1, len(line)):
                if initiallist[var_l] != initiallist[var_k] and initiallist[var_l] != 0:
                    break
                elif initiallist[var_l] == initiallist[var_k]:
                    flag[var_k] = True
                    initiallist[var_k] = 2*initiallist[var_l]
                    var_m = var_k+1
                    while var_l < len(line)-1:
                        initiallist[var_m] = initiallist[var_l+1]
                        var_l += 1
                        var_m += 1
                    while var_m < len(line):
                        initiallist[var_m] = 0
                        var_m += 1
                    break    
    return initiallist

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self.row = grid_height
        self.column = grid_width
        self.reset()
        self.tiles = {UP: [[0, col] for col in range(self.column)], 
           DOWN: [[self.row - 1, col] for col in range(self.column)], 
           LEFT: [[row, 0] for row in range(self.row)], 
           RIGHT: [[row, self.column - 1] for row in range(self.row)]} 
    
    def reset(self):
        """
        Reset the game so the grid is empty.
        """
        self.grid = [ [0 for dummy_col in range(self.column)] for dummy_row in range(self.row)]
        return self.grid
    
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        return str(self.grid)

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self.row
    
    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self.column
                            
    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """

        for item in self.tiles[direction]:
            newlist = []
            temprow = item[0]
            tempcol = item[1]
            while temprow < self.row and tempcol < self.column and temprow >= 0 and tempcol >= 0:
                newlist.append(self.get_tile(temprow, tempcol))
                temprow += OFFSETS[direction][0]
                tempcol += OFFSETS[direction][1]
            merged = merge(newlist)
            temprow = item[0]
            tempcol = item[1]                        
            #while temprow < self.row and tempcol < self.column and temprow >= 0 and tempcol >= 0:
            for items in merged:                 
                self.set_tile(temprow, tempcol, items)
                temprow += OFFSETS[direction][0]
                tempcol += OFFSETS[direction][1]
                if temprow >= self.row or tempcol >= self.column or temprow < 0 or tempcol < 0:
                    break
        self.new_tile()
                
        
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty 
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        zerolist = []
        for row in range(self.row):
            for col in range(self.column):
                if self.grid[row][col] == 0:
                    zerolist.append([row, col])
        if zerolist != []:
            newele = random.randrange(0, len(zerolist))
            srow = zerolist[newele][0]
            scol = zerolist[newele][1]
            self.grid[srow][scol] = random.choice([2,2,2,2,2,2,2,2,2,4])
        
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """        
        self.grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """        
        # replace with your code
        return self.grid[row][col]
 
    
poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
