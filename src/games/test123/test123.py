import sys
sys.path.append("../../")
import Graphics

class test123( Graphics.Game ):
    def __init__(self, name):
        super().__init__(name)
        print("--------------------------------------------------------------------------------")
        print("testtestttest")
        print("--------------------------------------------------------------------------------")

    def start(self):
        print("start test")

    def render(self, screen, board):
        screen.fill( (255,0,255) )

    def end(self):
        print("end test")
