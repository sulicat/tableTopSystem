import cv2 as cv
import numpy as np
import math
import sys
import random
sys.path.append("../imageRecognition/")
import stampFuncs as Stamp
import imutils

stampMap = cv.imread("../resources/asci_symbols_reg_small.jpg")
cap = cv.VideoCapture(2)
stamp1 = Stamp.returnStamp( stampMap, 5, 5, 22 )
stamp1_cont = Stamp.stampContours( stamp1 )

stampF = Stamp.returnStamp( stampMap, 5, 5, 3 )
stampF_cont = Stamp.stampContours( stampF )


thresh_Hs = 0
thresh_Ss = 0
thresh_Vs = 0
thresh_He = 255
thresh_Se = 255
thresh_Ve = 255

def Hs_range(x):
    global thresh_Hs
    thresh_Hs = x

def Ss_range(x):
    global thresh_Ss
    thresh_Ss = x

def Vs_range(x):
    global thresh_Vs
    thresh_Vs = x

def He_range(x):
    global thresh_He
    thresh_He = x

def Se_range(x):
    global thresh_Se
    thresh_Se = x

def Ve_range(x):
    global thresh_Ve
    thresh_Ve = x

cv.namedWindow('test')
cv.createTrackbar('H_S', 'test', 0, 300, Hs_range)
cv.createTrackbar('H_E', 'test', 0, 300, He_range)
cv.createTrackbar('S_S', 'test', 0, 300, Ss_range)
cv.createTrackbar('S_E', 'test', 0, 300, Se_range)
cv.createTrackbar('V_S', 'test', 0, 300, Vs_range)
cv.createTrackbar('V_E', 'test', 0, 300, Ve_range)


while( True ):
    ret, frame_original = cap.read()
    frame = Stamp.preProcessImage( frame_original )
    #contours, hierarchy = cv.findContours ( frame, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE )

    #stamp1_locations = Stamp.findStamp( contours, stamp1_cont )
    #for (x,y,w,h) in stamp1_locations:
    #    cv.rectangle( frame_original, ( int(x),int(y) ), (int(x+w), int(y+h)), (0,255,0), 3, 200 )


    #stampF_locations = Stamp.findStamp( contours, stampF_cont )
    #for (x,y,w,h) in stampF_locations:
    #    cv.rectangle( frame_original, ( int(x),int(y) ), (int(x+w), int(y+h)), (0,0,255), 3, 200 )



    frame_lab = cv.cvtColor(frame_original, cv.COLOR_BGR2HSV)
    fL,fA,fB = cv.split(frame_lab)
    #mask = cv.inRange( frame_lab, (0, 0, 0), (255, 120, 120) )
    mask = cv.inRange( frame_lab, (thresh_Hs, thresh_Ss, thresh_Vs), (thresh_He, thresh_Se, thresh_Ve) )
    mask = imutils.resize(mask, width=800)
    cv.imshow( "test", mask )


    #frame = imutils.resize(frame, width=500)
    #frame_original = imutils.resize(frame_original, width=500)
    #frame_lab = imutils.resize(frame_lab, width=500)



    cv.imshow( "test2", frame_original )
    #cv.imshow( "test", frame_lab )

    if cv.waitKey(1) & 0xFF == ord('q'):
        break





