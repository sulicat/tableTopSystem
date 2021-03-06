#import cv2 as cv
import numpy as np
import threading
import time
from sharedVars import *
import random
import math
import sys
import json

from Graphics import *
#from ImageRecognition import *


'''
In order to allow for ease of developent, concidering we have 1 set of hardware, we wrote a replacement of main.py
that acts as a SIMULATOR for the image recognition system.

Using sim.py as the entry point for the program allows the user to run the system without running the image recognition library and without needing a webcam plugged in
the board state is simulated via a file sim_data.json
Editing sim_data.json will modify the current baord state in real time
'''
# manually importing the games. Writing plugin support not worth for starter
import games.test123.test123 as test123
import games.chess.chess as chess
import games.chess.chess1P as chess1P
import games.checkers.checkers as checkers
import games.checkers.checkers1P as checkers1P
import games.colorTest.colorTest as colorTest
import games.rock_paper_scissors.rock_paper_scissors as rps

class Sim( threading.Thread ):
    def __init__( self, name ):
        threading.Thread.__init__(self)
        print_sim("SIMulator Started")
        print_sim("\tThread name: " + name )

        self.recognition_delay = 0.05
        self.image_count_max = 3
        self.image_current_count = 0

        self.local_board_states = []

    def run( self ):
        while( sharedVars.DONE ):
            if( self.image_current_count == self.image_count_max ):

                sharedVars.BOARD_STATE = mode_of_boards( self.local_board_states )

                time.sleep( self.recognition_delay )

                self.image_current_count = 0
                self.local_board_states = []

            else:
                self.image_current_count += 1

                #ret, frame = self.cap.read()
                #self.local_board_states.append(Stamp.stamps( frame ))
                with open("sim_data.json") as f:
                    data = json.load(f)
                    new_data = []
                    for item in data["data"]:
                        new_data_temp = []
                        for i in reversed( range( len(item) ) ):
                            new_data_temp.append( item[i] )

                        new_data.append(new_data_temp)

                    time.sleep( 0.5 )
                    self.local_board_states.append(new_data)






def main():
    image_recognition = Sim( "thread_imgrec" )
    graphics = Graphics( "thread_gphc" )


    graphics.addGame( chess1P.Chess("D Chess 1P") )
    graphics.addGame( chess.Chess("D Chess 2P") )
    graphics.addGame( checkers.Checkers("D Checkers 2P") )
    graphics.addGame( checkers1P.Checkers("D Checkers 1P") )

    graphics.addGame( rps.rockPaperScissors("R/P/S") )
    graphics.addGame( test123.test123("Ball Demo") )
    graphics.addGame( colorTest.colorTest("Color Test") )


    graphics.start()
    image_recognition.start()

    graphics.join()
    image_recognition.join()



if __name__ == '__main__': main()
