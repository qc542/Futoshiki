from Futoshiki import *
import random


def load_input_test() -> int:
    [initial_state, constr] = load_input("input1.txt")
    
    print("load_input returns two lists: initial_state and constr.\n")
    print("The following is load_input printed in its raw form: \n\n")
    print(initial_state)
    print('\n')

    print("The following is constr printed in its raw form: \n\n")
    print(constr)
    print('\n')

    for a_row in initial_state:
        print(a_row)
        print('\n')

    for i in range(len(constr)):
        for j in range(len(constr[i])):
            print("Cell coordinates: Row " + str(i) + ", Column " +
                    str(j) + '\n')
            print("Cell constraints: \n")
            
            for k in range(len(constr[i][j])):
                print(constr[i][j][k])
                if (k != (len(constr[i][j]) - 1)):
                    print(' ')

            print('\n')

    return 0


def initialize_board_test() -> int:
    """ Tests the instantiation of both the Board class and the 
    Cell class, since initialize_board uses both."""

    [initial_state, constr] = load_input("input1.txt")
    a_board = initialize_board(initial_state, constr)

    for i in range(0,5):
        print("Row " + str(i) + ": \n")
        for j in range(0,5):
            a_cell = a_board.cells[i][j]
            print("Cell coordinates: " + str(a_cell.coord) + '\n')
            print("Assignment: " + str(a_cell.assign) + '\n')
            print("Domain: " + str(a_cell.domain) + '\n')
            print("Constraints: " + str(a_cell.constr) + '\n')
            print('\n')

        print('\n')

    return 0


def board_moves_test(a_board: Board) -> int:
    """ Tests the four methods of the Board class that are for locating a 
    given cell's neighbors: go_up, go_down, go_left and go_right."""

    for i in range(0, 5):
        for j in range(0, 5):
            origin = Cell((i, j), None, None, None)
            print("Origin: " + str(origin.coord) + '\n')

            try:
                left = a_board.go_left(origin)
                print("To the left: " + str(left.coord) + '\n')
            except ValueError:
                print("No cell exists to the left of the origin.\n")

            try:
                right = a_board.go_right(origin)
                print("To the right: " + str(right.coord) + '\n')
            except ValueError:
                print("No cell exists to the right of the origin.\n")

            try:
                up = a_board.go_up(origin)
                print("Above: " + str(up.coord) + '\n')
            except ValueError:
                print("No cell exists above the origin.\n")

            try:
                down = a_board.go_down(origin)
                print("Below: " + str(down.coord) + '\n')
            except ValueError:
                print("No cell exists below the origin.\n")

            print('\n')

    return 0


def print_board(a_board: Board) -> int:
    """ Given a Board object as the parameter, the function prints 
    out all the cells on the board one by one in an easy-to-read 
    format. In hindsight, I wrote this function without being 
    aware that it's almost identical to initialize_board_test. 
    Regardless, I decided to keep them both; this function was 
    named for a more general purpose and therefore will be called 
    more often than initialize_board_test."""

    for a_row in range(len(a_board.cells)):
        for a_column in range(len(a_board.cells[a_row])):
            print("Cell coordinates: Row " + str(a_row) + ", Column " 
                    + str(a_column))
            cell = a_board.cells[a_row][a_column]
            print("Assigned value: " + str(cell.assign))
            print("Domain: " + str(cell.domain))
            print("Constraints: " + str(cell.constr))
            print('\n', end = '')
            """ Python 3 automatically adds a newline character to 
            each call to print(). Therefore, to print only one empty 
            line, add "end = ''" as the second argument."""

    print("All cells on the board have been printed.")
    print("*****************************************************")
    return 0

def forward_checking_test(a_board: Board) -> int:
    """ The function takes a Board object as the parameter and looks for 
    the first cell on the board that has been assigned a value. Once found, 
    that cell is passed to forward_checking. If forward_checking returns 0, 
    that indicates the operation was conducted successfully, and forward_-
    checking_test passes the Board object to print_board. If forward_chec-
    king returns 1, that indicates the puzzle has no solution, and forwad_-
    checking_test prints a relevant message."""


    
    failure = start_fc(a_board, a_board.cells[0][0])
    if not failure:
        print("The function forward_checking was initially " + 
        "called on the cell " + str(a_board.cells[0][0].coord) + 
        "; the function returned 0. Forward checking was " + 
        "conducted succesfully. The board following the " + 
        " completion of forward checking is shown below: """, 
        end = "\n\n")
        print_board(a_board)

    else:
        print("The function forward_checking returned 1 when " + 
        "it was initially called on the cell " + 
        str(a_board.cells[0][0].coord) + ". There is at least one " + 
        "cell on the board whose domain has been reduced to " + 
        "none. Therefore there is no solution to this puzzle.")

    return 0

def calc_degree_test(a_board: Board) -> int:
    """ The function takes a Board object as the parameter and tests the 
    calc_degree function. It loops through all cells on the given board 
    and prints the degree of each cell in a grid format."""

    for i in range(0, 5):
        for j in range(0, 5):
            print(str(calc_degree(a_board, a_board.cells[i][j])) + ' ',
                    end = '')
        print('\n\n', end = '')

    print("The degree of each cell has been printed.")
    return 0


def select_unassigned_cell_test(a_board: Board) -> int:
    
    selected = select_unassigned_cell(a_board)
    print("The following outcomes were obtained before forward " +
            "checking is applied to the given board: ")
    print("The cell " + str(selected.coord) + " was returned by " +
            "the function select_unassigned_cell.")
    print("The degree of the cell is " + str(calc_degree(a_board, selected)) +
            ".")
    print("There are " + str(len(selected.domain)) + " values remaining " +
            "in the cell's domain: " + str(selected.domain))
    
    for i in range(0, 41):
        print('*', end='')
    print('\n', end='')

    print("Now applying forward checking to the board:")
    print("Calling start_fc on the board...")
    if not start_fc(a_board, a_board.cells[0][0]):
        print("Done.")
        selected = select_unassigned_cell(a_board)
        print("The following outcomes were obtained after forward " + 
                "checking has been applied: ")
        print("The cell " + str(selected.coord) + " was returned by " +
                "the function select_unassigned_cell.")
        print("The degree of the cell is " +
                str(calc_degree(a_board, selected)) + ".")
        print("There are " + str(len(selected.domain)) + " values remaining " +
                "in the cell's domain: " + str(selected.domain))
    
    else:
        print("start_fc returned 1 instead of 0.")

    return 0


def is_complete_test(a_board: Board) -> int:
    if is_complete(a_board):
        print("The function is_complete indicates all cells on the " +
                "given board have been assigned a value.")
    else:
        print("The function is_complete indicates NOT all cells on " +
                "the given board have been assigned a value.")

    return 0


def order_domain_values_test(a_cell: Cell) -> int:
    print("Upon sorting, the domain values of the given cell " + 
                "are ordered as " + str(order_domain_values(a_cell)))
    return 0


def is_consistent_test(a_board: Board) -> int:
    print("Applying forward checking to the given board:")
    print("Calling start_fc on the given board...")
    if not start_fc(a_board, a_board.cells[0][0]):
        print("Forward checking succeeded.")
    else:
        print("start_fc returned 1 instead of 0; test terminated.")
        return 1

    selected = select_unassigned_cell(a_board)
    print("The cell " + str(selected.coord) + " has been selected as " +
            "the next variable to be assigned a value.")
    print("The cell's constraints are: " + str(selected.constr))
    
    if not order_domain_values(selected):
        print("The cell's domain values have been sorted: " +
                str(selected.domain))
    
    for i in range(len(selected.domain)):
        if is_consistent(a_board, selected, selected.domain[i]):
            print("The cell would be consistent with the rest of the " +
                    "assignment if it were assigned " + 
                    str(selected.domain[i]) + '.')
        else:
            print("The cell would be INCONSISTENT with the rest of the " +
                    "assignment if it were assigned " +
                    str(selected.domain[i]) + '.')

    others = []
    for i in range(1,6):
        if i not in selected.domain: others.append(i)
        # Compiles a list of integers that are not in the cell's domain

    if len(others) > 0:
        # If there are values not present in the cell's domain,
        # call is_consistent on these values to verify the outcomes

        print("\n\nThese values are not in the cell's domain: " +
                str(others))
        print("Now calling is_consistent on these values:")
        for i in range(len(others)):
            if is_consistent(a_board, selected, others[i]):
                print("The cell would be consistent with the rest of the " +
                        "assignment if it were assigned " + 
                        str(others[i]) + '.')
            else:
                print("The cell would be INCONSISTENT with the rest of the " +
                        "assignment if it were assigned " +
                        str(others[i]) + '.')

    print("\nTest complete.")
    return 0


#load_input_test()
#initialize_board_test()
[initial_state, constr] = load_input("Input0.txt")
a_board = initialize_board(initial_state, constr)
#board_moves_test(a_board)
#fct_ret = forward_checking_test(a_board)
#print_board(a_board)
#calc_degree_test(a_board)
#select_unassigned_cell_test(a_board)
#is_complete_test(a_board)
#order_domain_values_test(a_board.cells[0][0])
is_consistent_test(a_board)
