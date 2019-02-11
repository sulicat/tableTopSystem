import cv2 as cv
import numpy as np
import threading
import time
from misc import *
from sharedVars import *
import random
import math
import sys

sys.path.append("../imageRecognition/")
import stampFuncs as Stamp


class ImageRecognition( threading.Thread ):
    def __init__( self, name ):
        threading.Thread.__init__(self)
        print_imr("image recognition started")
        print_imr("\tThread name: " + name )

        self.recognition_delay = 0.05
        self.image_count_max = 5
        self.image_current_count = 0
        self.cap = cv.VideoCapture(0)
        self.cap.set( cv.CAP_PROP_FRAME_WIDTH, 1920 )
        self.cap.set( cv.CAP_PROP_FRAME_HEIGHT, 1080 )

        self.local_board_states = []


    def run( self ):
        global BOARD_STATE
        global DONE

        while( DONE ):
            if( self.image_current_count == self.image_count_max ):

                condition.acquire()
                mode_of_boards( self.local_board_states )
                condition.notify_all()

                time.sleep( self.recognition_delay )
                condition.release()

                self.image_current_count = 0
                self.local_board_states = []

            else:
                print_imr("Frame")
                self.image_current_count += 1

                ret, frame = self.cap.read()
                self.local_board_states.append(Stamp.stamps( frame ))

