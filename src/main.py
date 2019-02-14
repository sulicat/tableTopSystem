import cv2 as cv
import numpy as np
import threading
import time
from misc import *
from sharedVars import *
import random
import math
import sys

from Graphics import *
from ImageRecognition import *


# manually importing the games. Writing plugin support not worth for starter
import games.test123.test123 as test123
import games.chess.chess as chess


'''
Main Program entry point:
Here we first instantiate an Image recognition and graphics thread
'''

def main():
    image_recognition = ImageRecognition( "thread_imgrec" )
    graphics = Graphics( "thread_gphc" )

    graphics.addGame( test123.test123("Test") )
    graphics.addGame( chess.Chess("Chess") )

    graphics.start()
    image_recognition.start()

    graphics.join()
    image_recognition.join()



if __name__ == '__main__': main()
