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



def main():
    image_recognition = ImageRecognition( "thread_imgrec" )
    graphics = Graphics( "thread_gphc" )

    graphics.start()
    image_recognition.start()

    graphics.join()
    image_recognition.join()



if __name__ == '__main__': main()
