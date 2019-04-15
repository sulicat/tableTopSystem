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
    def move(self, current_state, value, move, location):
        #will return single value (0, 1, 2) meaning (green, red, yellow) for squares
        #will return array (moves) with possible movement options
        #final_move is subset of moves with a different color showing no more jumps

        #case where piece on same piece is in adjacent square
        if current_state[move[0], move[1]] == value:
            moves = [move[0], move[1]]
            final_moves = [move[0], move[1]]
            return 1, moves, final_moves

        elif current_state[move[0], move[1]] == 0:
            moves = [move[0], move[1]]
            final_moves = [move[0], move[1]]
            return 0, moves, final_moves

        else:
            move[0] = ( (move[0] - location[0][0]) * 2) + location[0][0]
            move[1] = ( (move[1] - location[0][1]) * 2) + location[0][1]


            origins, last_jump, moves, final_moves = [], [], [], []

            if( current_state [move[0]] [move[1]] == 0 ):
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
                    status, new_moves, new_final_moves = self.move( current_state, value, move1, [move] )
                    if( status == 2 ):
                        for m in new_moves:
                            moves.append(m)
                if m2 == 1:
                    status, new_moves, new_final_moves = self.move( current_state, value, move2, [move] )
                    if( status == 2 ):
                        for m in new_moves:
                            moves.append(m)



                origins.append(move)
                last_jump.append(location)

                #x, y, moves, final_moves, z = tile_check(origins, last_jump, moves, final_move, value)
                moves.append(move)

                #for loop to remove elements in final_moves that are also in moves
                for mov in moves:
                    for fmov in final_moves:
                        if mov == fmov:
                            del mov

            return 2, moves, final_moves

                                                                                                    

    #asd
    def render(self, screen, board):
        screen.fill( (0, 0, 0) )
        misc.render_grid(screen)

        #cell length and width
        cw, ch = (screen.get_width())/8, (screen.get_height())/8
        margin = 0

        for r in range(8):
            for c in range(8):
                if(r % 2) == (c % 2):
                    pygame.draw.rect(screen, (255,105,180), (r*cw, c*ch, cw, ch))
                else:
                    pass



        if np.count_nonzero(board) == self.total_peices:
            self.care = 1
            self.current_state = board

        elif np.count_nonzero(board) <= self.total_peices - 2:
            self.care = 0

        else:
            if self.care == 1:
                location = np.asarray( np.where( (self.current_state == board) == False) ).T.tolist()

                if len(location) > 0:

                    single_value = self.current_state[ location[0][0] ][ location[0][1] ]
                    #print("------------------------------")
                    #print(single_value)
                    #print("------------------------------")

                    pygame.draw.rect(screen, (255,215,0), ((7-location[0][1])*cw, location[0][0]*ch, cw, ch))

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
                        x, moves, final_moves = self.move(self.current_state, single_value, move1, location)
                        if x == 0:
                            pygame.draw.rect(screen, (50, 120, 0), ( (7-final_moves[1])*cw, final_moves[0]*ch, cw, ch))
                        elif x == 1: #x == 1
                            pygame.draw.rect(screen, (255,0,0), ( (7-final_moves[1])*cw, final_moves[0]*ch, cw, ch))

                        else:
                        #adjacent cell is enemy unit and chosen unit may jump
                            for mov in moves:
                                #pygame.draw.rect(screen, (178,102,255), ((7-mov[1])*cw, mov[0]*ch, cw, ch))
                                pygame.draw.rect(screen, (50,120,0), ((7-mov[1])*cw, mov[0]*ch, cw, ch))

                            for fmov in final_moves:
                                pygame.draw.rect(screen, (0,180,0), ((7-fmov[1])*cw, fmov[0]*ch, cw, ch))


                    if m2 == 1:
                       # pygame.draw.rect(screen, (0,255,0), ((7-move2[1])*cw, move2[0]*ch, cw, ch))
                        x, moves, final_moves = self.move(self.current_state, single_value, move2, location)

                        if x == 0:
                            pygame.draw.rect(screen, (50, 120, 0), ( (7-final_moves[1])*cw, final_moves[0]*ch, cw, ch))
                        elif x == 1:
                            pygame.draw.rect(screen, (255,0,0), ( (7-final_moves[1])*cw, final_moves[0]*ch, cw, ch))

                        else:
                            for mov in moves:
                                #pygame.draw.rect(screen, (178,102,255), ((7-mov[1])*cw, mov[0]*ch, cw, ch))
                                pygame.draw.rect(screen, (50,120,0), ((7-mov[1])*cw, mov[0]*ch, cw, ch))

                            for fmov in final_moves:
                                pygame.draw.rect(screen, (0,255,0), ((7-fmov[1])*cw, fmov[0]*ch, cw, ch))




    def end(self):
        print("end test")
