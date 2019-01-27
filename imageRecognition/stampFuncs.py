import cv2 as cv
import numpy as np
import math
import sys
import random


# --------------------------------------------------------------------------------
TRASH_CUTOFF = 2
STAMP_CUTOFF = 30

#THRESH_START = (0,0,245)
#THRESH_END = (300,44,300)

THRESH_START = (0,26,242)
THRESH_END = (110,300,300)

# --------------------------------------------------------------------------------
IMG_BIT_STARTER = "../resources/bit_starter.jpg"
stamp_original = cv.imread(IMG_BIT_STARTER)
stamp_starter = cv.imread(IMG_BIT_STARTER)
stamp_starter = cv.cvtColor(stamp_starter, cv.COLOR_BGR2GRAY)
ret, thresh_starter = cv.threshold(stamp_starter, 127, 255, 0)
stamp_starter = ~thresh_starter

contours_starter, hierarchy_starter = cv.findContours ( stamp_starter, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE )
cv.drawContours( stamp_original, contours_starter, -1, (255,0,0), 3 )

# --------------------------------------------------------------------------------
bit_locations = [
    (0, 0.15, 0.5, 0.35),
    (0.5, 0.15, 0.5, 0.35),
    (0, 0.5, 0.35, 0.5),
    (0.35, 0.5, 0.3, 0.5),
    (0.65, 0.5, 0.35, 0.5)
]

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
    output = cv.cvtColor(output, cv.COLOR_BGR2HSV)
    mask = cv.inRange( output, THRESH_START, THRESH_END )
    mask = ~mask
    kernel = np.ones( (3, 3), np.uint8 )
    mask = cv.erode( mask, kernel, iterations = 1)
    #mask = floodFillSelect(mask, (10,10))
    return mask


def findStampLocations( frame_cnt ):
    global contours_starter
    out = []
    new_cont = []

    for cnt in frame_cnt:
        ret = cv.matchShapes( cnt, contours_starter[0], 1, 0.0 )
        if ret > STAMP_CUTOFF:
            x,y,w,h = cv.boundingRect( cnt )

            w_n = w*1.8
            h_n = w_n
            x_n = x - (w_n - w)/2
            y_n = y
            #y_n = y + h_n - h*1

            out.append( (x_n, y_n, w_n, h_n) )
            #new_cont.remove(cnt)

            #rect = cv.minAreaRect(cnt)
            #box = cv.boxPoints(rect)
            #box = np.int0(box)
        else:
            new_cont.append(cnt)

    return out, new_cont



def fineStampLocationsWRotation( frame_cnt ):
    global contours_starter
    out = []

    for cnt in new_cont:
        ret = cv.matchShapes( cnt, contours_starter[0], 1, 0.0 )
        if ret > STAMP_CUTOFF:
            x,y,w,h = cv.boundingRect( cnt )
            rect = cv.minAreaRect(cnt)
            # rect includes the center, size and rotatation
            out.append( rect )

    return out



def findID( cntrs, box ):
    out = []
    i = 0
    ID = 0
    for (_x, _y, _w, _h) in bit_locations:
        b_x = box[0] + box[2]*_x
        b_y = box[1] + box[3]*_y
        b_w = box[2]*_w
        b_h = box[3]*_h
        #out.append(  (b_x, b_y, b_w, b_h) )
        bit_area = recArea( (b_x, b_y, b_w, b_h) )

        sum_cnt_area = 0
        for cnt in cntrs:
            x,y,w,h = cv.boundingRect( cnt )
            intersect = intersection( [b_x, b_y, b_w, b_h], [x,y,w,h] )
            if intersect != (0,0,0,0):
                out.append( (intersect, i) )
                sum_cnt_area += recArea( intersect )

        if sum_cnt_area > bit_area * 0.1:
            ID = ID | (1 << i)

        i = i + 1

    return out, ID


def recArea( rec ):
    # x, y, w, h
    return rec[2]*rec[3]

def safeTuple(inputList):
    return tuple(map(lambda x: int(x), inputList))

def union(a,b):
    x = min(a[0], b[0])
    y = min(a[1], b[1])
    w = max(a[0]+a[2], b[0]+b[2]) - x
    h = max(a[1]+a[3], b[1]+b[3]) - y
    return (x, y, w, h)

def intersection(a,b):
    x = max(a[0], b[0])
    y = max(a[1], b[1])
    w = min(a[0]+a[2], b[0]+b[2]) - x
    h = min(a[1]+a[3], b[1]+b[3]) - y
    if w<0 or h<0: return (0,0,0,0)
    return (x, y, w, h)


                                                                                                    
