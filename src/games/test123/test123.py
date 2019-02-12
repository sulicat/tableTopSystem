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

    def render(self, screen):
        print("render test")

    def end(self):
        print("end test")
