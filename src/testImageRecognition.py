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

bit_colors = [ (255,0,0), (0,255,255), (0,255,0), (0,0,255), (255,255,0) ]
font = cv.FONT_HERSHEY_SIMPLEX
cap = cv.VideoCapture(2)

while( True ):
    ret, frame_original = cap.read()
    rows, cols, d = frame_original.shape

    frame_original = Stamp.cameraCalibrate( frame_original )
    frame_original = Stamp.fixPerspective( frame_original )
    frame_original = Stamp.rotateBound( frame_original, 90 )

    frame = Stamp.preProcessImage( frame_original )
    contours, hierarchy = cv.findContours ( frame, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE )

    #stamp_locations, new_contours = Stamp.findStampLocations( contours )
    #if len(new_contours) > 1:
    #    new_contours.pop(0)

    rotation_contours = contours.copy()
    rotation_contours.pop(0)
    cv.drawContours( frame_original, rotation_contours, -1, (255,0,0), 1 )

    stamp_bounds_w_angle, new_cont = Stamp.fineStampLocationsWRotation( rotation_contours )

    for (rect, angle) in stamp_bounds_w_angle:
        bits, ID = Stamp.findIDwRotation( new_cont, rect, angle )
        cv.putText( frame_original, str(ID), (int(rect[0][0]), int(rect[0][1])), font, 1, (0,0,255), 3, cv.LINE_AA )

        box = cv.boxPoints(rect)
        pnts = np.array( box, np.int32 )
        cv.polylines(frame_original, [pnts], True, (255,0,255), 1)

        #for (poly, rect_bit, bit) in bits:
            #cv.polylines(frame_original, [poly], True, bit_colors[bit], 1)
            #cv.putText( frame_original, str(bit), (int(poly[0][0][0]), int(poly[0][0][1])), font, 0.5, (255,255,255), 1, cv.LINE_AA )


    cv.imshow( "test2", frame_original )
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
