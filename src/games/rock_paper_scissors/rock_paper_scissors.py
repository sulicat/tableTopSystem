import sys
sys.path.append("../../")
import Graphics
import misc
import numpy as np
import pygame
import random

class rockPaperScissors( Graphics.Game ):
    def __init__(self, name):
        super().__init__(name)

        self.font = pygame.font.SysFont('Comic Sans MS', 65)
        self.font_big = pygame.font.SysFont('Comic Sans MS', 100)

        self.images = {}
        self.images["rock"] = pygame.image.load("../resources/rock_paper_scissors/rock.png")
        self.images["paper"] = pygame.image.load("../resources/rock_paper_scissors/paper.png")
        self.images["scissors"] = pygame.image.load("../resources/rock_paper_scissors/scissors.png")
        self.images["rock"] = pygame.transform.scale(self.images["rock"], (100,100))
        self.images["paper"] = pygame.transform.scale(self.images["paper"], (100,100))
        self.images["scissors"] = pygame.transform.scale(self.images["scissors"], (100,100))

        self.arrow_up = pygame.image.load("../resources/icon_arrow_up.png")
        self.arrow_up = pygame.transform.scale(self.arrow_up, (100,100))

        self.mode = "choose"
        self.choice = "none"
        self.countdown_max = 39
        self.countdown = 39

    def start(self):
        print("start rps")

    def render(self, screen, board):
        w, h = screen.get_width(), screen.get_height()
        screen.fill( (0,0,0) )

        y_pos = int((h/2) - (self.images["rock"].get_size()[1]/2)) - 100
        item_halfW = int(self.images["rock"].get_size()[0]/2)
        item_offset = int(w/3) - item_halfW

        arrow_y_pos = h - 50 - (self.arrow_up.get_size()[1])

        if( self.mode == "choose" ):
            # render text at the top to tell the user to select one of the three options
            text = self.font.render( "Choose Rock, Paper or Scissors", False, (255,0,0) )
            screen.blit( text, ( int(text.get_size()[0]/2), 100 ) )
            # render the 3 options that the user has, centered at thirds of the screen
            #screen.blit( self.rock, ( item_offset, y_pos ) )
            #screen.blit( self.paper, ( item_offset * 2, y_pos ) )
            #screen.blit( self.scissors, ( item_offset * 3, y_pos ) )
            # Render the arrows indicating to the user to place their selection on the
            # block above
            #screen.blit( self.arrow_up, ( item_offset, arrow_y_pos ) )
            #screen.blit( self.arrow_up, ( item_offset * 2, arrow_y_pos ) )
            #screen.blit( self.arrow_up, ( item_offset * 3, arrow_y_pos ) )

            misc.render_imageInCell( screen, self.images["rock"], (1,2) )
            misc.render_imageInCell( screen, self.images["paper"], (4,2) )
            misc.render_imageInCell( screen, self.images["scissors"], (7,2) )

            misc.render_imageInCell( screen, self.arrow_up, (1,5) )
            misc.render_imageInCell( screen, self.arrow_up, (4,5) )
            misc.render_imageInCell( screen, self.arrow_up, (7,5) )

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

            arr_scissors = board[ 0:8, 0:2 ]
            arr_paper = board[ 0:8, 3:5 ]
            arr_rock = board[ 0:8, 6:8 ]

            selector_id = 25
            if( selector_id in arr_rock ):
                self.choice = "rock"
                self.mode = "round"
            elif( selector_id in arr_paper ):
                self.choice = "paper"
                self.mode = "round"
            elif( selector_id in arr_scissors ):
                self.choice = "scissors"
                self.mode = "round"

        elif( self.mode == "round" ):
            misc.render_imageInCell( screen, self.images[self.choice], (3,6) )
            misc.render_imageInCell( screen, self.images[self.choice], (4,6) )
            misc.render_imageInCell( screen, self.images[self.choice], (5,6) )

            if( self.countdown >= 0 ):
                text = self.font_big.render( "Computer Choosing in ", False, (255, 0, 255) )
                screen.blit( text, ( int( (w/2) - text.get_size()[0]/2), 100 ) )

                text = self.font_big.render( str(int(self.countdown/10)), False, (255, 0, 255) )
                screen.blit( text, ( int((w/2) - text.get_size()[0]/2), 200 ) )
                self.countdown -= 1

            else:
                self.countdown = self.countdown_max
                self.mode = "computer"
                self.computer_choice, temp = random.choice(list(self.images.items()))

        elif( self.mode == "computer" ):
            misc.render_imageInCell( screen, self.images[self.choice], (3,6) )
            misc.render_imageInCell( screen, self.images[self.choice], (4,6) )
            misc.render_imageInCell( screen, self.images[self.choice], (5,6) )

            misc.render_imageInCell( screen, self.images[self.computer_choice], (3,1) )
            misc.render_imageInCell( screen, self.images[self.computer_choice], (4,1) )
            misc.render_imageInCell( screen, self.images[self.computer_choice], (5,1) )

            if( self.computer_choice == self.choice ):
                text = self.font_big.render( "It's a draw", False, (255, 0, 255) )

            elif( self.computer_choice == "scissors" and self.choice == "paper" ):
                text = self.font_big.render( "You're a LOSER", False, (255, 0, 255) )
            elif( self.computer_choice == "paper" and self.choice == "rock" ):
                text = self.font_big.render( "You're a LOSER", False, (255, 0, 255) )
            elif( self.computer_choice == "rock" and self.choice == "scissors" ):
                text = self.font_big.render( "You're a LOSER", False, (255, 0, 255) )

            else:
                text = self.font_big.render( "WINNER", False, (255, 0, 255) )


            screen.blit( text, ( int((w/2) - text.get_size()[0]/2), h/2 - 50 ) )
            self.countdown -= 1
            text = self.font_big.render( str(int(self.countdown/10)), False, (255, 0, 255) )
            screen.blit( text, ( 50, 50 ) )

            if( self.countdown < 0 ):
                self.mode = "choose"
                self.countdown = self.countdown_max





    def end(self):
        print("end rps")
