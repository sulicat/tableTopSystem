import sys
sys.path.append("../../")
import Graphics
import pygame
import numpy as np
import misc
import pprint

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
        self.kill_positions = {}
        self.must_remove = []
        self.kings = []
        self.last_picked_up = []
        self.last_picked_up_v = 0


    def start(self):
        print("start Checkers")

    #check if movement is within 2d array
    def adjacent(self, a):
        if (0 <= a[0] <= 7) and (0 <= a[1] <= 7):
            return 1
        else:
            return 0

                                                                                                    
    #checking adjacent tiles for movement
    def move(self, current_state, value, move, location, prev_kills = [], visited = []):
        #will return single value (0, 1, 2) meaning (green, red, yellow) for squares
        #will return array (moves) with possible movement options
        #final_move is subset of moves with a different color showing no more jumps
        temp_move = [move[0], move[1]]
        kill_pos = {}

        add_to_v = True
        for v in visited:
            if( v[0] == location[0][0] and v[1] == location[0][1] ):
                add_to_v = False
        if add_to_v:
            visited.append( [location[0][0],location[0][1]]  )

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
                prev_kills.append( temp_move )

            kill_pos[ move[0], move[1] ] = prev_kills

            origins, last_jump, moves, final_moves = [], [], [], []


            if( move[0] < 8 and move[1] < 8 and current_state [move[0]] [move[1]] == 0 ):
                #print( "loc: " + str(location[0][0]) + "," + str(location[0][1]) + " => " + str(move[0]) + "," + str(move[1]) );
                if( value == self.white ):
                    offs = 1
                else:
                    offs = -1


                move1 = [move[0] + offs, move[1] - 1]
                move2 = [move[0] + offs, move[1] + 1]
                move3 = [move[0] - offs, move[1] - 1]
                move4 = [move[0] - offs, move[1] + 1]

                move1_2 = [move[0] + 2*offs, move[1] - 2]
                move2_2 = [move[0] + 2*offs, move[1] + 2]
                move3_2 = [move[0] - 2*offs, move[1] - 2]
                move4_2 = [move[0] - 2*offs, move[1] + 2]

                move1, move2, move3, move4  = np.asarray(move1), np.asarray(move2), np.asarray(move3), np.asarray(move4)
                m1, m2, m3, m4 = self.adjacent(move1), self.adjacent(move2), self.adjacent(move3), self.adjacent(move4)


                print( "move" )
                print( move1_2 )
                print( move2_2 )
                print( move3_2 )
                print( move4_2 )
                print( "location" )
                print( location )
                print( "visited" )
                print( visited )

                use_m = [True, True, True, True]
                for v in visited:
                    if( v[0] == move1_2[0] and v[1] == move1_2[1] ):
                        use_m[0] = False
                    if( v[0] == move2_2[0] and v[1] == move2_2[1] ):
                        use_m[1] = False
                    if( v[0] == move3_2[0] and v[1] == move3_2[1] ):
                        use_m[2] = False
                    if( v[0] == move4_2[0] and v[1] == move4_2[1] ):
                        use_m[3] = False



                if m1 == 1 and use_m[0]:
                    status, new_moves, new_final_moves, new_kill_pos = self.move( current_state, value, move1, [move], prev_kills.copy(), visited.copy() )
                    if( status == 2 ):
                        for m in new_moves:
                            moves.append(m)

                    for key, v in new_kill_pos.items():
                        kill_pos[ key ] = v

                if m2 == 1 and use_m[1]:
                    status, new_moves, new_final_moves, new_kill_pos = self.move( current_state, value, move2, [move], prev_kills.copy(), visited.copy() )
                    if( status == 2 ):
                        for m in new_moves:
                            moves.append(m)

                    for key, value in new_kill_pos.items():
                        kill_pos[ key ] = value

                if m3 == 1 and use_m[2]:
                    status, new_moves, new_final_moves, new_kill_pos = self.move( current_state, value, move3, [move], prev_kills.copy(), visited.copy() )
                    if( status == 2 ):
                        for m in new_moves:
                            moves.append(m)

                    for key, value in new_kill_pos.items():
                        kill_pos[ key ] = value

                if m4 == 1 and use_m[3]:
                    status, new_moves, new_final_moves, new_kill_pos = self.move( current_state, value, move4, [move], prev_kills.copy(), visited.copy() )
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


        for index, item in enumerate(self.kings):
            r = 7-item[1]
            c = item[0]
            pygame.draw.rect(screen, (255,255,0), (r*cw, c*ch, cw/4, ch/4))
            pygame.draw.rect(screen, (255,255,0), ((r+1)*cw - (cw/4), (c+1)*ch - (cw/4), cw/4, ch/4))

        misc.render_grid_nums( screen )


        # ----------------------------------------------------------------------------------------------------
        # still waiting on setup
        if np.count_nonzero(board) == self.total_peices and self.care == 0:
            self.care = 1
            self.current_state = board

        # ----------------------------------------------------------------------------------------------------
        # peices need to be killed
        elif np.count_nonzero(board) > self.total_peices:

            self.care = 0

            menu.fill( ( 150,150,255 ) )

            text = self.font_big.render( "Remove Peices", False, (0,0,0) )
            text = pygame.transform.rotate(text, 270);
            menu.blit( text, ( 10, 10 ) )

            text = self.font_big.render( "Kill", False, (0,0,0) )
            text = pygame.transform.rotate(text, 270);
            menu.blit( text, ( 80, 10 ) )

            text = self.font_big.render( "#: " + str(np.count_nonzero(board) - self.total_peices), False, (255,0,0) )
            menu.blit( text, ( 10, 550 ) )

            for i in range( len(self.must_remove) ):
                text = self.font_big.render( "(" + str(self.must_remove[i][0]) + "," + str(self.must_remove[i][1]) + ")", False, (255,150,0) )
                menu.blit( text, ( 10, 750 + i*100 ) )


            temp_location = np.asarray( np.where( (self.current_state == board) == False) ).T.tolist()
            if( len(temp_location) > 0 ):
                for i, r in enumerate( self.must_remove ):
                    if( temp_location[0][0] == r[0] and temp_location[0][1] == r[1] ):
                        del self.must_remove[i]
                        self.current_state = board

            return

        # ----------------------------------------------------------------------------------------------------
        # peice has been moved
        elif np.count_nonzero(board) == self.total_peices and self.care == 1:
            if self.inc_turn == True:
                # placing a peice down in a different spot
                temp_location = np.asarray( np.where( (self.current_state == board) == False) ).T.tolist()
                if( len(temp_location) > 0 ):

                    if( len(self.last_picked_up) > 0):
                        for index, elem in enumerate(temp_location):
                            if(elem[0] == self.last_picked_up[0] and elem[1] == self.last_picked_up[1]):
                                del temp_location[index]

                    # adding a white king
                    if( self.last_picked_up_v == self.white and temp_location[0][0] == 7):
                        self.kings.append( temp_location[0] )

                    # adding a black king
                    elif( self.last_picked_up_v == self.black and temp_location[0][0] == 0):
                        self.kings.append( temp_location[0] )

                    # if the peice moved and it was a king, change the king index
                    for index, item in enumerate(self.kings):
                        if( self.last_picked_up[0] == item[0] and self.last_picked_up[1] == item[1] ):
                            self.kings[index] = temp_location[0]
                            break

                    self.turn = self.turn + 1
                    self.inc_turn = False

                    for k,v in self.kill_positions.items():
                        for l in temp_location:
                            if( l[0] == k[0] and l[1] == k[1] ):
                                self.must_remove = v.copy()
                                self.total_peices -= len(self.must_remove)
                                break

                    self.current_state = board

            else:
                if (board-self.current_state).any():
                    menu.fill( (255,0,0) )
                    text = self.font_big.render( "Illegal Move!! Revert!!", False, (0,0,0) )
                    text = pygame.transform.rotate(text, 270);
                    menu.blit( text, ( 80, 10 ) )


            if( self.turn%2 == 0 ):
                text = self.font_big.render( "Blues Turn ", False, (255,255,255) )
                text = pygame.transform.rotate(text, 270);
                menu.blit( text, ( 10, 10 ) )
            else:
                text = self.font_big.render( "Reds Turn ", False, (255,255,255) )
                text = pygame.transform.rotate(text, 270);
                menu.blit( text, ( 10, 10 ) )


            # remove dead kings
            for index, item in enumerate(self.kings):
                if board[item[0]][item[1]] == 0:
                    del self.kings[index]
                    break





        # ----------------------------------------------------------------------------------------------------
        # peices need to be added
        elif np.count_nonzero(board) <= self.total_peices - 2 or self.care == 0:
            self.care = 0
            text = self.font_big.render( "Setup - " + str( self.total_peices - np.count_nonzero(board) ) + " More", False, (255,0,0) )
            text = pygame.transform.rotate(text, 270);
            menu.blit( text, ( 10, 10 ) )

        # ----------------------------------------------------------------------------------------------------
        # peice has been picked up
        else:
            if self.care == 1:
                location = np.asarray( np.where( (self.current_state == board) == False) ).T.tolist()

                if len(location) > 0:
                    #picked up peice -> dick hard
                    single_value = self.current_state[ location[0][0] ][ location[0][1] ]
                    if (single_value == self.white and self.turn%2 == 1) or (single_value == self.black and self.turn%2 == 0):
                        self.inc_turn = False
                        menu.fill( (255,0,0) )
                        text = self.font_big.render( "Not Your Turn !!", False, (0,0,0) )
                        text = pygame.transform.rotate(text, 270)
                        menu.blit( text, ( 80, 10 ) )

                    else:
                        self.inc_turn = True


                    if( self.turn%2 == 0 ):
                        text = self.font_big.render( "Blues Turn ", False, (255,255,255) )
                        text = pygame.transform.rotate(text, 270);
                        menu.blit( text, ( 10, 10 ) )
                    else:
                        text = self.font_big.render( "Reds Turn ", False, (255,255,255) )
                        text = pygame.transform.rotate(text, 270);
                        menu.blit( text, ( 10, 10 ) )


                    #pygame.draw.rect(screen, (255,215,0), ((7-location[0][1])*cw, location[0][0]*ch, cw, ch))

                    self.last_picked_up = location[0].copy()
                    self.last_picked_up_v = single_value.copy()
                    if( single_value == self.white ):
                        offs = 1
                    else:
                        offs = -1


                    move1 = [location[0][0] + offs, location[0][1] - 1]
                    move2 = [location[0][0] + offs, location[0][1] + 1]
                    move3 = [location[0][0] - offs, location[0][1] - 1]
                    move4 = [location[0][0] - offs, location[0][1] + 1]
                    move1, move2, move3, move4 = np.asarray(move1), np.asarray(move2), np.asarray(move3), np.asarray(move4)
                    m1, m2, m3, m4 = self.adjacent(move1), self.adjacent(move2), self.adjacent(move3), self.adjacent(move4)

                    kpos_1 = {}
                    kpos_2 = {}
                    kpos_3 = {}
                    kpos_4 = {}

                    is_king = False
                    for k in self.kings:
                        if( location[0][0] == k[0] and location[0][1] == k[1] ):
                            is_king = True


                    #we now draw the squares for movement options if it is possible
                    if m1 == 1:
                       # pygame.draw.rect(screen, (0,255,0), ((7-move1[1])*cw, move1[0]*ch, cw, ch))
                        x, moves, final_moves, kpos_1 = self.move(self.current_state, single_value, move1, location, [])
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

                    if m2 == 1:
                       # pygame.draw.rect(screen, (0,255,0), ((7-move2[1])*cw, move2[0]*ch, cw, ch))
                        x, moves, final_moves, kpos_2 = self.move(self.current_state, single_value, move2, location, [])

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

                    if is_king:
                        if m3 == 1:
                            # pygame.draw.rect(screen, (0,255,0), ((7-move2[1])*cw, move2[0]*ch, cw, ch))
                            x, moves, final_moves, kpos_3 = self.move(self.current_state, single_value, move3, location, [])

                            if x == 0:
                                r = 7-final_moves[1]
                                c = final_moves[0]
                                pygame.draw.rect(screen, (0,255,0), (r*cw, c*ch, cw/4, ch/4))
                                pygame.draw.rect(screen, (0,255,0), ((r+1)*cw - (cw/4), (c+1)*ch - (cw/4), cw/4, ch/4))

                            elif x==2:
                                for mov in moves:
                                    r = 7-mov[1]
                                    c = mov[0]
                                    misc.render_imageInCell( screen, self.purple_star_img, (r, c) )

                        if m4 == 1:
                            # pygame.draw.rect(screen, (0,255,0), ((7-move2[1])*cw, move2[0]*ch, cw, ch))
                            x, moves, final_moves, kpos_4 = self.move(self.current_state, single_value, move4, location, [])

                            if x == 0:
                                r = 7-final_moves[1]
                                c = final_moves[0]
                                pygame.draw.rect(screen, (0,255,0), (r*cw, c*ch, cw/4, ch/4))
                                pygame.draw.rect(screen, (0,255,0), ((r+1)*cw - (cw/4), (c+1)*ch - (cw/4), cw/4, ch/4))

                            elif x==2:
                                for mov in moves:
                                    r = 7-mov[1]
                                    c = mov[0]
                                    misc.render_imageInCell( screen, self.purple_star_img, (r, c) )




                    kpos = {}
                    for k,v in kpos_1.items():
                        kpos[k] = v
                    for k,v in kpos_2.items():
                        kpos[k] = v
                    for k,v in kpos_3.items():
                        kpos[k] = v
                    for k,v in kpos_4.items():
                        kpos[k] = v

                    self.kill_positions = kpos.copy()


    def end(self):
        print("end test")
