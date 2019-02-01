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

cap = cv.VideoCapture(2)


ACTIVE_AREA = [ [300, 80],
                [1700, 80],
                [450, 1050],
                [1550, 1050] ]

while( True ):

    ret, frame_original = cap.read()
    rows, cols, d = frame_original.shape
    M = cv.getRotationMatrix2D((cols/2,rows/2), 180, 1)
    # NOTE THIS IS CROPPING THE IMAGE --- FIX ME LAZY
    #frame_original = cv.warpAffine(frame_original, M, (cols,rows))

    pts_from = np.float32( ACTIVE_AREA )

    pts_to = np.float32([ [0,0],
                          [cols,0],
                          [0,rows],
                          [cols,rows]
    ])

    M = cv.getPerspectiveTransform(pts_from, pts_to)
    frame_skew = cv.warpPerspective( frame_original, M, (cols,rows))

    for pnt in ACTIVE_AREA:
        cv.circle(frame_original, (pnt[0], pnt[1]), 5, (255,0,255), -1)





    cv.imshow( "test2", frame_original )
    cv.imshow( "test", frame_skew )

    if cv.waitKey(1) & 0xFF == ord('q'):
        break
