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

        self.recognition_delay = 0.1
        self.image_count_max = 5
        self.image_current_count = 0
        self.cap = cv.VideoCapture(0)
        self.cap.set( cv.CAP_PROP_FRAME_WIDTH, 1920 )
        self.cap.set( cv.CAP_PROP_FRAME_HEIGHT, 1080 )

        self.local_board_states = []


    def run( self ):
        global BOARD_STATE

        while( True ):
            if( self.image_current_count == self.image_count_max ):

                condition.acquire()
                print_imr("output modify")

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



class Graphics( threading.Thread ):
    def __init__( self, name ):
        threading.Thread.__init__(self)
        print_grph("Graphics System Started")
        print_grph("\tThread name: " + name )

        self.run_timer = 1


    def run( self ):
        global BOARD_STATE
        while( True ):
            #print_grph("Graphics Run")
            #xprint(BOARD_STATE)
            time.sleep( self.run_timer )






def main():
    image_recognition = ImageRecognition( "thread_imgrec" )
    graphics = Graphics( "thread_gphc" )


    graphics.start()
    image_recognition.start()


    graphics.join()
    image_recognition.join()



if __name__ == '__main__': main()
