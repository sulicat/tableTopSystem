import cv2 as cv
import numpy as np
import math
import sys
import random
sys.path.append("../imageRecognition/")
import stampFuncs as Stamp
import imutils

stampMap = cv.imread("../resources/asci_symbols_reg.jpg")
cap = cv.VideoCapture(2)
stamp1 = Stamp.returnStamp( stampMap, 5, 5, 22 )


while( True ):
    ret, frame_original = cap.read()
    frame = Stamp.preProcessImage( frame_original )

    image_contours, image_hierarchy = cv.findContours ( frame, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE )

    cv.drawContours( frame_original, image_contours, -1, (255, 0, 0), 3)



    cv.imshow( "test", frame )
    cv.imshow( "test2", frame_original )

    if cv.waitKey(1) & 0xFF == ord('q'):
        break





