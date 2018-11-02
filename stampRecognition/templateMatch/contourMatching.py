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


def findStamp( image, stamp ):
    output = image.copy()
    image_gray = cv.cvtColor( image, cv.COLOR_BGR2GRAY )
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

    cv.drawContours( output, image_contours, -1, (255,0,0), 3 )
    '''
    for cnt in image_contours:
        x,y,w,h = cv.boundingRect( cnt )
        cv.rectangle( image, ( int(x),int(y) ), (int(x+w), int(y+h)), (0,0,255), 1, 200 )
    '''

    for cnt in image_contours:
        ret = cv.matchShapes( cnt, stamp_contours[0], 1, 0.0 )
        if ret < 0.3:
            x,y,w,h = cv.boundingRect( cnt )
            cv.rectangle( output, ( int(x),int(y) ), (int(x+w), int(y+h)), (0,0,255), 3, 200 )
            print(ret)

    '''
    circles = cv.HoughCircles( image_thresh, cv.HOUGH_GRADIENT, 1, 20,
                               param1=50, param2=30, minRadius=0, maxRadius=0 )


    circles = np.uint16( np.around(circles) )
    for i in circles[0,:]:
        # draw the outer circle
        cv.circle(image, (i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
        cv.circle(image, (i[0],i[1]),2,(0,0,255),3)
    '''

    return output


stampMap = cv.imread("../../resources/testStamps/5_5.jpg")



stamp0 = returnStamp( stampMap, 5, 5, 0 )
stamp1 = returnStamp( stampMap, 5, 5, 1 )
stamp2 = returnStamp( stampMap, 5, 5, 2 )
stamp10 = returnStamp( stampMap, 5, 5, 10 )


output = findStamp( stampMap, stamp0 )
output = cv.resize( output, (400, 500) )
cv.imshow( "image0", output )


output = findStamp( stampMap, stamp1 )
output = cv.resize( output, (400, 500) )
cv.imshow( "image1", output )


output = findStamp( stampMap, stamp2 )
output = cv.resize( output, (400, 500) )
cv.imshow( "image2", output )


output = findStamp( stampMap, stamp10 )
output = cv.resize( output, (400, 500) )
cv.imshow( "image10", output )


while 1:
    if cv.waitKey(33) == ord('q'):
        break
