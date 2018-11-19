import cv2 as cv
import numpy as np
import math
import sys
import random


def returnStamp( inMap, stamps_x, bits, stampNumber ):
    map_h, map_w, map_channel = inMap.shape[:3]
    stamp_bits = bits
    stampCount_x = stamps_x
    stampSize = int(map_w / stampCount_x)
    x = stampNumber % stamps_x
    y = int( (stampNumber / (stampCount_x)) )

    return inMap[ y*stampSize : (y+1)*stampSize, x*stampSize : (x+1)*stampSize ]


def preProcessImage( image ):
    output = image.copy()
    w, h, c = output.shape[:3]
    for r in range( 0, h ):
        for c in range( 0, w ):
            if( output[r][c][0] > 50 or output[r][c][2] > 50 ):
                output[r][c] = 0

    return output



def findStamp( image, stamp, fill=(0,0,255) ):
    output = image.copy()
#    output = preProcessImage( output )
    image_gray = cv.cvtColor( output, cv.COLOR_BGR2GRAY )
#    image_gray = image.copy()
    stamp_gray = cv.cvtColor( stamp, cv.COLOR_BGR2GRAY )


    #apply erosion
    kernel = np.ones( (2, 2),np.uint8 )
    image_erosion = cv.erode( image_gray, kernel, iterations = 1 )
    stamp_erosion = cv.erode( stamp_gray, kernel, iterations = 1 )

    #retrieve edges with Canny
    thresh = 175
    #image_edges = cv.Canny( image_erosion, thresh, thresh*2 )
    #stamp_edges = cv.Canny( stamp_erosion, thresh, thresh*2 )

    ret, image_thresh = cv.threshold(image_erosion, 127, 255, 0)
    ret, stamp_thresh = cv.threshold(stamp_erosion, 127, 255, 0)

    #image_contours, image_hierarchy = cv.findContours( image_edges, cv.cv.CV_RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)
    #stamp_contours, stamp_hiererchy = cv.findContours( stamp_edges, cv.cv.CV_RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)
    image_c, image_contours, image_hierarchy = cv.findContours ( image_thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE )
    stamp_c, stamp_contours, stamp_hierarchy = cv.findContours ( stamp_thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE )

    #cv.drawContours( output, image_contours, -1, (255,0,0), 3 )
    #cv.drawContours( output, stamp_contours, -1, (255,0,0), 3 )

    output = []


    cutoff = 0.4
    for cnt in image_contours:
        ret = cv.matchShapes( cnt, stamp_contours[0], 1, 0.0 )
        print(ret)
        if ret < cutoff:
            x,y,w,h = cv.boundingRect( cnt )
            cv.rectangle( image, ( int(x),int(y) ), (int(x+w), int(y+h)), fill, 3, 200 )
            output.append( (x,y,w,h) )

    print("__________________________________________")

    return output, image_contours, stamp_contours


def addToTestImage( image, stamp, pos=None, size=None, angle=0 ):
    output = image.copy()
    tempStamp = stamp.copy()

    if( size != None ):
        tempStamp = cv.resize( tempStamp, size )

    sw, sh, sc = tempStamp.shape[:3]
    iw, ih, ic = image.shape[:3]

    rotate_matrix = cv.getRotationMatrix2D( (sw/2, sh/2), angle, 1 )
    tempStamp = cv.warpAffine( tempStamp, rotate_matrix, (sw, sh) )

    if( pos == None ):
        x = random.randint( 0, iw - sw )
        y = random.randint( 0, ih - sh )
    else:
        x = pos[0]
        y = pos[1]

    #output[ y:y+sh, x:x+sw ] = tempStamp

    for r in range( y, y+sh):
        for c in range( x, x+sw):
            if( tempStamp[r-y][c-x][1] > 200 ):
                output[r][c] = tempStamp[r-y][c-x]

    return output


