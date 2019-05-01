import sys
sys.path.append("../../")
import Graphics
import chess
import pygame

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
        self.start_state_fen = "4r3/8/8/8/8/8/8/1B6" # no pawns

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


    # clear the chess board and make it replicate the board passed down by the image recognition
    def setChessBoard( self, board ):
        self.chess_board.set_fen("8/8/8/8/8/8/8/8")
        for r, row in enumerate(board):
            for c, item in enumerate(board[r]):
                if( item in self.id2peice.keys() ):
                    self.chess_board.set_piece_at( chess.square( c, r ), self.id2peice[item] )



    def start(self):
        print("start Chess")

    def render(self, screen, menu, board ):
        cw, ch = (screen.get_width())/8, (screen.get_height())/8
        # render the grid
        for r in range(8):
            for c in range(8):
                if(r % 2) == (c % 2):
                    pygame.draw.rect(screen, (180,102,0), (r*cw, c*ch, cw, ch))


        self.setChessBoard( board.copy() )

        # we are waiting on the user to add all the correct peices to the board
        if( self.state == "settingUp" ):
            text = self.font_big.render( "Setup... Follow Letters", False, (255,0,0) )
            text = pygame.transform.rotate(text, 270);
            menu.blit( text, ( 10, 10 ) )

            for c in range( 8 ):
                text = self.font_small.render( str(self.state_indicator[0][c]),False, (255,255,255) )
                screen.blit( text, ( cw*c, ch*0 ) )
                text = self.font_small.render( str(self.state_indicator[1][c]),False, (255,255,255) )
                screen.blit( text, ( cw*c, ch*1 ) )
                text = self.font_small.render( str(self.state_indicator[2][c]),False, (255,255,255) )
                screen.blit( text, ( cw*c, ch*6 ) )
                text = self.font_small.render( str(self.state_indicator[3][c]),False, (255,255,255) )
                screen.blit( text, ( cw*c, ch*7 ) )

                print( "current: ", end="")
                print( self.chess_board.fen().split(" ")[0] )
                print( "wanted: ", end="")
                print( self.start_state_fen )
                print( "----------------------------------------------------------------------------------------------------" )


            if( self.chess_board.fen().split(" ")[0] == self.start_state_fen ):
                self.state = "playing"

        else:
            text = self.font_big.render( "playing", False, (255,0,0) )
            text = pygame.transform.rotate(text, 270);
            menu.blit( text, ( 10, 10 ) )







    def end(self):
        print("end chess")
