"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        if self._grid[target_row][target_col] != 0:
            return False
        for row in range(target_row+1, self._height):
            for col in range(self._width):
                if self._grid[row][col] != col + self._width * row:
                    return False
        for col in range(target_col+1, self._width):
            if self._grid[target_row][col] != col + self._width * target_row:
                return False
        return True
    
    def position_tile(self, cur_row, cur_col, target_row, target_col):
        """
        useful
        """
        move_string = ""
        if cur_col < target_col:
            move_left = target_col - cur_col
            move_up = target_row - cur_row
            if move_up == 0:
                for dummy_left in range(move_left):
                    self.update_puzzle("l")
                    move_string += "l"
                for dummy_left in range(move_left - 1):
                    self.update_puzzle("urrdl")
                    move_string += "urrdl"
            else:
                for dummy_up in range(move_up):
                    self.update_puzzle("u")
                    move_string += "u"
                while move_left > 1:
                    for dummy_left in range(move_left):
                        self.update_puzzle("l")
                        move_string += "l"
                    self.update_puzzle("d")
                    move_string += "d"
                    for dummy_left in range(move_left):
                        self.update_puzzle("r")
                        move_string += "r"
                    self.update_puzzle("u")
                    move_string += "u"
                    move_left -= 1
                self.update_puzzle("l")
                move_string += "l"
                for dummy_down in range(move_up - 1):
                    self.update_puzzle("ddruuld")
                    move_string += "ddruuld"
                self.update_puzzle("druld")
                move_string += "druld"
        elif cur_col == target_col:
            move_up = target_row - cur_row
            for dummy_up in range(move_up):
                self.update_puzzle("u")
                move_string += "u"
            for dummy_down in range(move_up - 1):
                self.update_puzzle("lddru")
                move_string += "lddru"
            self.update_puzzle("ld")
            move_string += "ld"
        elif cur_col > target_col:
            move_left = cur_col - target_col
            move_up = target_row - cur_row
            for dummy_up in range(move_up):
                self.update_puzzle("u")
                move_string += "u"
            for dummy_left in range(move_left):
                self.update_puzzle("r")
                move_string += "r"
            for dummy_left in range(move_left):
                self.update_puzzle("dllur")
                move_string += "dllur"
            self.update_puzzle("l")
            move_string += "l"  
            for dummy_down in range(move_up - 1):
                self.update_puzzle("ddruuld")
                move_string += "ddruuld" 
            self.update_puzzle("druld")
            move_string += "druld"
#        assert self.lower_row_invariant(target_row, target_col - 1)
        return move_string

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
#        assert target_row > 1 and target_col > 0
#        assert self.lower_row_invariant(target_row, target_col)
        cur_row, cur_col = self.current_position(target_row, target_col)
        move_string = ""
        move_string += self.position_tile(cur_row, cur_col, target_row, target_col)
        return move_string

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        move_string = ""
        if self.current_position(target_row, 0) == (target_row - 1, 0):
            self.update_puzzle("u")
            move_string += "u"
            for dummy_move in range(self._width - 1):
                self.update_puzzle("r")
                move_string += "r"
        else:
            self.update_puzzle("ur")
            move_string += "ur"
            cur_col = self.current_position(target_row, 0)[1]
            cur_row = self.current_position(target_row, 0)[0]
            if cur_row == target_row - 1 and cur_col > 1:
                for dummy_move in range(cur_col - 2):
                    self.update_puzzle("r")
                    move_string += "r"
                for dummy_move in range(cur_col - 1):
                    self.update_puzzle("rulld")
                    move_string += "rulld"
            else:
                move_string += self.position_tile(cur_row, cur_col, target_row - 1, 1)              
            self.update_puzzle("ruldrdlurdluurddlur")
            move_string += "ruldrdlurdluurddlur"
            for dummy_move in range(self._width - 2):
                self.update_puzzle("r")
                move_string += "r" 
        assert self.lower_row_invariant(target_row - 1, self._width - 1)
        return move_string

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if self._grid[0][target_col] != 0:
            return False
        for row in range(2, self._height):
            for col in range(self._width):
                if self._grid[row][col] != col + self._width * row:
                    return False
        for col in range(target_col, self._width):
            if self._grid[1][col] != col + self._width:
                return False
        for col in range(target_col+1, self._width):
            if self._grid[0][col] != col:
                return False  
        return True

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if self._grid[1][target_col] != 0:
            return False
        for row in range(2, self._height):
            for col in range(self._width):
                if self._grid[row][col] != col + self._width * row:
                    return False
        for col in range(target_col+1, self._width):
            if self._grid[1][col] != col + self._width:
                return False
        for col in range(target_col+1, self._width):
            if self._grid[0][col] != col:
                return False  
        return True

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row0_invariant(target_col)
        move_string = ""
        self.update_puzzle("ld")
        move_string += "ld"
        cur_row, cur_col = self.current_position(0, target_col)
        move_left = target_col - cur_col - 1
        if cur_col == target_col:
            return move_string
        else:
            if cur_row == 0:
                while move_left > 0:
                    self.update_puzzle("u")
                    move_string += "u"
                    for dummy_move in range(move_left):
                        self.update_puzzle("l")
                        move_string += "l"
                    self.update_puzzle("d")
                    move_string += "d"
                    for dummy_move in range(move_left):
                        self.update_puzzle("r")
                        move_string += "r"
                    move_left -= 1
                self.update_puzzle("uld")
                move_string += "uld"
            else:
                while move_left > 1:
                    for dummy_move in range(move_left):
                        self.update_puzzle("l")
                        move_string += "l"
                    self.update_puzzle("u")
                    move_string += "u"
                    for dummy_move in range(move_left):
                        self.update_puzzle("r")
                        move_string += "r"
                    self.update_puzzle("d")
                    move_string += "d"
                    move_left -= 1
                self.update_puzzle("l")
                move_string += "l"
            self.update_puzzle("urdlurrdluldrruld")
            move_string += "urdlurrdluldrruld"
        assert self.row1_invariant(target_col - 1)
        return move_string

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row1_invariant(target_col)
        move_string = ""
        cur_row, cur_col = self.current_position(1, target_col)
        move_left = target_col - cur_col
        if cur_row == 0:
            while move_left > 0:
                self.update_puzzle("u")
                move_string += "u"
                for dummy_move in range(move_left):
                    self.update_puzzle("l")
                    move_string += "l"
                self.update_puzzle("d")
                move_string += "d"
                for dummy_move in range(move_left):
                    self.update_puzzle("r")
                    move_string += "r"
                move_left -= 1
            self.update_puzzle("u")
            move_string += "u"
        else:
            while move_left > 0:
                for dummy_move in range(move_left):
                    self.update_puzzle("l")
                    move_string += "l"
                self.update_puzzle("u")
                move_string += "u"
                for dummy_move in range(move_left):
                    self.update_puzzle("r")
                    move_string += "r"
                self.update_puzzle("d")
                move_string += "d"
                move_left -= 1
            self.update_puzzle("u")
            move_string += "u"
        assert self.row0_invariant(target_col)
        return move_string

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        move_string = ""
        assert self.row1_invariant(1)
        self.update_puzzle("lu")
        move_string += "lu"
        flag = 0
        while flag < 4 and self.current_position(0, 1) != 1:
            self.update_puzzle("rdlu")
            move_string += "rdlu"
            flag += 1
        return move_string

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        # this is not 100% right, final score was 79.3
        move_string = ""
        step = self._height - 1
        temp = self._width - 1
        flag = 0
        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] != col + self._width * row:
                    flag = 1
        if flag == 0:
            return move_string
        while step > 1:
            for col in range(self._width - 1, 0, -1):
                move_string += self.solve_interior_tile(step, col)
            move_string += self.solve_col0_tile(step)
            step -= 1  
        while temp > 1:              
            move_string += self.solve_row1_tile(temp)
            move_string += self.solve_row0_tile(temp)
            temp -= 1
        move_string += self.solve_2x2()        
        return move_string

# Start interactive simulation
poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))


