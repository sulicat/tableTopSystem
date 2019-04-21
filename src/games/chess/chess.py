import sys
sys.path.append("../../")
import Graphics

class Chess( Graphics.Game ):
    def __init__(self, name):
        super().__init__(name)

    def start(self):
        print("start Chess")

    def render(self, screen, menu, board):
        print("render chess")

    def end(self):
        print("end chess")
