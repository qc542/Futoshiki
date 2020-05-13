from Futoshiki import *


def print_board_assign(a_board: Board) -> int:
    """ Prints all assigned value on the board in a grid layout. """
    for i in range(0, 5):
        for j in range(0, 5):
            if a_board.cells[i][j].assign == None:
                print(0, end=' ')
            else:
                print(a_board.cells[i][j].assign, end=' ')
        print('\n', end='')

    return 0
        
