import numpy as np
from scipy.stats import mode
import pygame


#==== DEBUG FUNCTIONS ===============================================================================
def print_sys( _str ):
    print("[SYSTEM]\t\t" + _str)

def print_imr( _str ):
    print("[IMG REC]\t\t" + _str)

def print_grph( _str ):
    print("[GRAPHICS]\t\t" + _str)

def print_sim( _str ):
    print("[SIMULATOR]\t\t" + _str)

'''
Given an array of game boards, return a game board with the mode of every (x,y) in all the input game boards
'''
def mode_of_boards( boards ):
    output = np.zeros( ( len(boards[0]), len(boards[1]) ), np.int8 )
    combined_boards = np.dstack(boards.copy())

    for r in range( 0, len(boards[0]) ):
        for c in range( 0, len(boards[0][0]) ):
            output[r][c] = mode( combined_boards[r][c] )[0]


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
    screen.blit( img, ( dx*pos[0], dy*pos[1] ) )

