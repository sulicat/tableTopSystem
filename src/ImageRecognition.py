import cv2 as cv
import numpy as np
import threading
import time
from misc import *
import sharedVars
import random
import math
import sys

sys.path.append("../imageRecognition/")
import stampFuncs as Stamp



'''
This is the class responsible for using the libraries created in house to identify and locate the stamps
This class will take N amount of frames
for every frame it recieved, it will parse the it into an XxY grid and append it to an array
The mode of these arrays is later published for the Graphics system to parse

This class also inherits Thread, therefore it runs asyncrously from the rest of the application.
Writing to BOARD_STATE is thread safe because Image Recognition is the only class allowed to write to it
Image recognition is supposed to be a singleton
'''
class ImageRecognition( threading.Thread ):
    def __init__( self, name ):
        threading.Thread.__init__(self)
        print_imr("image recognition started")
        print_imr("\tThread name: " + name )

        self.recognition_delay = 0.05
        self.image_count_max = 3
        self.image_current_count = 0
        self.cap = cv.VideoCapture(0)
        self.cap.set( cv.CAP_PROP_FRAME_WIDTH, 1920 )
        self.cap.set( cv.CAP_PROP_FRAME_HEIGHT, 1080 )

        self.local_board_states = []


    def run( self ):
        while( sharedVars.DONE ):
            if( self.image_current_count == self.image_count_max ):

                sharedVars.BOARD_STATE = mode_of_boards( self.local_board_states )

                time.sleep( self.recognition_delay )

                self.image_current_count = 0
                self.local_board_states = []

            else:
                print_imr("Frame")
                self.image_current_count += 1

                ret, frame = self.cap.read()
                self.local_board_states.append(Stamp.stamps( frame ))

