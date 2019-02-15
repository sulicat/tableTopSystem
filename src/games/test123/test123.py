import sys
sys.path.append("../../")
import Graphics
import misc

class test123( Graphics.Game ):
    def __init__(self, name):
        super().__init__(name)


    def start(self):
        print("start test")

    def render(self, screen, board):
        screen.fill( (255,0,255) )

        misc.render_grid( screen, thickness=4 )
        misc.render_cellFill( screen, 1, 1 )
        misc.render_cellFill( screen, 3, 1, color=(255,255,0) )


    def end(self):
        print("end test")
