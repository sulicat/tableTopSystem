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

bit_colors = [ (255,0,0), (0,255,255), (0,255,0), (0,0,255), (255,255,0) ]
font = cv.FONT_HERSHEY_SIMPLEX
cap = cv.VideoCapture(2)

while( True ):

    ret, frame_original = cap.read()
    rows, cols, d = frame_original.shape
    M = cv.getRotationMatrix2D((cols/2,rows/2), 180, 1)
    # NOTE THIS IS CROPPING THE IMAGE --- FIX ME LAZY
    frame_original = cv.warpAffine(frame_original, M, (cols,rows))

    frame = Stamp.preProcessImage( frame_original )
    contours, hierarchy = cv.findContours ( frame, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE )

    stamp_locations, new_contours = Stamp.findStampLocations( contours )
    new_contours.pop(0) #NOT SURE ABOUT THIS

    for (x,y,w,h) in stamp_locations:
        cv.rectangle( frame_original, ( int(x),int(y) ), (int(x+w), int(y+h)), (0,0,255), 1, 200 )


    for s in stamp_locations:
        testBits, ID = Stamp.findID( new_contours,  s)
        for ((x,y,w,h), bit) in testBits:
            cv.rectangle( frame_original, ( int(x),int(y) ), (int(x+w), int(y+h)), bit_colors[bit], 1, 200 )
            cv.putText( frame_original, str(bit), (int(x), int(y)), font, 0.5, (255,255,255), 1, cv.LINE_AA )
            #cv.rectangle( frame_original, ( int(x),int(y) ), (int(x+w), int(y+h)), (255,0,255), 1, 200 )

        cv.putText( frame_original, str(ID), (int(s[0]), int(s[1])), font, 1, (255,0,255), 2, cv.LINE_AA )


    #stamp_locations_rot = Stamp.fineStampLocationsWRotation( contours )
    #for rect in stamp_locations_rot:
    #        print(rect[2])
    #        print("")

    cv.imshow( "test2", frame_original )

    if cv.waitKey(1) & 0xFF == ord('q'):
        break





