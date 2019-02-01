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

#THRESH_START = (0,26,242)
#THRESH_END = (110,300,300)

#THRESH_START = (73,73,230)
#THRESH_END = (160,300,300)

THRESH_START = (30, 0, 235)
THRESH_END = (109,350,350)

#THRESH_START = (49, 0, 242)
#THRESH_END = (112, 305, 350)

THRESH_START = (47, 68, 237)
THRESH_END = (109,350,350)


# out height is fixed, so we can fix our stamp size
STAMP_W = 90
STAMP_H = 90


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
    global STAMP_W
    global STAMP_H

    angle = 0
    out = []
    new_cont = []

    for cnt in frame_cnt:
        ret = cv.matchShapes( cnt, contours_starter[0], 1, 0.0 )
        print(ret)
        if ret > STAMP_CUTOFF:
            x,y,w,h = cv.boundingRect( cnt )
            rect = cv.minAreaRect(cnt)
            _w = rect[1][0]
            _h = rect[1][1]
            angle = rect[2]

            if( _w < _h ):
                angle += 90
            else:
                angle += 0

            trans_x = (STAMP_W / 2) * math.sin( math.radians(angle) )
            trans_y = (STAMP_H / 2) * math.cos( math.radians(angle) )

            rect_out = ( (rect[0][0] - trans_x, rect[0][1] + trans_y),
                         (STAMP_W, STAMP_H),
                         rect[2] )

            out.append( (rect_out, angle) )

        else:
            new_cont.append(cnt)

    return out, new_cont


def findIDwRotation( cntrs, box, angle ):
    out = []
    ID = 0
    i = 0
    center = box[0]
    box_w = box[1][0]
    box_h = box[1][1]

    top_left = [center[0] - box_w/2, center[1] - box_h/2]


    for (_x, _y, _w, _h) in bit_locations:
        bit_x = top_left[0] + box_w * _x
        bit_y = top_left[1] + box_h * _y
        bit_w = box_w * _w
        bit_h = box_h * _h

        #poly = np.array( [bit_x, bit_y, bit_x+bit_w, bit_y + bit_h], np.int32 )
        poly = np.array([ [bit_x, bit_y],
                          [bit_x, bit_y + bit_h],
                          [bit_x + bit_w, bit_y + bit_h],
                          [bit_x + bit_w, bit_y]
        ], np.int32 )

        M = cv.getRotationMatrix2D(center, -angle, 1)
        poly = np.array([poly])
        poly = cv.transform(poly, M)

        _c = ( np.mean( [poly[0][0][0], poly[0][1][0], poly[0][2][0], poly[0][3][0] ]),
               np.mean( [poly[0][0][1], poly[0][1][1], poly[0][2][1], poly[0][3][1] ])    )

        _s = ( bit_w, bit_h )

        if( _c[0] < _c[1] ):
            angle -= 90

        rect_out = ( _c, _s, angle )

        out.append( (poly, rect_out, i) )
        i += 1

    return out, 2


def findIntersection( rec1, rec2 ):
    retval, region = cv.rotatedRectangleIntersection(rec1, rec2)
    if retval != 0:
        region = [[item[0][0], item[0][1]] for item in region]
        region = np.array( region, np.int32 )

    return retval, region


                                                                                                    
































def findID( cntrs, box ):
    out = []
    i = 0
    ID = 0
    for (_x, _y, _w, _h) in bit_locations:
        b_x = box[0] + box[2]*_x
        b_y = box[1] + box[3]*_y
        b_w = box[2]*_w
        b_h = box[3]*_h
        #out.append(  ( (b_x, b_y, b_w, b_h), 0) )
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


                                                                                                    
