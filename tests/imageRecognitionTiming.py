import cv2 as cv
import numpy as np
import math
import sys
import random
sys.path.append("../imageRecognition/")
import stampFuncs as Stamp
import stampFuncsOptimized as StampFast


import time


cap = cv.VideoCapture(0)

cap.set( cv.CAP_PROP_FRAME_WIDTH, 1920 )
cap.set( cv.CAP_PROP_FRAME_HEIGHT, 1080 )


start = time.time()

for i in range( 20 ):
    a = time.time()

    ret, frame = cap.read()
    print( StampFast.stamps( frame ) )

    print( "i: " + str(i) + "\t" + str(time.time() - a) )

print( "Read: " + str(time.time() - start))
