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
import games.checkers.checkers as checkers
import games.colorTest.colorTest as colorTest
import games.rock_paper_scissors.rock_paper_scissors as rps


'''
Main Program entry point:
Here we first instantiate an Image recognition and Graphics thread
We add the games to the Graphics thread
Communication between these two threads is handles within the classes
'''

def main():
    image_recognition = ImageRecognition( "thread_imgrec" )
    graphics = Graphics( "thread_gphc" )

    graphics.addGame( checkers.Checkers("Checkers") )
    graphics.addGame( rps.rockPaperScissors("R/P/S") )
    graphics.addGame( test123.test123("Ball Demo") )
    graphics.addGame( chess.Chess("Chess") )
    graphics.addGame( colorTest.colorTest("Color Test") )

    graphics.start()
    image_recognition.start()

    graphics.join()
    image_recognition.join()



if __name__ == '__main__': main()
