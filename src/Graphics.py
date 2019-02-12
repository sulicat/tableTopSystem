from misc import *
import sharedVars

import threading
import time
import pygame
from pygame.locals import *
pygame.init()
pygame.font.init()

font_1 = pygame.font.SysFont('Comic Sans MS', 30)

img_arrow_up = pygame.image.load("../resources/icon_arrow_up.png")
img_arrow_up = pygame.transform.scale(img_arrow_up, (100,100))

img_arrow_down = pygame.image.load("../resources/icon_arrow_down.png")
img_arrow_down = pygame.transform.scale(img_arrow_down, (100,100))

img_close = pygame.image.load("../resources/icon_close.png")
img_close = pygame.transform.scale(img_close, (100,100))


class Game():
    def __init__(self, name):
        self.name = name

    def start(self):
        print("empty game: start")

    def render(self, screen):
        print("empty game: render")

    def end(self):
        print("empty game: end")


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

        self.game_screen.fill( (0,0,0) )
        self.menu_screen.fill( (0,0,0) )

        # Game Control
        self.state = "Boot"
        self.selector_id = 31
        self.games = []
        self.current_game = -1
        self.current_menu_offset = 1
        self.open_for_commands = True


    def addGame( self, game ):
        self.games.append(game)



    def run( self ):
        global font_1
        global img_arrow_up
        global img_arrow_down
        global img_close

        while sharedVars.DONE:
            time.sleep( self.run_timer )
            print(sharedVars.BOARD_STATE)

            #---- Graphics Loop -------------------------------------------------------------
            self.game_screen.fill( (0,0,0) )
            self.menu_screen.fill( (0,0,0) )

            # pass the screen render to the game
            #  also pass the state of the system
            if self.state == "Game":
                self.menu_screen.fill( (0,0,0) )

            # start the sytem by opening the menu.
            elif self.state == "Boot":

                # check if 31 is placed on the column
                if self.selector_id not in sharedVars.BOARD_STATE:
                    self.open_for_commands = True
                    print_grph("OPEN FOR COMMANDS")


                if self.open_for_commands == True:
                    self.game_screen.fill( (0,0,0) )
                    text = font_1.render( "Put Selector on Board to open Menu", False, (255,255,255))
                    self.game_screen.blit(text, (100,100))
                    if self.selector_id in sharedVars.BOARD_STATE:
                        self.state = "Menu"

            else:
                self.menu_screen.fill( (66,188,168) )
                item_height = self.menu_h / 5
                # render menu items
                # the menu will contain 5 items
                #  ^
                #  G
                #  G
                #  V
                #  X
                self.menu_screen.blit(img_arrow_up, ( (self.menu_w / 2) - (img_arrow_up.get_size()[0]/2),
                                                      (item_height*0) + (item_height/2) - (img_arrow_up.get_size()[1]/2) )
                )

                self.menu_screen.blit(img_arrow_down, ( (self.menu_w / 2) - (img_arrow_down.get_size()[0]/2),
                                                        (item_height*3) + (item_height/2) - (img_arrow_down.get_size()[1]/2) )
                )

                self.menu_screen.blit(img_close, ( (self.menu_w / 2) - (img_close.get_size()[0]/2),
                                                   (item_height*4) + (item_height/2) - (img_close.get_size()[1]/2) )
                )

                if( self.current_menu_offset >= 0 and self.current_menu_offset < len(self.games) ):
                    text_game1 = font_1.render( self.games[self.current_menu_offset].name, False, (255,255,255) )
                    self.menu_screen.blit( text_game1, ((self.menu_w / 2) - text_game1.get_width()/2,
                                                        (item_height*1) + (item_height/2)))

                if( self.current_menu_offset >= 0 and self.current_menu_offset + 1 < len(self.games) ):
                    text_game2 = font_1.render( self.games[self.current_menu_offset+1].name, False, (255,255,255) )
                    self.menu_screen.blit( text_game2, ((self.menu_w / 2) - text_game2.get_width()/2,
                                                        (item_height*2) + (item_height/2)))

                # check if 31 is placed on the column
                if self.selector_id not in sharedVars.BOARD_STATE:
                    self.open_for_commands = True
                    print_grph("OPEN FOR COMMANDS")

                right_col = [row[len(row)-1] for row in sharedVars.BOARD_STATE]
                if( self.open_for_commands ):
                    # top 2 rows... up arrow
                    if( right_col[0] == self.selector_id or right_col[1] == self.selector_id ):
                        if( self.current_menu_offset > 0 ):
                            self.current_menu_offset -= 1
                        self.open_for_commands = False

                    # 6th rows... down arrow
                    if( right_col[6] == self.selector_id ):
                        if( self.current_menu_offset < len(self.games)-1 ):
                            self.current_menu_offset += 1
                        self.open_for_commands = False

                    # 7th rows... down arrow
                    if( right_col[7] == self.selector_id ):
                        self.state = "Boot"
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
