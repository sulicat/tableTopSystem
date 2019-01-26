import cv2 as cv
import numpy as np
import math
import sys
import random
sys.path.append("../imageRecognition/")
import stampFuncs as Stamp
import imutils
from scipy.interpolate import splprep, splev

stampMap = cv.imread("../resources/asci_symbols_reg.jpg")
cap = cv.VideoCapture(2)
stamp1 = Stamp.returnStamp( stampMap, 5, 5, 22 )
stamp1_cont = Stamp.stampContours( stamp1 )

stampF = Stamp.returnStamp( stampMap, 5, 5, 3 )
stampF_cont = Stamp.stampContours( stampF )



while( True ):

    ret, frame_original = cap.read()
    rows, cols, d = frame_original.shape
    M = cv.getRotationMatrix2D((cols/2,rows/2),90,1)
    # NOTE THIS IS CROPPING THE IMAGE --- FIX ME LAZY
    frame_original = cv.warpAffine(frame_original, M, (cols,rows))

    frame = Stamp.preProcessImage( frame_original )
    contours, hierarchy = cv.findContours ( frame, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE )
    #cv.drawContours( frame_original, contours, -1, (255,0,0), 3 )


    print("--- 2 ---")
    stamp1_locations = Stamp.findStamp( contours, stamp1_cont )
    for (x,y,w,h) in stamp1_locations:
        cv.rectangle( frame_original, ( int(x),int(y) ), (int(x+w), int(y+h)), (0,255,0), 3, 200 )

    print("--- F ---")
    stampF_locations = Stamp.findStamp( contours, stampF_cont )
    for (x,y,w,h) in stampF_locations:
        cv.rectangle( frame_original, ( int(x),int(y) ), (int(x+w), int(y+h)), (0,0,255), 3, 200 )


    #frame = imutils.resize(frame, width=500)
    #frame_original = imutils.resize(frame_original, width=500)
    #frame_lab = imutils.resize(frame_lab, width=500)



    cv.imshow( "test2", frame_original )
    #cv.imshow( "test2", stampF )
    cv.imshow( "test", frame )

    if cv.waitKey(1) & 0xFF == ord('q'):
        break





