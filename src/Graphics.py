from misc import *
import sharedVars

import threading
import time
import pygame
from pygame.locals import *
pygame.init()
pygame.font.init()


# -- Load all the assets used by the Graphics Engine -----------------------------
font_1 = pygame.font.SysFont('Comic Sans MS', 45)

img_arrow_up = pygame.image.load("../resources/icon_arrow_up.png")
img_arrow_up = pygame.transform.scale(img_arrow_up, (100,100))

img_arrow_down = pygame.image.load("../resources/icon_arrow_down.png")
img_arrow_down = pygame.transform.scale(img_arrow_down, (100,100))

img_close = pygame.image.load("../resources/icon_close.png")
img_close = pygame.transform.scale(img_close, (100,100))

img_select = pygame.image.load("../resources/icon_accept.png")
img_select = pygame.transform.scale(img_select, (100,100))


'''
This class is the class that functions as a template for different games added to this system
Every game will habe a start(), render() and end() function
All games added to this system will inherit from this class
'''
class Game():
    def __init__(self, name):
        self.name = name

    def start(self):
        print("empty game: start")

    def render(self, screen, board):
        print("empty game: render")

    def end(self):
        print("empty game: end")


'''
This is the main Graphics object
- It inherits from a thread, and therefore functions asyncronosly from the rest of the program
- This is the class responsible for:
   - Getting and publishing data from the image recognition system to the outside games
   - Displaying and controlling the main menu and select screen
   - Sending inputs and render commands to selected games.
'''

class Graphics( threading.Thread ):
    def __init__( self, name ):
        threading.Thread.__init__(self)
        print_grph("Graphics System Started")
        print_grph("\tThread name: " + name )

        # Calibration Var
        game_x_f, game_y_f = 0.03, 0
        game_w_f, game_h_f = 0.6, 1

        menu_x_f, menu_y_f = 0.65, 0
        menu_w_f, menu_h_f = 0.11,1

        info = pygame.display.Info()
        #screen_width, screen_height = int(info.current_w*0.5), int(info.current_h)
        screen_width, screen_height = info.current_w, int(info.current_h)
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
        #self.screen = pygame.display.set_mode((window_width,window_height), pygame.FULLSCREEN)

        self.run_timer = 0.1

        self.game_screen = pygame.Surface( (self.game_w, self.game_h) )
        self.menu_screen = pygame.Surface( (self.menu_w, self.menu_h) )

        self.game_screen.fill( (0,0,0) )
        self.menu_screen.fill( (0,0,0) )

        # Game Control
        self.state = "Boot"
        self.selector_id = 31
        self.games = []
        self.current_game = -1
        self.current_menu_offset = 0
        self.open_for_commands = True


    def addGame( self, game ):
        self.games.append(game)

    def getScreen( self ):
        print("test:")

    def run( self ):
        global font_1
        global img_arrow_up
        global img_arrow_down
        global img_close
        global img_select

        while sharedVars.DONE:
            time.sleep( self.run_timer )
            print_grph( self.state )
            print(sharedVars.BOARD_STATE)

            #---- Graphics Loop -------------------------------------------------------------
            self.game_screen.fill( (0,0,0) )
            self.menu_screen.fill( (0,0,0) )

            # pass the screen render to the game
            #  also pass the state of the system
            if self.state == "Game":
                self.menu_screen.fill( (0,0,0) )

                # check if 31 is placed on the column
                if self.selector_id not in sharedVars.BOARD_STATE:
                    self.open_for_commands = True
                    print_grph("OPEN FOR COMMANDS")

                if self.selector_id in sharedVars.BOARD_STATE and self.open_for_commands == True:
                    self.state = "Menu"
                    self.open_for_commands = False

                else:
                    self.games[self.current_game].render( self.game_screen, sharedVars.BOARD_STATE.copy() )


            # start the sytem by opening the menu.
            elif self.state == "Boot":

                # check if 31 is placed on the column
                if self.selector_id not in sharedVars.BOARD_STATE:
                    self.open_for_commands = True
                    print_grph("OPEN FOR COMMANDS")


                if self.open_for_commands == True:
                    self.game_screen.fill( (0,0,0) )
                    text = font_1.render( "Place Selector", False, (255,255,255))
                    self.menu_screen.blit(text, (0,100))
                    if self.selector_id in sharedVars.BOARD_STATE:
                        self.state = "Menu"



            else:
                self.menu_screen.fill( (66,188,168) )
                item_height = self.menu_h / 5
                # render menu items
                # the menu will contain 5 items
                #  X
                #  ^
                #  G
                #  V
                #  GO

                self.menu_screen.blit(img_close, ( (self.menu_w / 2) - (img_close.get_size()[0]/2),
                                                   (item_height*0) + (item_height/2) - (img_close.get_size()[1]/2) )
                )

                self.menu_screen.blit(img_arrow_up, ( (self.menu_w / 2) - (img_arrow_up.get_size()[0]/2),
                                                      (item_height*1) + (item_height/2) - (img_arrow_up.get_size()[1]/2) )
                )

                self.menu_screen.blit(img_arrow_down, ( (self.menu_w / 2) - (img_arrow_down.get_size()[0]/2),
                                                        (item_height*3) + (item_height/2) - (img_arrow_down.get_size()[1]/2) )
                )

                self.menu_screen.blit(img_select, ( (self.menu_w / 2) - (img_select.get_size()[0]/2),
                                                      (item_height*4) + (item_height/2) - (img_select.get_size()[1]/2) )
                )


                if( self.current_menu_offset >= 0 and self.current_menu_offset < len(self.games) ):
                    text_game1 = font_1.render( self.games[self.current_menu_offset].name, False, (255,0,0) )
                    self.menu_screen.blit( text_game1, ((self.menu_w / 2) - text_game1.get_width()/2,
                                                        (item_height*2) + (item_height/2)))

                    # previous selection
                    if( self.current_menu_offset >= 1 ):
                        temp_str = self.games[self.current_menu_offset-1].name
                    else:
                        temp_str = "..."

                    text_game2 = font_1.render( temp_str, False, (100,100,0) )
                    self.menu_screen.blit( text_game2, ((self.menu_w / 2) - text_game2.get_width()/2,
                                                        (item_height*2) + (item_height/2) - int(text_game2.get_height()*2.2) ))

                    # next selection
                    if( self.current_menu_offset < len(self.games)-1 ):
                        temp_str = self.games[self.current_menu_offset+1].name
                    else:
                        temp_str = "..."

                    text_game2 = font_1.render( temp_str, False, (100,100,0) )
                    self.menu_screen.blit( text_game2, ((self.menu_w / 2) - text_game2.get_width()/2,
                                                        (item_height*2) + (item_height/2) + int(text_game2.get_height()*2.2) ))



                # check if 31 is placed on the column
                if self.selector_id not in sharedVars.BOARD_STATE:
                    self.open_for_commands = True
                    print_grph("OPEN FOR COMMANDS")


                # ---- Input Control For Menu ----------------------------------------------------
                right_col = [row[0] for row in sharedVars.BOARD_STATE]
                if( self.open_for_commands ):

                    # 7th rows... Exit
                    if( right_col[0] == self.selector_id ):
                        self.state = "Boot"
                        self.open_for_commands = False

                    # top 2 rows... up arrow
                    if( right_col[1] == self.selector_id or right_col[2] == self.selector_id ):
                        if( self.current_menu_offset > 0 ):
                            self.current_menu_offset -= 1
                        self.open_for_commands = False

                    # 6th rows... down arrow
                    if( right_col[5] == self.selector_id or right_col[6] == self.selector_id ):
                        if( self.current_menu_offset < len(self.games)-1 ):
                            self.current_menu_offset += 1
                        self.open_for_commands = False

                    # top row... Select
                    if( right_col[7] == self.selector_id ):
                        self.current_game = self.current_menu_offset
                        self.games[self.current_game].start()
                        self.state = "Game"
                        self.open_for_commands = False



            self.screen.blit( self.game_screen, (self.game_x, self.game_y) )
            self.screen.blit( self.menu_screen, (self.menu_x, self.menu_y) )
            #--------------------------------------------------------------------------------


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print_grph("Closing")
                    DONE = False
                    break

            pygame.display.flip()

        pygame.quit()
        quit()

