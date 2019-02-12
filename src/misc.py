import numpy as np

from scipy.stats import mode

#==== DEBUG FUNCTIONS ===============================================================================
def print_sys( _str ):
    print("[SYSTEM]\t\t" + _str)

def print_imr( _str ):
    print("[IMG REC]\t\t" + _str)

def print_grph( _str ):
    print("[GRAPHICS]\t\t" + _str)

def print_sim( _str ):
    print("[SIMULATOR]\t\t" + _str)


def mode_of_boards( boards ):
    output = np.zeros( ( len(boards[0]), len(boards[1]) ), np.int8 )
    combined_boards = np.dstack(boards.copy())

    for r in range( 0, len(boards[0]) ):
        for c in range( 0, len(boards[0][0]) ):
            output[r][c] = mode( combined_boards[r][c] )[0]


    return output
