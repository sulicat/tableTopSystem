import sys
sys.path.append("../../")
import Graphics
import misc
import numpy as np
import pygame


# given a col of 8 rgb colors
# this program will display them on the colors across 7 cells down with decreasing
# brightness

class colorTest( Graphics.Game ):
    def __init__(self, name):
        super().__init__(name)
        self.initial_colors = [ (255, 0, 0),
                                (0, 255, 0),
                                (0, 0, 255),
                                (255, 0, 255),
                                (0, 255, 255),
                                (255, 255, 0),
                                (255, 255, 255),
                                (0, 0, 0)
        ]

        self.colors = []


        mult = 0.8

        for r in range( 0,len(self.initial_colors) ):
            self.colors.append( [ self.initial_colors[r] ] )

        for c in range(1,8):
            for r in range(0, len(self.colors) ):
                self.colors[r].append(( int(self.colors[r][c-1][0]*mult),
                                        int(self.colors[r][c-1][1]*mult),
                                        int(self.colors[r][c-1][2]*mult) ))

                #self.colors[r].append( (0,0,1) )



    def start(self):
        print("start test")

    def render(self, screen, board):
        w, h = screen.get_width(), screen.get_height()

        screen.fill( (0,0,0) )
        misc.render_grid( screen, thickness=4 )

        for r in range(0,8):
            for c in range( 0,8 ):
                misc.render_cellFill( screen, c, r, color = self.colors[r][c], max_r = 8, max_c = 8 )


    def end(self):
        print("end test")
