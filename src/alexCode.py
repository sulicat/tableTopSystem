import sys

sys.path.append("../../")
import Graphics
import pygame
import numpy as np
import misc


class Checkers(Graphics.Game):
    def __init__(self, name):
        super().__init__(name)
        self.care = 0
        self.current_state = []
        self.white = 12
        self.black = 24
        self.total_pieces = 24
        self.turn = 0
        self.xmoves, self.xfinal_moves, self.ymoves, self.yfinal_moves = [], [], [], []
        self.wmoves, self.wfinal_moves, self.zmoves, self.zfinal_moves = [], [], [], []
        #picked_up == 0 means anticipating piece being picked up
        #picked_up == 1 means anticipating piece being placing down
        self.picked_up = 0
        self.kings = []

    def start(self):
        print("start Checkers")

    # check if movement is within 2d array
    def adjacent(self, a):
        if (0 <= a[0] <= 7) and (0 <= a[1] <= 7):
            return 1
        else:
            return 0

    # checking adjacent tiles for movement
    def move(self, current_state, value, move, location):
        # will return single value (0, 1, 2) meaning (green, red, yellow) for squares
        # will return array (moves) with possible movement options
        # final_move is subset of moves with a different color showing no more jumps

        # case where piece on same piece is in adjacent square
        if current_state[move[0], move[1]] == value:
            moves = [move[0], move[1]]
            final_moves = [move[0], move[1]]
            return 1, moves, final_moves

        elif current_state[move[0], move[1]] == 0:
            moves = [move[0], move[1]]
            final_moves = [move[0], move[1]]
            return 0, moves, final_moves

        else:
            move[0] = ((move[0] - location[0][0]) * 2) + location[0][0]
            move[1] = ((move[1] - location[0][1]) * 2) + location[0][1]

            moves, final_moves = [], []

            if current_state[move[0]][move[1]] == 0:
                if (value == self.white):
                    offs = 1
                else:
                    offs = -1

                move1 = [move[0] + offs, move[1] - 1]
                move2 = [move[0] + offs, move[1] + 1]
                move3 = [move[0] - offs, move[1] - 1]
                move4 = [move[0] - offs, move[1] + 1]
                move1, move2, move3, move4 = np.asarray(move1), np.asarray(move2), np.asarray(move3), np.asarray(move4)
                m1, m2, m3, m4 = self.adjacent(move1), self.adjacent(move2), self.adjacent(move3), self.adjacent(move4)

                if m1 == 1:
                    status, new_moves, new_final_moves = self.move(current_state, value, move1, [move])
                    if (status == 2):
                        for m in new_moves:
                            moves.append(m)
                    else:
                        for f in new_final_moves:
                            final_moves.append(f)

                if m2 == 1:
                    status, new_moves, new_final_moves = self.move(current_state, value, move2, [move])
                    if (status == 2):
                        for m in new_moves:
                            moves.append(m)
                    else:
                        for f in new_final_moves:
                            final_moves.append(f)

                if m3 == 1:
                    status, new_moves, new_final_moves = self.move(current_state, value, move2, [move])
                    if (status == 2):
                        for m in new_moves:
                            moves.append(m)
                    else:
                        for f in new_final_moves:
                            final_moves.append(f)

                if m4 == 1:
                    status, new_moves, new_final_moves = self.move(current_state, value, move2, [move])
                    if (status == 2):
                        for m in new_moves:
                            moves.append(m)
                    else:
                        for f in new_final_moves:
                            final_moves.append(f)

                moves.append(move)

            return 2, moves, final_moves

    def render(self, screen, board):
        screen.fill((0, 0, 0))
        misc.render_grid(screen)

        #cell length and width
        cw, ch = (screen.get_width()) / 8, (screen.get_height()) / 8
        margin = 0

        white_king = [[7, 0], [7, 2], [7, 4], [7, 6]]
        black_king = [[0, 1], [0, 3], [0, 5], [0, 7]]

        for r in range(8):
            for c in range(8):
                if (r % 2) == (c % 2):
                    pygame.draw.rect(screen, (255, 105, 180), (r * cw, c * ch, cw, ch))
                else:
                    pass

        if np.count_nonzero(board) == self.total_pieces:
            self.care = 1
            self.current_state = board

        elif np.count_nonzero(board) <= self.total_pieces - 2 or np.count_nonzero(board) >= self.total_pieces + 2:
            self.care = 0

        else:
            if self.care == 1:
                location = np.asarray(np.where((self.current_state == board) == False)).T.tolist()

                if len(location) > 0:

                    single_value = self.current_state[location[0][0]][location[0][1]]
                    pygame.draw.rect(screen, (255, 215, 0), ((7 - location[0][1]) * cw, location[0][0] * ch, cw, ch))

                    if self.turn % 2 == 0 and single_value == self.white:
                        pass
                    elif self.turn % 2 == 1 and single_value == self.black:
                        pass
                    else:
                        print("Not your turn!")
                        return

                    if single_value == self.white:
                        offs = 1
                    else:
                        offs = -1

                    move1 = [location[0][0] + offs, location[0][1] - 1]
                    move2 = [location[0][0] + offs, location[0][1] + 1]
                    move1, move2 = np.asarray(move1), np.asarray(move2)
                    m1, m2 = self.adjacent(move1), self.adjacent(move2)

                    #next few lines only apply to kings
                    move3 = [location[0][0] - offs, location[0][1] - 1]
                    move4 = [location[0][0] - offs, location[0][1] + 1]
                    move3, move4 = np.asarray(move3), np.asarray(move4)
                    m3, m4 = self.adjacent(move3), self.adjacent(move4)

                    if self.picked_up == 0:
                        #we now draw the squares for movement options if it is possible
                        if m1 == 1:
                            x, self.xmoves, self.xfinal_moves = \
                                self.move(self.current_state, single_value, move1, location)
                            if x == 0:
                                pygame.draw.rect(screen, (50, 120, 0),
                                                 ((7 - self.xfinal_moves[1]) * cw, self.xfinal_moves[0] * ch, cw, ch))
                            elif x == 1:  # x == 1
                                pygame.draw.rect(screen, (255, 0, 0),
                                                 ((7 - self.xfinal_moves[1]) * cw, selx.ffinal_moves[0] * ch, cw, ch))

                            else:
                                #adjacent cell is enemy unit and chosen unit may jump
                                for mov in self.xmoves:
                                    pygame.draw.rect(screen, (50, 120, 0), ((7 - mov[1]) * cw, mov[0] * ch, cw, ch))

                                for fmov in self.xfinal_moves:
                                    pygame.draw.rect(screen, (0, 180, 0), ((7 - fmov[1]) * cw, fmov[0] * ch, cw, ch))

                        if m2 == 1:
                            y, self.ymoves, self.yfinal_moves = self.move(self.current_state, single_value, move2, location)

                            if y == 0:
                                pygame.draw.rect(screen, (50, 120, 0),
                                    ((7 - self.yfinal_moves[1]) * cw, self.yfinal_moves[0] * ch, cw, ch))

                            elif y == 1:
                                pygame.draw.rect(screen, (255, 0, 0),
                                    ((7 - self.yfinal_moves[1]) * cw, self.yfinal_moves[0] * ch, cw, ch))

                            else:
                                for mov in self.ymoves:
                                    pygame.draw.rect(screen, (50, 120, 0), ((7 - mov[1]) * cw, mov[0] * ch, cw, ch))

                                for fmov in self.yfinal_moves:
                                    pygame.draw.rect(screen, (0, 255, 0), ((7 - fmov[1]) * cw, fmov[0] * ch, cw, ch))

                        if location in kings:
                            if m3 == 1:
                                w, self.wmoves, self.wfinal_moves = self.move(self.current_state, single_value,
                                                                                  move3, location)

                                if w == 0:
                                    pygame.draw.rect(screen, (50, 120, 0),
                                                        (
                                                        (7 - self.wfinal_moves[1]) * cw, self.wfinal_moves[0] * ch, cw,
                                                        ch))

                                elif w == 1:
                                    pygame.draw.rect(screen, (255, 0, 0),
                                                        (
                                                        (7 - self.wfinal_moves[1]) * cw, self.wfinal_moves[0] * ch, cw,
                                                        ch))

                                else:
                                    for mov in self.wmoves:
                                        pygame.draw.rect(screen, (50, 120, 0),
                                                        ((7 - mov[1]) * cw, mov[0] * ch, cw, ch))

                                    for fmov in self.wfinal_moves:
                                        pygame.draw.rect(screen, (0, 255, 0),
                                                        ((7 - fmov[1]) * cw, fmov[0] * ch, cw, ch))

                            if m4 == 1:
                                z, self.zmoves, self.zfinal_moves = self.move(self.current_state, single_value,
                                                                                  move4, location)

                                if z == 0:
                                    pygame.draw.rect(screen, (50, 120, 0),
                                                        ((7 - self.zfinal_moves[1]) * cw, self.zfinal_moves[0] * ch, cw,
                                                        ch))
                                elif z == 1:
                                    pygame.draw.rect(screen, (255, 0, 0),
                                                        ((7 - self.zfinal_moves[1]) * cw, self.zfinal_moves[0] * ch, cw,
                                                        ch))
                                else:
                                    for mov in self.zmoves:
                                        pygame.draw.rect(screen, (50, 120, 0),
                                                        ((7 - mov[1]) * cw, mov[0] * ch, cw, ch))

                                    for fmov in self.zfinal_moves:
                                        pygame.draw.rect(screen, (0, 255, 0),
                                                        ((7 - fmov[1]) * cw, fmov[0] * ch, cw, ch))

                        self.picked_up = self.picked_up + 1

                    else:
                        #remove duplicates in moves found in final_moves
                        for i in xmoves:
                            for j in xfinal_moves:
                                if i == j:
                                    del[i]
                        for i in ymoves:
                            for j in yfinal_moves:
                                if i == j:
                                    del[i]

                        #check if legal move
                        if location in kings:
                            if location in (self.xfinal_moves or self.yfinal_moves or self.wfinal_moves or self.zfinal_moves):
                                #function to find pieces removed from move
                                self.total_pieces = self.total_pieces - remove

                        elif location in self.xfinal_moves or location in self.yfinal_moves:
                            #function to find pieces removed from move
                            self.total_pieces = self.total_pieces - remove

                        else:
                            print("Not a valid move!")
                            return

                        for w in white_king:
                            if location == white_king and single_value == self.white:
                                kings.append(location)

                        for b in black_king:
                            if location == black_king and single_value == self.black:
                                kings.append(location)

                        #remove duplicates later

                        self.picked_up = self.picked_up - 1

                self.turn = self.turn + 0.5

    def end(self):
        print("end test")
