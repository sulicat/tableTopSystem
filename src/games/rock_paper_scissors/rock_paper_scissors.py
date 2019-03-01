import sys
sys.path.append("../../")
import Graphics
import misc
import numpy as np
import pygame


class rockPaperScissors( Graphics.Game ):
    def __init__(self, name):
        super().__init__(name)
        self.rock = pygame.image.load("../resources/rock_paper_scissors/rock.png")
        self.paper = pygame.image.load("../resources/rock_paper_scissors/paper.png")
        self.scissors = pygame.image.load("../resources/rock_paper_scissors/scissors.png")
        self.rock = pygame.transform.scale(self.rock, (100,100))
        self.paper = pygame.transform.scale(self.paper, (100,100))
        self.scissors = pygame.transform.scale(self.scissors, (100,100))

        self.mode = "choose"


    def start(self):
        print("start rps")

    def render(self, screen, board):
        w, h = screen.get_width(), screen.get_height()
        screen.fill( (0,0,0) )


        if( self.mode == "choose" ):
            render_choose_mode

    def render_choose_mode(self):
        # we will render the options in the middle of the screen
        screen.blit( self.rock, ( 100,100 ) )



    def end(self):
        print("end rps")
