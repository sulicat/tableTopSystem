import sys
sys.path.append("../../")
import Graphics
import misc
import numpy as np
import pygame

class test123( Graphics.Game ):
    def __init__(self, name):
        super().__init__(name)
        self.gravity = 1
        self.ball_pos = [200,0]
        self.ball_vel = [0,0]
        self.ball_acel = [0,self.gravity+0.5]
        self.ball_color = (180,102,0)
        self.ball_size = 30
        self.ball_spawn = False
        self.ball_bounce_count = 0

        self.ball2_pos = [200,0]
        self.ball2_vel = [0,0]
        self.ball2_acel = [0,self.gravity]
        self.ball2_color = (255,0,255)
        self.ball2_size = 50
        self.ball2_spawn = False
        self.ball2_bounce_count = 0


    def start(self):
        print("start test")

    def render(self, screen, menu, board):
        w, h = screen.get_width(), screen.get_height()

        screen.fill( (0,0,0) )
        misc.render_grid( screen, thickness=4 )
        x = np.where(board == 12)
        ball_loc = np.asarray(x).T.tolist()

        if( len(ball_loc) > 0 ):
            self.ball_pos = [ (8-ball_loc[0][1]) * (w/8) - self.ball_size, 0 ]
            self.ball_spawn = True
            self.ball_vel[0] = 0
            self.ball_vel[1] = 0



        if( self.ball_spawn == True):
            pygame.draw.circle(screen, self.ball_color, (int(self.ball_pos[0]),int(self.ball_pos[1])) , self.ball_size )
            self.ball_vel[0] += self.ball_acel[0]
            self.ball_vel[1] += self.ball_acel[1]
            self.ball_pos[0] += self.ball_vel[0]
            self.ball_pos[1] += self.ball_vel[1]

            if( self.ball_pos[1] + self.ball_size > h and self.ball_vel[1] >= 0):
                self.ball_pos[1] = h - self.ball_size
                self.ball_vel[1] = -0.85 * self.ball_vel[1]
                self.ball_bounce_count += 1

                if( self.ball_bounce_count > 3 ):
                    self.ball_spawn = False
                    self.ball_bounce_count = 0
                    self.ball_vel = [0,0]






        x = np.where(board == 24)
        ball_loc = np.asarray(x).T.tolist()

        if( len(ball_loc) > 0 ):
            self.ball2_pos = [ (8-ball_loc[0][1]) * (w/8) - self.ball2_size, 0 ]
            self.ball2_spawn = True
            self.ball2_vel[0] = 0
            self.ball2_vel[1] = 0


        if( self.ball2_spawn == True):
            pygame.draw.circle(screen, self.ball2_color, (int(self.ball2_pos[0]),int(self.ball2_pos[1])) , self.ball2_size )
            self.ball2_vel[0] += self.ball2_acel[0]
            self.ball2_vel[1] += self.ball2_acel[1]
            self.ball2_pos[0] += self.ball2_vel[0]
            self.ball2_pos[1] += self.ball2_vel[1]

            if( self.ball2_pos[1] + self.ball2_size > h and self.ball2_vel[1] >= 0):
                self.ball2_pos[1] = h - self.ball2_size
                self.ball2_vel[1] = -0.85 * self.ball2_vel[1]
                self.ball2_bounce_count += 1

                if( self.ball2_bounce_count > 3 ):
                    self.ball2_spawn = False
                    self.ball2_bounce_count = 0
                    self.ball2_vel = [0,0]





    def end(self):
        print("end test")
