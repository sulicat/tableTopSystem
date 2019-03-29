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

    def start(self):
        print("start Checkers")

    #check if movement is within 2d array
    def adjacent(self, a):
        if (0 <= a[0] <= 7) and (0 <= a[1] <= 7):
            return 1
        else:
            return 0


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
            pass #for now

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



        if np.count_nonzero(board) == 3:
            self.care = 1
            self.current_state = board

        elif np.count_nonzero(board) <= 1:
            self.care = 0

        else:
            if self.care == 1:
                location = np.asarray( np.where( (self.current_state == board) == False) ).T.tolist()

                if len(location) > 0:

                    single_value = self.current_state[ location[0][0] ][ location[0][1] ]
                    print("------------------------------")
                    print(single_value)
                    print("------------------------------")

                    pygame.draw.rect(screen, (255,215,0), ((7-location[0][1])*cw, location[0][0]*ch, cw, ch))

                    move1 = (location[0][0] + 1, location[0][1] - 1)
                    move2 = (location[0][0] + 1, location[0][1] + 1)
                    move1, move2 = np.asarray(move1), np.asarray(move2)
                    m1, m2 = self.adjacent(move1), self.adjacent(move2)

                    #we now draw the squares for movement options if it is possible
                    if m1 == 1:
                       # pygame.draw.rect(screen, (0,255,0), ((7-move1[1])*cw, move1[0]*ch, cw, ch))
                        x, moves, final_moves = self.move(self.current_state, single_value, move1, location)
                        print(final_moves)
                        print(x)
                        if x == 0:
                            pygame.draw.rect(screen, (0,255,0), ( (7-final_moves[1])*cw, final_moves[0]*ch, cw, ch))
                        else: #x == 1
                            pygame.draw.rect(screen, (255,0,0), ( (7-final_moves[1])*cw, final_moves[0]*ch, cw, ch))

                    else:
                        pass

                    if m2 == 1:
                       # pygame.draw.rect(screen, (0,255,0), ((7-move2[1])*cw, move2[0]*ch, cw, ch))
                        y, moves, final_moves = self.move(self.current_state, single_value, move2, location)
                        print(final_moves)
                        print(y)
                        if y == 0:
                            pygame.draw.rect(screen, (0,255,0), ( (7-final_moves[1])*cw, final_moves[0]*ch, cw, ch))
                        else:
                            pygame.draw.rect(screen, (255,0,0), ( (7-final_moves[1])*cw, final_moves[0]*ch, cw, ch))
                    else:
                        pass

                else:
                    pass
            else:
                pass

            '''
                    move1 = (location[0][0] + 1, location[0][1] - 1)
                    move2 = (location[0][0] + 1, location[0][1] + 1)
                    move1, move2 = np.asarray(move1), np.asarray(move2)
                    m1, m2 = adjacent(move1), adjacent(move2)

                    #we now draw the squares for movement options if it is possible
                    if m1 == 1:
                       x, moves, final_moves = move(current_state, single_value, move1, location)
                       if x = 0:
                           pygame.draw.rect(screen, (0,255,0), (final_moves[0][0]*cw, final_moves[0][1]*ch, cw, ch))
                       else: #x == 1
                           pygame.draw.rect(screen, (255,0,0), (final_moves[0][0]*cw, final_moves[0][1]*ch, cw, ch))
                    else:
                        pass

                    if m2 == 1:
                        y, moves, final_moves = move(current_state, single_value, move2, location)
                      
                        if y = 0:
                            pygame.draw.rect(screen, (0,255,0), (final_moves[0][0]*cw, final_moves[0][1]*ch, cw, ch))
                        else:
                            pygame.draw.rect(screen, (0,255,0), (final_moves[0][0]*cw, final_moves[0][1]*ch, cw, ch))
               
                    else:
                        pass

                else:
                    pass
            '''
    def end(self):
        print("end test")
