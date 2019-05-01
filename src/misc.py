import numpy as np
from scipy.stats import mode
import pygame


font_small = pygame.font.SysFont('Comic Sans MS', 35)

#==== DEBUG FUNCTIONS ===============================================================================
def print_sys( _str ):
    print("[SYSTEM]\t\t" + _str)

def print_imr( _str ):
    print("[IMG REC]\t\t" + _str)

def print_grph( _str ):
    print("[GRAPHICS]\t\t" + _str)

def print_sim( _str ):
    print("[SIMULATOR]\t\t" + _str)



board_index = [ [0,  32, 0,  31, 0,  30, 0,  29],
                [28, 0,  27, 0,  26, 0,  25, 0],
                [0,  24, 0,  23, 0,  22, 0,  21],
                [20, 0,  19, 0,  18, 0,  17, 0],
                [0,  16, 0,  15, 0,  14, 0,  13],
                [12, 0,  11, 0,  10, 0,  9,  0],
                [0,  8,  0,  7,  0,  6,  0,  5],
                [4,  0,  3,  0,  2,  0,  1,  0] ]


'''
Given an array of game boards, return a game board with the mode of every (x,y) in all the input game boards
'''
def mode_of_boards( boards ):
    if( len(boards) > 1 ):
        output = np.zeros( ( len(boards[0]), len(boards[1]) ), np.int8 )
        combined_boards = np.dstack(boards.copy())

        for r in range( 0, len(boards[0]) ):
            for c in range( 0, len(boards[0][0]) ):
                output[r][c] = mode( combined_boards[r][c] )[0]

    elif len(boards) == 1:
        return boards[0]

    return output


'''
Helper method to render a grid on the given surface
'''
def render_grid( screen, c_x = 8, c_y = 8, thickness = 2, color = (255,255,255)):
    w,h = screen.get_width(), screen.get_height()
    dx, dy = w/c_x, h/c_y

    for i in range (0,c_x+1):
        pygame.draw.line( screen, color, (i*dx, 0), (i*dx, h) )

    for i in range (0,c_y+1):
        pygame.draw.line( screen, color, (0, i*dy), (w, i*dy) )


def render_grid_nums( screen, c_x = 8, c_y = 8, thickness = 2, color = (255,255,255)):
    w,h = screen.get_width(), screen.get_height()
    dx, dy = w/c_x, h/c_y

    for r in range (0,c_y):
        for c in range(0,c_x):
            text = font_small.render( str(r)+","+str(c_x-c-1), False, color )
            screen.blit( text, ( dx*c, dy*r ) )


def render_checkers_IDs( screen, c_x = 8, c_y = 8, thickness = 2, color = (255,255,255)):
    global board_index
    w,h = screen.get_width(), screen.get_height()
    dx, dy = w/c_x, h/c_y

    for r in range (0,c_y):
        for c in range(0,c_x):
            if( board_index[r][c] != 0 ):
                text = font_small.render( str(board_index[r][c]), False, color )
                screen.blit( text, ( dx*c + int(dx/2), dy*r + int(dy/2) ) )


'''
Helper method to fill a cell with a color in a given pygame surface
'''
def render_cellFill( screen, r, c, color = (255,0,0), max_r = 8, max_c = 8 ):
    w,h = screen.get_width(), screen.get_height()
    dx, dy = w/max_r, h/max_c
    pygame.draw.rect( screen, color, (r*dx, c*dy, dx, dy) )



'''
Helper method to fill a cell with a color in a given pygame surface
'''
def render_cellBorder( screen, r, c, color = (255,0,0), max_r = 8, max_c = 8, border = 2 ):
    w,h = screen.get_width(), screen.get_height()
    dx, dy = w/max_r, h/max_c
    pygame.draw.rect( screen, color, (r*dx, c*dy, dx, dy), border )



'''
Helper method to draw an image in a set of cells
'''
def render_imageInCell( screen, img, pos, max_r = 8, max_c = 8 ):
    w,h = screen.get_width(), screen.get_height()
    dx, dy = w/max_c, h/max_r
    px = int((dx - 100) / 2)
    py = int((dy - 100) / 2)
    screen.blit( img, ( dx*pos[0] + px, dy*pos[1] + py ) )

