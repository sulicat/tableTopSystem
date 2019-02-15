import sys
sys.path.append("../../")
import Graphics
import misc
import numpy as np

class test123( Graphics.Game ):
    def __init__(self, name):
        super().__init__(name)

    def start(self):
        print("start test")

    def render(self, screen, board):
        screen.fill( (0,0,0) )
        misc.render_grid( screen, thickness=4 )
        x = np.where(board == 25)
        ball_spawn_1 = np.asarray(x).T.tolist()
        print(ball_spawn_1)




    def end(self):
        print("end test")
