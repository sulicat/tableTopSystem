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
import os

bit_colors = [ (255,0,0), (0,255,255), (0,255,0), (0,0,255), (255,255,0) ]
font = cv.FONT_HERSHEY_SIMPLEX

cap = cv.VideoCapture(0)

cap.set( cv.CAP_PROP_FRAME_WIDTH, 1920 )
cap.set( cv.CAP_PROP_FRAME_HEIGHT, 1080 )

ret, frame_original = cap.read()

rows, cols, d = frame_original.shape

frame_original = Stamp.cameraCalibrate( frame_original )
frame_img = frame_original.copy()
frame_original = Stamp.fixPerspective( frame_original )

frame = Stamp.preProcessImage( frame_original )
im, contours, hierarchy = cv.findContours ( frame, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE )

rotation_contours = contours.copy()
rotation_contours.pop(0)
cv.drawContours( frame_original, rotation_contours, -1, (255,0,255), 2 )

stamp_bounds_w_angle, new_cont = Stamp.fineStampLocationsWRotation( rotation_contours )

frame_show = frame_original.copy()
for (rect, angle) in stamp_bounds_w_angle:
    bits, ID = Stamp.findIDwRotation( new_cont, rect, angle )
    cv.putText( frame_show, str(ID), (int(rect[0][0]), int(rect[0][1])), font, 1, (0,0,255), 3, cv.LINE_AA )

    box = cv.boxPoints(rect)
    pnts = np.array( box, np.int32 )
    cv.polylines(frame_show, [pnts], True, (255,0,255), 1)

    for (poly, rect_bit, bit) in bits:
        cv.polylines(frame_show, [poly], True, bit_colors[bit], 1)
        cv.putText( frame_show, str(bit), (int(poly[0][0][0]), int(poly[0][0][1])), font, 0.5, (255,255,255), 1, cv.LINE_AA )


cv.imwrite("/var/www/html/frame0.png", frame_show)
cv.imwrite("/var/www/html/frame1.png", frame_img)
