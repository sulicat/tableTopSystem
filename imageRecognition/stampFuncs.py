import cv2 as cv
import numpy as np
import math
import sys
import random

TRASH_CUTOFF = 2
STAMP_CUTOFF = 0.4


# ----------------------------------------------------------------------------------------------------
def returnStamp( inMap, stamps_x, bits, stampNumber ):
    map_h, map_w, map_channel = inMap.shape[:3]
    stamp_bits = bits
    stampCount_x = stamps_x
    stampSize = int(map_w / stampCount_x)
    x = stampNumber % stamps_x
    y = int( (stampNumber / (stampCount_x)) )

    return inMap[ y*stampSize : (y+1)*stampSize, x*stampSize : (x+1)*stampSize ]

                                                                                                    

def stampContours( stamp ):
    im = stamp.copy()
    imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(imgray, 127, 255, 0)
    contours, hierarchy = cv.findContours ( thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE )
    return contours[1]



# ----------------------------------------------------------------------------------------------------
def preProcessImage( image ):
    output = image.copy()
    mask = cv.inRange( output, (250, 0, 0), (255, 255, 255) )
    kernel = np.ones( (3, 3), np.uint8 )
    mask = cv.erode( mask, kernel, iterations = 1)
    return mask


def findStamp( frame_contours, stamp_contour ):
    out = []

    cutoff = 0.8
    for cnt in frame_contours:
        ret = cv.matchShapes( cnt, stamp_contour, 1, 0.0 )
        if ret < TRASH_CUTOFF and ret < STAMP_CUTOFF:
            x,y,w,h = cv.boundingRect( cnt )
            out.append( (x,y,w,h) )



    return out


                                                                                                    

