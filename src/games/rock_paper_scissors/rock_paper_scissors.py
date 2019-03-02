import sys
sys.path.append("../../")
import Graphics
import misc
import numpy as np
import pygame


class rockPaperScissors( Graphics.Game ):
    def __init__(self, name):
        super().__init__(name)

        self.font = pygame.font.SysFont('Comic Sans MS', 65)

        self.rock = pygame.image.load("../resources/rock_paper_scissors/rock.png")
        self.paper = pygame.image.load("../resources/rock_paper_scissors/paper.png")
        self.scissors = pygame.image.load("../resources/rock_paper_scissors/scissors.png")
        self.arrow_up = pygame.image.load("../resources/icon_arrow_up.png")
        self.rock = pygame.transform.scale(self.rock, (100,100))
        self.paper = pygame.transform.scale(self.paper, (100,100))
        self.scissors = pygame.transform.scale(self.scissors, (100,100))
        self.arrow_up = pygame.transform.scale(self.arrow_up, (100,100))


        self.mode = "choose"
        self.choice = "none"


    def start(self):
        print("start rps")

    def render(self, screen, board):
        w, h = screen.get_width(), screen.get_height()
        screen.fill( (0,0,0) )

        y_pos = int((h/2) - (self.rock.get_size()[1]/2)) - 100
        item_halfW = int(self.rock.get_size()[0]/2)
        item_offset = int(w/3) - item_halfW

        arrow_y_pos = h - 50 - (self.arrow_up.get_size()[1])

        if( self.mode == "choose" ):
            # render text at the top to tell the user to select one of the three options
            text = self.font.render( "Choose Rock, Paper or Scissors", False, (255,0,0) )
            screen.blit( text, ( int(text.get_size()[0]/2), 100 ) )
            # render the 3 options that the user has, centered at thirds of the screen
            screen.blit( self.rock, ( item_offset, y_pos ) )
            screen.blit( self.paper, ( item_offset * 2, y_pos ) )
            screen.blit( self.scissors, ( item_offset * 3, y_pos ) )
            # Render the arrows indicating to the user to place their selection on the
            # block above
            screen.blit( self.arrow_up, ( item_offset, arrow_y_pos ) )
            screen.blit( self.arrow_up, ( item_offset * 2, arrow_y_pos ) )
            screen.blit( self.arrow_up, ( item_offset * 3, arrow_y_pos ) )


            # if this is the first time we have entered the choose method
            # then we want to update the image recognition mask in order to allow it to
            # ignore the parts of the image we drew the busy graphics on
            # .... tbd
            # SULI: do this


            # Rendering is done. Now we will check the posision of the peices
            # the positions we care about are the following:
            # [ 0  0  0  0  0  0  0  0] <<-- NO
            # [ 0  0  0  0  0  0  0  0] <<-- NO
            # [ 0  0  0  0  0  0  0  0] <<-- NO
            # [ 0  0  0  0  0  0  0  0] <<-- NO
            # [ x  x  0  y  y  0  z  z] <<-- YES
            # [ x  x  0  y  y  0  z  z] <<-- YES
            # [ x  x  0  y  y  0  z  z] <<-- YES
            # [ 0  0  0  0  0  0  0  0] <<-- NO

            arr_rock = board[ 4:7, 0:2 ]
            arr_paper = board[ 4:7, 3:5 ]
            arr_scissors = board[ 4:7, 6:8 ]

            selector_id = 12
            if( selector_id in arr_rock ):
                self.choice = "rock"
            elif( selector_id in arr_paper ):
                self.choice = "paper"
            elif( selector_id in arr_scissors ):
                self.choice = "scissors"


    def end(self):
        print("end rps")
