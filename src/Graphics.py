from misc import *
from sharedVars import *

import threading
import time
import pygame
pygame.init()




class Graphics( threading.Thread ):
    def __init__( self, name ):
        threading.Thread.__init__(self)
        print_grph("Graphics System Started")
        print_grph("\tThread name: " + name )

        # Calibration Var
        game_x_f, game_y_f = 0, 0
        game_w_f, game_h_f = 0.7, 1

        menu_x_f, menu_y_f = 0.7, 0
        menu_w_f, menu_h_f = 0.3, 1


        info = pygame.display.Info()
        screen_width, screen_height = info.current_w, info.current_h
        window_width, window_height = screen_width - 10, screen_height - 10

        self.game_w = game_w_f * window_width
        self.game_h = game_h_f * window_height
        self.game_x = game_x_f * window_width
        self.game_y = game_y_f * window_height

        self.menu_w = menu_w_f * window_width
        self.menu_h = menu_h_f * window_height
        self.menu_x = menu_x_f * window_width
        self.menu_y = menu_y_f * window_height


        self.screen = pygame.display.set_mode((window_width,window_height))
        self.run_timer = 0.1

        self.game_screen = pygame.Surface( (self.game_w, self.game_h) )
        self.menu_screen = pygame.Surface( (self.menu_w, self.menu_h) )

        self.game_screen.fill( (255,0,255) )
        self.menu_screen.fill( (0,255,255) )



    def run( self ):
        global BOARD_STATE
        global DONE

        while DONE:
            time.sleep( self.run_timer )

            self.screen.blit( self.game_screen, (self.game_x, self.game_y) )
            self.screen.blit( self.menu_screen, (self.menu_x, self.menu_y) )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print_grph("Closing")
                    DONE = False
                    break

            pygame.display.flip()

        pygame.quit()
        quit()

