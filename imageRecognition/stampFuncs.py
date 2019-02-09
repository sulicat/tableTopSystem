import cv2 as cv
import numpy as np
import math
import sys
import random


# --------------------------------------------------------------------------------
font = cv.FONT_HERSHEY_SIMPLEX
bit_colors = [ (255,0,0), (0,255,255), (0,255,0), (0,0,255), (255,255,0) ]

TRASH_CUTOFF = 2
STAMP_CUTOFF = 29
AREA_CUTOFF = 0

#THRESH_START = (0, 67, 237)
#THRESH_END = (103, 350, 350)

#THRESH_START = (236, 179, 0)
#THRESH_END = (350, 284, 164)

THRESH_START = (0, 67, 238)
THRESH_END = (102, 350, 350)

# out height is fixed, so we can fix our stamp size
STAMP_W = 70
STAMP_H = 70
BIT_PERCENT_AREA = 0.35

# cropping area
ACTIVE_AREA = [ [671,  72],
                [1490, 92],
                [612,  1008],
                [1584, 1000] ]

#720
CAMERA_CALIB_MTX = np.array(
    [[ 874.90931472,    0.,          658.1936634 ],
     [   0.,          878.7926458,   385.33508979],
     [   0.,            0.,            1.        ]]
, np.float)


#720
CAMERA_CALIB_DIST = np.array(
    [[-0.35168813,  0.13369811, -0.00114138, -0.00110096, -0.02812739]]
    , np.float)



#1080
CAMERA_CALIB_MTX = np.array(
    [[  1.24001474e+04,   0.00000000e+00,   9.53052572e+02],
     [  0.00000000e+00,   7.21448228e+03,   5.37881141e+02],
     [  0.00000000e+00,   0.00000000e+00,   1.00000000e+00]]
, np.float)

#1080
CAMERA_CALIB_DIST = np.array(
[[ -7.74490514e+00,  -1.31558309e+02,  -2.40244863e-02, -2.86903700e-03, 1.18994236e+04]]
    , np.float)



# --------------------------------------------------------------------------------
IMG_BIT_STARTER = "../resources/bit_starter.jpg"
#IMG_BIT_STARTER = "../resources/bit_starter_03.jpg"
stamp_original = cv.imread(IMG_BIT_STARTER)
stamp_starter = cv.imread(IMG_BIT_STARTER)
stamp_starter = cv.cvtColor(stamp_starter, cv.COLOR_BGR2GRAY)
ret, thresh_starter = cv.threshold(stamp_starter, 127, 255, 0)
stamp_starter = ~thresh_starter

im, contours_starter, hierarchy_starter = cv.findContours ( stamp_starter, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE )
cv.drawContours( stamp_original, contours_starter, -1, (255,0,0), 3 )

# --------------------------------------------------------------------------------
bit_locations = [
    (0, 0.15, 0.5, 0.35),
    (0.5, 0.15, 0.5, 0.35),
    (0, 0.5, 0.35, 0.5),
    (0.35, 0.5, 0.3, 0.5),
    (0.65, 0.5, 0.35, 0.5)
]


# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

# Perspecitive Fix calculations
(tl, tr, bl, br) = ACTIVE_AREA
widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
perspective_maxWidth = max(int(widthA), int(widthB))

heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
perspective_maxHeight = max(int(heightA), int(heightB))

perspecitive_dst = np.array([
    [0, 0],
    [perspective_maxWidth - 1, 0],
    [0, perspective_maxHeight - 1],
    [perspective_maxWidth - 1, perspective_maxHeight - 1]], dtype = "float32")

perspecitive_src = np.float32( ACTIVE_AREA )
perspective_M = cv.getPerspectiveTransform( perspecitive_src, perspecitive_dst )



# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

def floodFillSelect( image, start ):
    w, h = image.shape
    mask = np.zeros( (w + 2, h + 2), np.uint8 )
    cv.floodFill(image, mask,  start, (255, 255, 255) )
    return mask


def rotateBound(image, angle):
    # grab the dimensions of the image and then determine the
    # center
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)

    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))

    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY

    # perform the actual rotation and return the image
    return cv.warpAffine(image, M, (nW, nH))



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
    im2, contours, hierarchy = cv.findContours ( thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE )
    return contours



# ----------------------------------------------------------------------------------------------------
def cameraCalibrate( image ):
    global CAMERA_CALIB_MTX
    global CAMERA_CALIB_DIST

    h,  w = image.shape[:2]
    newcameramtx, roi = cv.getOptimalNewCameraMatrix( CAMERA_CALIB_MTX, CAMERA_CALIB_DIST, (w,h), 1, (w,h))
    mapx, mapy = cv.initUndistortRectifyMap(CAMERA_CALIB_MTX, CAMERA_CALIB_DIST, None, newcameramtx, (w,h), 5)
    frame_calib = cv.remap(image, mapx,mapy, cv.INTER_LINEAR)
    return frame_calib



def fixPerspective( image ):
    global perspective_maxWidth
    global perspective_maxHeight
    global perspective_M

    frame_skew = cv.warpPerspective( image, perspective_M, (perspective_maxWidth, perspective_maxHeight))
    return frame_skew



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

    #print("--------------------------------------------------------------------------------")
    for cnt in frame_cnt:
        ret = cv.matchShapes( cnt, contours_starter[0], 1, 0.0 )
        area = cv.contourArea( cnt )
        #print(str(ret) + " " + str(area))
        if ret > STAMP_CUTOFF and area > AREA_CUTOFF:
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
    sum_area = 0

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

        #if( _c[0] < _c[1] ):
        #    angle -= 90
        #    print("asdf")

        rect_out = ( _c, _s, angle )

        # now we want to find out which bit it is
        sum_area = 0
        for cnt in cntrs:
            x,y,w,h = cv.boundingRect(cnt)
            cnt_rect = ((x+w/2,y+h/2), (w,h), 0)
            cnt_rect1 = cv.boxPoints(cnt_rect)
            cnt_rect1 = np.int0(cnt_rect1)
            #cv.drawContours(frame_original, [cnt_rect1], 0, (0,0,255), 1)

            rec1 = cv.boxPoints(rect_out)
            rec1 = np.int0(rec1)
            #cv.drawContours(frame_original, [rec1], 0, (0,0,0), 1)

            ret, reg = findIntersection( cnt_rect, rect_out )
            if ret != 0:
                #cv.polylines(frame_original, [reg], True, (0,255,0), 2)
                #cv.fillPoly(frame_original, [reg], bit_colors[bit] )
                area = cv.contourArea(reg)
                sum_area += area



        area_bit = bit_w * bit_h
        if( sum_area > area_bit*BIT_PERCENT_AREA ):
            ID = ID | (1 << i)

        out.append( (poly, rect_out, i) )
        i += 1

    return out, ID


def stampsInGrid( stamps, cont, image, cells_x = 8, cells_y=8 ):
    w, h, c = image.shape
    out_img = np.zeros( [w,h,3], dtype=np.uint8 )
    out_arr = np.zeros( [cells_x, cells_y], dtype=np.uint8 )

    for (rect, angle) in stamps:
        bits, ID = findIDwRotation( cont, rect, angle )
        if( ID != 0 ):
            pos_x = rect[0][0]
            pos_y = rect[0][1]
            pos_x = int( (pos_x / w) * cells_x )
            pos_y = int( (pos_y / h) * cells_y )
            out_arr[pos_y][pos_x] = ID


    padding_x = int((w/cells_x) / 2)
    padding_y = int((h/cells_y) / 2)

    for r in range( 0, cells_y ):
        for c in range( 0, cells_x ):
            _color = (255,255,255)

            if( out_arr[r][c] != 0 ):
                _color = (255,0,255)

            cv.putText( out_img, str(out_arr[r][c]), (int(c*(w/cells_x) + padding_x), int(r*(h/cells_y)) + padding_y), font, 1, _color, 1, cv.LINE_AA )


    return out_img, out_arr



def stampsInImage( stamps, cont, image, cells_x = 8, cells_y=8 ):
    output = image.copy()
    for (rect, angle) in stamps:
        bits, ID = findIDwRotation( cont, rect, angle )
        cv.putText( output, str(ID), (int(rect[0][0]), int(rect[0][1])), font, 1, (0,0,255), 3, cv.LINE_AA )

        box = cv.boxPoints(rect)
        pnts = np.array( box, np.int32 )
        cv.polylines(output, [pnts], True, (255,0,255), 1)

        for (poly, rect_bit, bit) in bits:
            cv.polylines(output, [poly], True, bit_colors[bit], 1)
            cv.putText( output, str(bit), (int(poly[0][0][0]), int(poly[0][0][1])), font, 0.5, (255,255,255), 1, cv.LINE_AA )

    return output


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

        if sum_cnt_area > bit_area * BIT_PERCENT_AREA:
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


                                                                                                    
