import cv2 as cv
import numpy as np
import math
import sys
import random
sys.path.append("../imageRecognition/")
import stampFuncs as Stamp
import imutils
from scipy.interpolate import splprep, splev
import random
import statistics

cap = cv.VideoCapture(0)
cap.set( cv.CAP_PROP_FRAME_WIDTH,  1920 )
cap.set( cv.CAP_PROP_FRAME_HEIGHT, 1080 )


'''
A quick script that will allow us to visiblt test and debug our perspective fixing constants.
We need these constants to be easily calibrated as we are still finalizing the final build, and the webcam moves around a lot
'''

while( True ):

    ret, frame_original = cap.read()
    rows, cols, d = frame_original.shape
    M = cv.getRotationMatrix2D((cols/2,rows/2), 180, 1)
    # NOTE THIS IS CROPPING THE IMAGE --- FIX ME LAZY
    #frame_original = cv.warpAffine(frame_original, M, (cols,rows))

    frame_calib = Stamp.cameraCalibrate( frame_original )
    frame_skew = Stamp.fixPerspective( frame_calib )


    for pnt in Stamp.ACTIVE_AREA:
        cv.circle(frame_calib, (pnt[0], pnt[1]), 5, (255,0,255), -1)

    for pnt in Stamp.ACTIVE_AREA:
        cv.circle(frame_skew, (pnt[0], pnt[1]), 5, (255,255, 0), -1)

    cv.namedWindow("ior fix", cv.WINDOW_NORMAL)
    cv.imshow( "ior fix", frame_calib )
    cv.imshow( "test", frame_skew )

    if cv.waitKey(1) & 0xFF == ord('q'):
        break
