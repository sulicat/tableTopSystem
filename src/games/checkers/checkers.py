import sys
sys.path.append("../../")
import Graphics

class Checkers( Graphics.Game ):
    def __init__(self, name):
        super().__init__(name)

    def start(self):
        print("start Checkers")

    def render(self, screen, board):
        screen.fill( (0,255,255) )

    def end(self):
        print("end test")
