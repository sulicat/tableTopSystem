import cv2 as cv
import numpy as np
import math
import sys
import random

TRASH_CUTOFF = 2
STAMP_CUTOFF = 0.4

THRESH_START = (66,142,47)
THRESH_END = (155,300,158)

def floodFillSelect( image, start ):
    w, h = image.shape
    mask = np.zeros( (w + 2, h + 2), np.uint8 )
    cv.floodFill(image, mask,  start, (255, 255, 255) )
    return mask


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
    thresh = ~thresh
    contours, hierarchy = cv.findContours ( thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE )
    return contours



# ----------------------------------------------------------------------------------------------------
def preProcessImage( image ):
    output = image.copy()
    output = cv.cvtColor(output, cv.COLOR_BGR2LAB)
    mask = cv.inRange( output, THRESH_START, THRESH_END )
    mask = ~mask
    kernel = np.ones( (3, 3), np.uint8 )
    mask = cv.erode( mask, kernel, iterations = 1)
    #mask = floodFillSelect(mask, (10,10))

    return mask


def findStamp( frame_contours, stamp_contour ):
    out = []
    print("--")
    cutoff = 0.8
    for cnt in frame_contours:
        for cnt_stamp in stamp_contour:
            ret = cv.matchShapes( cnt, cnt_stamp, 1, 0.0 )
            if ret < TRASH_CUTOFF and ret < STAMP_CUTOFF:
                x,y,w,h = cv.boundingRect( cnt )
                out.append( (x,y,w,h) )
                print(ret)



    return out


                                                                                                    

