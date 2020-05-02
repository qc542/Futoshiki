import io
import copy


class Cell:
    def __init__(self, coord: tuple, assign: int, domain: list,
            constr: list):
        self.coord = coord
        # The coordinates of the cell represented as a tuple
        # e.g. (2, 3) denotes Row 2, Column 3
        # Row and column numbers range from 0~4 (inclusive)

        self.assign = assign
        # The value assigned to the cell, if any
        # = None if the cell is unassigned

        self.domain = domain
        # Represented as a list of integers

        self.constr = constr
        # Constraints of inequality on the cell, represented as
        # a list of strings


class Board:
    def __init__(self, all_cells: list, all_constr: list):
        self.cells = all_cells
        # All twenty-five cells on the board, represented as
        # a five-by-five list

        self.constr = all_constr
        # All constraints of all twenty-five cells, represented as
        # a five-by-five-by-four list
        # The constraints of an individual cell is represented as
        # a list of four strings, each of which indicates the constraint 
        # regarding one of the four neighbors

    """ The following are four methods that, when given one of the Cell 
    objects on the board, return one of its neighbors. If moving in 
    the particular direction (left, right, etc.) goes beyond the 
    boundaries of the board, each of the methods raises a ValueError."""    
    def go_left(self, origin: Cell) -> Cell:
        row = origin.coord[0]
        col = origin.coord[1] - 1
        if (0 <= col <= 4):
            return self.cells[row][col]
            # If the move is within the boundaries of the board,
            # return the destination as a Cell object

        else:
            raise ValueError()
            # ValueError will be caught by the function that calls
            # this method

        
    def go_right(self, origin: Cell) -> Cell:
        row = origin.coord[0]
        col = origin.coord[1] + 1
        if (0 <= col <= 4):
            return self.cells[row][col]
        else:
            raise ValueError()


    def go_up(self, origin: Cell) -> Cell:
        row = origin.coord[0] - 1
        col = origin.coord[1]
        if (0 <= row <= 4):
            return self.cells[row][col]
        else:
            raise ValueError()


    def go_down(self, origin: Cell) -> Cell:
        row = origin.coord[0] + 1
        col = origin.coord[1]
        if (0 <= row <= 4):
            return self.cells[row][col]
        else:
            raise ValueError()


def load_input(filename: str) -> list:
    """ Given the name of the input file, the function reads the file line by 
    line and builds the data structures for the initial state as well as the 
    constraints of inequality."""
    
    text_stream = io.open(filename, 'r', encoding='utf-8', errors='ignore', newline='\n')
    """ Calls Python's io function to read the file with the specified name."""

    initial_state = []
    for i in range(0,5):
        initial_state.append(list(map(int, text_stream.readline().rstrip().split(' '))))
        """ The rstrip method removes all trailing white space of 
        the string. The split method uses the given character as the 
        delimiter to break down the string and return a list of the 
        substrings. The map function takes that list, converts the 
        substrings into integers and returns a map object, which is 
        eventually converted into a list by the exterior call to the 
        list function."""

        """ A state is represented as a multi-layer list. The first 
        layer contains the five rows, each of which contains a 
        second layer that consists of five cells."""

    blank_line = text_stream.readline()

    """ In the input file, there is a blank line following the 
    first five lines, after which begin the next five lines 
    that represent the horizontal constraints."""

    constr = []
    """ The constraints from the input file will be 
    converted to a specific text format and stored in this 
    list."""


    for i in range(0,5):
        a_row = []
        # A list that stores the constraints of all cells
        # in a single row
        for j in range(0,5):
            a_row.append(['U', 'D', 'L', 'R'])
            """ Each row in the list "constr" contains
            five lists, one for each of the five cells 
            in a row. Each sublist stores the constraints 
            in four directions that relate to the 
            particular cell: its relation with the cell 
            above ('U'), the cell below ('D'), the cell 
            to the left ('L'), and the cell to the 
            right ('R'). 'U', 'D', 'L' and 'R' 
            are four strings that function as placeholders 
            for now. Afterward they'll be modified to 
            indicate the exact relations between each pair.
            """
            if i == 0:
                a_row[j][0] = "N/A"
                """ For all cells in the first row, the 
                first element in their lists is replaced 
                with "N/A", since there are no cells 
                above them."""
            elif i == 4:
                a_row[j][1] = "N/A"
                """ By the same token, the second element 
                in the lists of all cells in the last row 
                is replaced with "N/A"."""

            if j == 0:
                a_row[j][2] = "N/A"
                """ For all cells in the first column,
                the third element in their lists is 
                replaced with "N/A", since there are no 
                cells to their left."""
            elif j == 4:
                a_row[j][3] = "N/A"
                """ By the same token, the fourth element 
                in the lists of all cells in the last 
                column is replaced with "N/A"."""

        constr.append(a_row)
        """ Now that the proper placeholders have been 
        inserted into the list of a single row, append 
        the row to the list "constr"."""

    """ By this point "constr" has been formatted as:

    1st layer: five lists, each referring to a row on 
    the Fukushiki board.
    
    2nd layer: this is within each list in the 1st 
    layer. There are five lists, each refering to a 
    cell in the particular row.

    3rd layer: this is within each list in 2nd layer. 
    There are four strings, each referring to the 
    relation between the current cell and the four 
    neighboring cells: the one above ('U'), the 
    one below ('D'), the one to the left ('L'), 
    and the one to the right ('R'). These strings 
    will be modified afterward to indicate the 
    exact relations."""


    """ The following for loop reads the next five lines, which 
    contain the constraints between horizontally-adjacent 
    cells."""

    for i in range(0, 5):
        line = list(map(str, text_stream.readline().rstrip().split(' ')))
        """ The functions and methods used in this line are 
        identical to the ones in the previous for loop. "line"
        is a list of the four characters that represent the 
        constraints in the row. """

        for j in range(len(line)):
            # len(line) is expected to be 4 (four constraints in 
            # a row)
            if line[j] == '0':
                constr[i][j][3] = "None"
                constr[i][j+1][2] = "None"
                """ For instance, if j = 0, and line[j] = 0, 
                that indicates there's no constraint between 
                the first and second cells of the row. 
                Therefore, modify the fourth element of the 
                first cell, which stores the current cell's 
                relation with the cell on the right; replace 
                'R' with "None", since there's no constraint. 
                By the same token, replace the third element 
                of the second cell with "None"."""

            elif line[j] == '>':
                constr[i][j][3] = "GTR"
                constr[i][j+1][2] = "STL"
                """ For instance, if j = 0, and line[j] = '>', 
                that indicates the first cell of the row has 
                to be greater than the second cell. Therefore, 
                modify the fourth element of the first cell, 
                which stores the current cell's relation with 
                the cell on the right; replace 'R' with "GTR", 
                which stands for "Greater Than Right". By the 
                same token, replace the third element of the 
                second cell with "STL", which stands for 
                "Smaller Than Left"."""

            elif line[j] == '<':
                constr[i][j][3] = "STR"
                constr[i][j+1][2] = "GTL"
                """ The same notation as above, only that the 
                relation is one being smaller than the other."""

    """ By the end of the double-layer for loop, all constraints 
    for horizontally-adjacent cells have been read and stored. 
    The input file contains another blank line, followed by the 
    last four lines, which illustrate the constraints for 
    vertically-adjacent cells."""

    blank_line = text_stream.readline()
    # Move the read cursor past the blank line.

    for i in range(0, 4):
        # range = (0,4) because this part of the input file contains 
        # only four rows
        
        line = list(map(str, text_stream.readline().rstrip().split(' ')))
        # Contains the same methods as previously explained
        # "line" is a list that contains the four characters that 
        # represent the constraints in a column

        for j in range(len(line)):
            # len(line) is expected to be 5, since there are five 
            # characters in each line of this part of the input

            if line[j] == '0':
                constr[i][j][1] = "None"
                constr[i+1][j][0] = "None"
                """ 0 indicates there's no constraint, so the second 
                element of the cell (i, j), which refers to its 
                relation with the cell underneath it, should be 
                "None". By the same token, the first element 
                of the cell (i+1, j) should be "None" as well."""

            elif line[j] == '^':
                constr[i][j][1] = "STD"
                constr[i+1][j][0] = "GTU"
                # STD = Smaller Than Down
                # GTU = Greater Than Up

            elif line[j] == 'v':
                constr[i][j][1] = "GTD"
                constr[i+1][j][0] = "STU"
                # GTD = Greater Than Down
                # STU = Smaller Than Up

    text_stream.close()
    # By this point, reading the input file has concluded

    ret = [initial_state, constr]
    # Returns the two lists that represent the initial state and 
    # all constraints, respectively
    return ret


def initialize_board(initial_state: list, constr: list) -> Board:
    """ The parameters are the initial state, represented as a five-by-five 
    list, and the list of constraints for all twenty-five cells. The function 
    instantiates twenty-five Cell objects with the given data and returns 
    a Board object."""

    all_cells = []
    # Will become a five-by-five list by the end of function
    # All Cell objects to be instantiated will be appended 
    # to this list, which is then used to instantiate the 
    # Board object

    for i in range(0,5):
        a_row = []
        for j in range(0,5):
            assign = initial_state[i][j]
            domain = [1, 2, 3, 4, 5]
            # The initial domain of an empty cell

            if assign == 0:
                assign = None
                # Zero indicates an empty cell
            else:
                domain = None
                # Domain doesn't apply to assigned cells

            a_row.append(Cell((i, j), assign, domain, constr[i][j]))
            # Instantiates the Cell object and appends it to the 
            # list of the row

        all_cells.append(a_row)

    # At this point all_cells is a five-by-five list that 
    # contains all twenty-five cells

    return Board(all_cells, constr)


def forward_checking(a_board: Board, a_cell: Cell) -> int:
    """ Conducts forward checking for the given assigned cell to 
    ensure there's no other cell in the same row or column with 
    the same assignment. Also reduces each neighbor's domain to 
    comply with the constraints, if any. Recursive calls to 
    itself are made to eventually check every cell on the board 
    for arc consistency."""

    """ The four methods of the Board class--go_up, go_down, go_left 
    and go_right--all throw a ValueError when the move goes beyond 
    the board's boundaries. These errors are caught in the except 
    statements below, and the respective variables are set as 
    None. If the move is legit, the method returns the destination 
    as a Cell object, and the corresponding variable (left, right 
    etc.) is turned into a reference (shallow copy) to that Cell."""

    if a_cell.domain == 0:
        return 1
    # Some of the recursive calls may encounter cases where the 
    # domain of the origin cell has been reduced to none, which 
    # indicates that there's no solution and that the program 
    # should halt. This if statement is written at the very 
    # beginning so that the recursive call could be termianted 
    # immediately if this were the case.

    try:
        left = a_board.go_left(a_cell)
    except ValueError:
        left = None

    try:
        right = a_board.go_right(a_cell)        
    except ValueError:
        right = None

    try:
        up = a_board.go_up(a_cell)
    except ValueError:
        up = None

    try:
        down = a_board.go_down(a_cell)
    except ValueError:
        down = None

    neighbors = [up, down, left, right]
    # The Cell objects in the list are arranged in the same order
    # as the constraint field of the Cell class (which stores 
    # the strings that represent the constraints regarding the
    # cell's neighbors): the neighbor above ("up"), below ("down"),
    # left and then right

    up_ret = 0
    down_ret = 0
    left_ret = 0
    right_ret = 0
    # The point is to initialize these variables. If the recursive 
    # calls in the code below are executed, these variables 
    # will hold the return values of those calls

    ret_vals = [up_ret, down_ret, left_ret, right_ret]
    # The variables to store the return values are arranged in 
    # the same order as the list of Cell objects above: up, 
    # down, left and right

    constr_strings = [["STU", "GTU"], ["STD", "GTD"],
            ["STL", "GTL"], ["STR", "GTR"]]
    # A list that contains all the strings that represent 
    # constraints regarding neighbors.
    # Arranged in the same order as the list of Cell objects 
    # above: the first sublist contains the two types of 
    # constraints for the neighbor above, the second sublist 
    # is for the neighbor below, followed by those for "left"
    # and "right"

    for i in range(len(neighbors)):
        if type(neighbors[i]) != None:
            # If the Cell object looked for was returned by
            # the methods of the Board class

            if neighbors[i].assign == None:
                # If the cell is empty, the indented code below 
                # will be run;
                # If the cell has been assigned a value, 
                # the program will jump to the recursive call ahead

                if a_cell.constr[i] == constr_strings[i][0]:
                # The list of Cell objects, the list of constraint 
                # strings and the list of return values all arrange 
                # their elements in the up-down-left-right order
                # Therefore the same index can locate the particular 
                # element for the same neighboring cell
                
                # The elements in constr_strings are ordered in such
                # a way that constr_strings[i][0] is always the string 
                # that denotes a "smaller than" relation, whereas
                # constr_strings[i][1] is the one that denotes a
                # "greater than" relation

                    if a_cell.assign != None:
                        # If the origin cell has been assigned
                        # a value

                        for j in range(len(neighbors[i].domain)):
                            if neighbors[i].domain[j] <= a_cell.assign:
                                neighbors[i].domain.pop(j)
                                # Remove the values that are smaller 
                                # than or equal to the origin's 
                                # assigned value
                    
                    else:
                        # If the origin cell has NOT been assigned 
                        # a value

                        # The domain list cannot possibly be empty 
                        # because an empty domain would've made the 
                        # function return 1 in the very beginning
                        
                        dom_min = min(a_cell.domain)
                        for j in range(len(neighbors[i].domain)):
                            if neighbors[i].domain[j] <= dom_min:
                                neighbors[i].domain.pop(j)
                                # Remove the values that are smaller 
                                # than or equal to the smallest value 
                                # in the origin's domain

                elif a_cell.constr[i] == constr_strings[i][1]:
                    # constr_strings[i][1] is always the string that
                    # refers to a "greater than" relation

                    if a_cell.assign != None:
                        for j in range(len(neighbors[i].domain)):
                            if neighbors[i].domain[j] >= a_cell.assign:
                                neighbors[i].domain.pop[j]

                    else:
                        dom_max = max(a_cell.domain)
                        for j in range(len(neighbors[i].domain)):
                            if neighbors[i].domain[j] >= dom_max:
                                neighbors[i].domain.pop(j)

                else:
                    # The case where there's no constraint regarding
                    # this neighbor

                    if a_cell.assign != None:
                        for j in range(len(neighbors[i].domain)):
                            if neighbors[i].domain[j] == a_cell.assign:
                                neighbors[i].domain.remove(a_cell.assign)
                                break
                        # If the origin cell has been assigned a value,
                        # remove that value from the neighbor's domain,
                        # since the same number can only show up once 
                        # in any row or column. Break the for loop after 
                        # the value has been removed.
                        # If the origin cell has NOT been assigned a
                        # value, no action needs to be taken. In the 
                        # recursive calls, the origin cell may not have 
                        # been assigned a value.

                if len(neighbors[i].domain) == 0:
                    return 1
                    # If an empty cell's domain has been reduced to none,
                    # return 1, which indicates the puzzle has no solution
                    # The return value will be caught by the function 
                    # that makes the call, which will then stop the program

                    # The domain field of a Cell is "None" only if the Cell
                    # has not been assigned a value, in which case the 
                    # entire code block will have been skipped due to the 
                    # "if neighbors[i].assign == None" statement above.
                    # Therefore this line does not incur a runtime error.

            return_vals[i] = forward_checking(a_board, neighbors[i])
            """ This line is executed if the neighbor has been assigned 
            a value or the neighbor's domain is not empty after the 
            reduction."""
       
    return max(return_vals)
    """ If any of the recursive calls returns one, there's no solution 
    to the puzzle. If any of the four elements of "return_vals" equals 
    one, the function will return one. The preceding function that made 
    the first call to forward_checking will stop the program if the 
    return value is one and continue if it's zero."""



