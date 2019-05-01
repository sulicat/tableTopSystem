import sys
sys.path.append("../../")
import Graphics
import chess


class Chess( Graphics.Game ):
    def __init__(self, name):
        super().__init__(name)

        self.id2fen = {
            12:"p",
            26:"r",
            25:"b",
            11:"n",
            10:"k",
            9:"q",

            24:"P",
            2:"R",
            3:"B",
            4:"N",
            5:"K",
            6:"Q"
        }

    def board2FEN( self, board ):
        FEN = ""
        for r, row in enumerate(board):
            for c, item in enumerate(board[r]):
                print(item)

        return FEN;


    def start(self):
        print("start Chess")

    def render(self, screen, menu, board):
        FEN = self.board2FEN( board.copy() )
        print( FEN )
        print(board)
        print("----------------------------------------------------------------------------------------------------")

    def end(self):
        print("end chess")
