import sys
sys.path.append("../../")
import Graphics
import chess
import pygame
import numpy as np
import misc

class Chess( Graphics.Game ):
    def __init__(self, name):
        super().__init__(name)

        self.font_big = pygame.font.SysFont('Comic Sans MS', 100)
        self.font_small = pygame.font.SysFont('Comic Sans MS', 35)


        self.state_indicator = [ ["R", "B", "KN", "Q", "K", "KN", "B", "R"],
                                 ["P", "P", "P",  "P", "P", "P",  "P", "P"],
                                 ["P", "P", "P",  "P", "P", "P",  "P", "P"],
                                 ["R", "B", "KN", "K", "Q", "KN", "B", "R"] ]

        #self.start_state_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
        self.start_state_fen = "4r3/8/8/8/8/8/8/1B2R3" # no pawns

        self.old_board = []
        self.kill_pos = []
        self.move_pos = []

        self.kill_img = pygame.image.load("../resources/kill.png")
        self.kill_img = pygame.transform.scale(self.kill_img, (100,100))

        self.thinking_img = pygame.image.load("../resources/kill.png")
        self.thinking_img = pygame.transform.scale(self.kill_img, (100,100))

        self.id2peice = {
            12 :chess.Piece(chess.PAWN, True),
            26 :chess.Piece(chess.ROOK, True),
            25 :chess.Piece(chess.BISHOP, True),
            11 :chess.Piece(chess.KNIGHT, True),
            10 :chess.Piece(chess.KING, True),
            9  :chess.Piece(chess.QUEEN, True),

            24 :chess.Piece(chess.PAWN, False),
            22 :chess.Piece(chess.ROOK, False),
            28 :chess.Piece(chess.BISHOP, False),
            5  :chess.Piece(chess.KNIGHT, False),
            14 :chess.Piece(chess.KING, False),
            7  :chess.Piece(chess.QUEEN, False),

            31:None
        }

        self.chess_board = chess.Board()

        self.state = "settingUp"
        self.turn = 0
        self.total_pieces = 10
        self.picked_up = False
        self.kill_mode = False
        self.picked_up_kill = []
        self.change = []
        self.change_piece = -1

        self.pick_up_pos = []
        self.place_down_pos = []

        self.purple_star_img = pygame.image.load("../resources/star_purple.png")
        self.purple_star_img = pygame.transform.scale(self.purple_star_img, (100,100))


    # clear the chess board and make it replicate the board passed down by the image recognition
    def setChessBoard( self, board ):
        self.chess_board.set_fen("8/8/8/8/8/8/8/8")
        for r, row in enumerate(board):
            for c, item in enumerate(board[r]):
                if( item in self.id2peice.keys() ):
                    self.chess_board.set_piece_at( chess.square( 7-c, 7-r ), self.id2peice[item] )



    def squareToRC( self, sq ):
        row =7 - int(sq/8)
        col = sq % 8
        return row,col
        print( row )
        print( col )
        print( "----------------------------------------------------------------------------------------------------" )

    def RCtoSquare( self, r, c ):
        return (7-r)*8 + c

    def start(self):
        print("start Chess")

    def render(self, screen, menu, board ):
        cw, ch = (screen.get_width())/8, (screen.get_height())/8
        # render the grid
        for r in range(8):
            for c in range(8):
                if(r % 2) == (c % 2):
                    pygame.draw.rect(screen, (180,102,0), (r*cw, c*ch, cw, ch))



        # we are waiting on the user to add all the correct peices to the board
        if( self.state == "settingUp" ):
            self.setChessBoard( board.copy() )
            text = self.font_big.render( "Add More Pieces", False, (255,255,255) )
            text = pygame.transform.rotate(text, 270);
            menu.blit( text, ( 80, 10 ) )
            text = self.font_big.render( str(self.total_pieces-np.count_nonzero(board)) + " to go", False, (255,0,0) )
            text = pygame.transform.rotate(text, 270);
            menu.blit( text, ( 10, 100 ) )

            for c in range( 8 ):
                text = self.font_small.render( str(self.state_indicator[0][c]),False, (255,255,255) )
                screen.blit( text, ( cw*c, ch*0 ) )
                text = self.font_small.render( str(self.state_indicator[1][c]),False, (255,255,255) )
                screen.blit( text, ( cw*c, ch*1 ) )
                text = self.font_small.render( str(self.state_indicator[2][c]),False, (255,255,255) )
                screen.blit( text, ( cw*c, ch*6 ) )
                text = self.font_small.render( str(self.state_indicator[3][c]),False, (255,255,255) )
                screen.blit( text, ( cw*c, ch*7 ) )



            if( self.chess_board.fen().split(" ")[0] == self.start_state_fen or np.count_nonzero(board) == self.total_pieces):
                self.state = "playing"
                self.old_board = board.copy()
                self.setChessBoard( board.copy() )



        elif self.state == "AIturn":
            


        # board has been setup
        else:
            # wait till there is a change between old board state and current borad state
            changes = np.asarray( np.where( (self.old_board == board) == False) ).T.tolist()

            # 2 pieces removed ... could be kill or need setup
            if( (np.count_nonzero(board) <= self.total_pieces - 3) ):
                self.state = "settingUp"

            elif( (np.count_nonzero(board) <= self.total_pieces - 2) ):
                self.kill_mode = True

                menu.fill((255,0,0))
                text = self.font_big.render( "Kill !", False, (255,255,255) )
                text = pygame.transform.rotate(text, 270);
                menu.blit( text, ( 20, 10 ) )

                menu.blit( self.kill_img, ( 20, 300 ) )
                menu.blit( self.kill_img, ( 20, 450 ) )
                menu.blit( self.kill_img, ( 20, 600 ) )




            elif( np.count_nonzero(board) == self.total_pieces - 1 and self.kill_mode == False):
                self.picked_up = True
                self.kill_pos = []
                self.move_pos = []

                if( len(changes) > 0 ):
                    self.change = changes[0]

                    self.change_piece = self.old_board [self.change[0]] [self.change[1]]
                    change_pos_square = self.RCtoSquare(self.change[0], 7-self.change[1])
                    self.pick_up_pos = [ self.change[0], self.change[1] ]

                    menu.fill( (0,0,0) )
                    if( self.turn % 2 == 0 ):
                        menu.fill( (0,100,255) )
                        text = self.font_big.render( "Blue Players Turn", False, (255,255,255) )
                    else:
                        menu.fill( (255,100,0) )
                        text = self.font_big.render( "Red Players Turn", False, (255,255,255) )
                    text = pygame.transform.rotate(text, 270);
                    menu.blit( text, ( 10, 10 ) )



                    # if we picked up the correct color
                    picked_color = self.id2peice[self.change_piece].color
                    if (self.turn % 2 == 0 and picked_color == False) or (self.turn % 2 == 1 and picked_color == True):
                        if( self.turn % 2 == 0 ):
                            self.chess_board.turn = False
                        else:
                            self.chess_board.turn = True

                        possible_moves = self.chess_board.legal_moves

                        for m in possible_moves:
                            if( m.from_square == change_pos_square ):
                                _r, _c = self.squareToRC(m.to_square)
                                r = _c
                                c = _r
                                if( self.old_board[_r][7-_c] == 0 ):
                                    pygame.draw.rect(screen, (0,255,0), (r*cw, c*ch, cw/4, ch/4))
                                    pygame.draw.rect(screen, (0,255,0), ((r+1)*cw - (cw/4), (c+1)*ch - (cw/4), cw/4, ch/4))
                                    self.move_pos.append( [_r,7-c] )
                                else:
                                    misc.render_imageInCell( screen, self.purple_star_img, (r, c) )
                                    self.kill_pos.append( [_r,7-c] )

                    else:
                        text = self.font_big.render( "NOT YOUR TURN!!!", False, (255,0,0) )
                        text = pygame.transform.rotate(text, 270);
                        menu.blit( text, ( 80, 10 ) )



            # piece placed down
            elif( self.picked_up == True ):
                self.kill_mode = False
                self.picked_up = False


                if( np.count_nonzero(board) == self.total_pieces - 1 ):
                    print("There should have been a kill <<----------")
                    self.total_pieces -= 1

                if( len(changes) > 0 ):
                    self.turn += 1
                    self.old_board = board.copy()
                    self.setChessBoard( board.copy() )

                    if( self.turn % 2 == 1 ):
                        self.state = "AIturn"

                print( self.turn )
                print( "kill: ", end="")
                print( self.kill_pos )
                print( "move: ", end="")
                print( self.move_pos )


            else:
                menu.fill( (0,0,0) )
                if( self.turn % 2 == 0 ):
                    menu.fill( (0,100,255) )
                    text = self.font_big.render( "Blue Players Turn", False, (255,255,255) )
                else:
                    menu.fill( (255,100,0) )
                    text = self.font_big.render( "Red Players Turn", False, (255,255,255) )

                text = pygame.transform.rotate(text, 270);
                menu.blit( text, ( 10, 10 ) )






    def end(self):
        print("end chess")
