import sys
sys.path.append("../../")
import Graphics
import pygame
import numpy as np
import misc

class Checkers( Graphics.Game ):
    def __init__(self, name):
        super().__init__(name)
        self.care = 0
        self.current_state = []
        self.white = 12
        self.black = 24
        self.total_peices = 6

        self.purple_star_img = pygame.image.load("../resources/star_purple.png")
        self.purple_star_img = pygame.transform.scale(self.purple_star_img, (100,100))
        self.font_big = pygame.font.SysFont('Comic Sans MS', 100)


        self.turn = 0
        self.inc_turn = True

    def start(self):
        print("start Checkers")

    #check if movement is within 2d array
    def adjacent(self, a):
        if (0 <= a[0] <= 7) and (0 <= a[1] <= 7):
            return 1
        else:
            return 0

                                                                                                    
    #asd
    #checking adjacent tiles for movement
    def move(self, current_state, value, move, location, prev_kills = []):
        #will return single value (0, 1, 2) meaning (green, red, yellow) for squares
        #will return array (moves) with possible movement options
        #final_move is subset of moves with a different color showing no more jumps
        temp_move = [move[0], move[1]]
        kill_pos = {}

        print( "oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo" )
        current_state[move[0], move[1]]
        print( value )
        print( "oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo" )

        #case where piece on same piece is in adjacent square
        if current_state[move[0], move[1]] == value:
            moves = [move[0], move[1]]
            final_moves = [move[0], move[1]]
            return 1, moves, final_moves, kill_pos

        elif current_state[move[0], move[1]] == 0:
            moves = [move[0], move[1]]
            final_moves = [move[0], move[1]]
            return 0, moves, final_moves, kill_pos

        else:
            move[0] = ( (move[0] - location[0][0]) * 2) + location[0][0]
            move[1] = ( (move[1] - location[0][1]) * 2) + location[0][1]

            add = True
            for i in prev_kills:
                if( i[0] == temp_move[0] and i[1] == temp_move[1] ):
                    add = False

            if add == True:
                prev_kills.append(  temp_move )


            origins, last_jump, moves, final_moves = [], [], [], []
            kill_pos[ move[1], move[0] ] = prev_kills


            if( move[0] < 8 and move[1] < 8 and current_state [move[0]] [move[1]] == 0 ):
                #print( "loc: " + str(location[0][0]) + "," + str(location[0][1]) + " => " + str(move[0]) + "," + str(move[1]) );
                if( value == self.white ):
                    offs = 1
                else:
                    offs = -1


                move1 = [move[0] + offs, move[1] - 1]
                move2 = [move[0] + offs, move[1] + 1]
                move1, move2 = np.asarray(move1), np.asarray(move2)
                m1, m2 = self.adjacent(move1), self.adjacent(move2)
                if m1 == 1:
                    status, new_moves, new_final_moves, new_kill_pos = self.move( current_state, value, move1, [move], prev_kills )
                    if( status == 2 ):
                        for m in new_moves:
                            moves.append(m)

                    for key, value in new_kill_pos.items():
                        kill_pos[ key ] = value


                if m2 == 1:
                    status, new_moves, new_final_moves, new_kill_pos = self.move( current_state, value, move2, [move], prev_kills )
                    if( status == 2 ):
                        for m in new_moves:
                            moves.append(m)

                    for key, value in new_kill_pos.items():
                        kill_pos[ key ] = value

                #x, y, moves, final_moves, z = tile_check(origins, last_jump, moves, final_move, value)
                moves.append(move)

                #for loop to remove elements in final_moves that are also in moves
                for mov in moves:
                    for fmov in final_moves:
                        if mov == fmov:
                            del mov

            return 2, moves, final_moves, kill_pos

                                                                                                    

    #asd
    def render(self, screen, menu, board):
        screen.fill( (0, 0, 0) )
        misc.render_grid(screen)

        #cell length and width
        cw, ch = (screen.get_width())/8, (screen.get_height())/8
        margin = 0

        for r in range(8):
            for c in range(8):
                if(r % 2) == (c % 2):
                    pygame.draw.rect(screen, (180,102,0), (r*cw, c*ch, cw, ch))


                else:
                    pass



        if np.count_nonzero(board) == self.total_peices and self.care == 0:
            self.care = 1
            self.current_state = board


        elif np.count_nonzero(board) == self.total_peices and self.care == 1:
            if self.inc_turn  == True:
                self.turn = self.turn + 1
                self.inc_turn = False
                self.current_state = board


            if( self.turn%2 == 0 ):
                text = self.font_big.render( "Whites Turn ", False, (255,255,255) )
                text = pygame.transform.rotate(text, 270);
                menu.blit( text, ( 10, 10 ) )
            else:
                text = self.font_big.render( "Blacks Turn ", False, (255,255,255) )
                text = pygame.transform.rotate(text, 270);
                menu.blit( text, ( 10, 10 ) )


        elif np.count_nonzero(board) <= self.total_peices - 2:
            self.care = 0
            text = self.font_big.render( "Setup ", False, (255,0,0) )
            text = pygame.transform.rotate(text, 270);
            menu.blit( text, ( 10, 10 ) )

        else:
            if self.care == 1:
                location = np.asarray( np.where( (self.current_state == board) == False) ).T.tolist()

                if len(location) > 0:
                    #picked up peice -> dick hard


                    single_value = self.current_state[ location[0][0] ][ location[0][1] ]
                    if (single_value == self.white and self.turn%2 == 1) or (single_value == self.black and self.turn%2 == 0):
                        self.inc_turn = False
                        text = self.font_big.render( "Not Your Turn !!", False, (255,0,255) )
                        text = pygame.transform.rotate(text, 270);
                        menu.blit( text, ( 10, 10 ) )
                        print("not your turn")

                    else:
                        self.inc_turn = True


                    if( self.turn%2 == 0 ):
                        text = self.font_big.render( "Whites Turn ", False, (255,255,255) )
                        text = pygame.transform.rotate(text, 270);
                        menu.blit( text, ( 10, 10 ) )
                    else:
                        text = self.font_big.render( "Blacks Turn ", False, (255,255,255) )
                        text = pygame.transform.rotate(text, 270);
                        menu.blit( text, ( 10, 10 ) )


                    #pygame.draw.rect(screen, (255,215,0), ((7-location[0][1])*cw, location[0][0]*ch, cw, ch))

                    if( single_value == self.white ):
                        offs = 1
                    else:
                        offs = -1


                    move1 = [location[0][0] + offs, location[0][1] - 1]
                    move2 = [location[0][0] + offs, location[0][1] + 1]
                    move1, move2 = np.asarray(move1), np.asarray(move2)
                    m1, m2 = self.adjacent(move1), self.adjacent(move2)

                    #we now draw the squares for movement options if it is possible
                    if m1 == 1:
                       # pygame.draw.rect(screen, (0,255,0), ((7-move1[1])*cw, move1[0]*ch, cw, ch))
                        x, moves, final_moves, k_pos = self.move(self.current_state, single_value, move1, location)
                        if x == 0:
                            r = 7-final_moves[1]
                            c = final_moves[0]
                            #pygame.draw.rect(screen, (50, 120, 0), ( (7-final_moves[1])*cw, final_moves[0]*ch, cw, ch))
                            pygame.draw.rect(screen, (0,255,0), (r*cw, c*ch, cw/4, ch/4))
                            pygame.draw.rect(screen, (0,255,0), ((r+1)*cw - (cw/4), (c+1)*ch - (cw/4), cw/4, ch/4))


                        elif x==2:
                        #adjacent cell is enemy unit and chosen unit may jump
                            for mov in moves:
                                r = 7-mov[1]
                                c = mov[0]
                                #pygame.draw.rect(screen, (50,120,0), ((7-mov[1])*cw, mov[0]*ch, cw, ch))
                                #pygame.draw.rect(screen, (0,255,0), (r*cw, c*ch, cw/4, ch/4))
                                #pygame.draw.rect(screen, (0,255,0), ((r+1)*cw - (cw/4), (c+1)*ch - (cw/4), cw/4, ch/4))
                                misc.render_imageInCell( screen, self.purple_star_img, (r,c) )

                            '''
                            for fmov in final_moves:
                                #pygame.draw.rect(screen, (0,180,0), ((7-fmov[1])*cw, fmov[0]*ch, cw, ch))
                                misc.render_imageInCell( screen, self.purple_star_img, (7-fmov[1], fmov[0]) )
                            '''

                            #print( "final moves" )
                            #print( final_moves )
                            #print( "moves" )
                            #print( moves )
                            print(k_pos)

                    if m2 == 1:
                       # pygame.draw.rect(screen, (0,255,0), ((7-move2[1])*cw, move2[0]*ch, cw, ch))
                        x, moves, final_moves, k_pos = self.move(self.current_state, single_value, move2, location)

                        if x == 0:
                            r = 7-final_moves[1]
                            c = final_moves[0]
                            #pygame.draw.rect(screen, (50, 120, 0), ( (7-final_moves[1])*cw, final_moves[0]*ch, cw, ch))

                            pygame.draw.rect(screen, (0,255,0), (r*cw, c*ch, cw/4, ch/4))
                            pygame.draw.rect(screen, (0,255,0), ((r+1)*cw - (cw/4), (c+1)*ch - (cw/4), cw/4, ch/4))

                        elif x==2:
                            for mov in moves:
                                r = 7-mov[1]
                                c = mov[0]
                                #pygame.draw.rect(screen, (50,120,0), ((7-mov[1])*cw, mov[0]*ch, cw, ch))
                                #pygame.draw.rect(screen, (0,255,0), (r*cw, c*ch, cw/4, ch/4))
                                #pygame.draw.rect(screen, (0,255,0), ((r+1)*cw - (cw/4), (c+1)*ch - (cw/4), cw/4, ch/4))
                                misc.render_imageInCell( screen, self.purple_star_img, (r, c) )
                            '''
                            for fmov in final_moves:
                                #pygame.draw.rect(screen, (0,255,0), ((7-fmov[1])*cw, fmov[0]*ch, cw, ch))
                                misc.render_imageInCell( screen, self.purple_star_img, (7-fmov[1], fmov[0]) )
                            '''

                            #print( "final moves" )
                            #print( final_moves )
                            #print( "moves" )
                            #print( moves )
                            #print(kill_pos)

                        print( "--------------------------------------------------------------------------------" )



    def end(self):
        print("end test")
