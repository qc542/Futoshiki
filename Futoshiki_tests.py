from Futoshiki import *

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
            a_cell = a_board.all_cells[i][j]
            print("Cell coordinates: " + str(a_cell.coord) + '\n')
            print("Assignment: " + str(a_cell.assign) + '\n')
            print("Domain: " + str(a_cell.domain) + '\n')
            print("Constraints: " + str(a_cell.constr) + '\n')
            print('\n')

        print('\n')

    return 0


load_input_test()
initialize_board_test()
