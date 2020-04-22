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
    # All Cell objects to be instantiated will be appended 
    # to this list, which is then used to instantiate the 
    # Board object

    for i in range(0,5):
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

            all_cells.append(Cell((i, j), assign, domain, constr[i][j]))
            # Instantiates the Cell object and appends it to the list

    return Board(all_cells, constr)

