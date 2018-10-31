import cv2 as cv
import numpy as np
import math
import sys
import random




def addStampToImage( stamp, image, pos = -1 ):
    sw, sh, sc = stamp.shape[:3]
    iw, ih, ic = image.shape[:3]
    if( pos != -1 ):
        image[ pos[1]:pos[1]+sh, pos[0]:pos[0]+sw ] = stamp

    return image



def findStamp( stamp, image ):
    orb = cv.ORB_create()
    kp1, des1 = orb.detectAndCompute( stamp,None )
    kp2, des2 = orb.detectAndCompute( image,None )
    bf = cv.BFMatcher()
    matches = bf.match( des1, des2 )
    matches = sorted(matches, key = lambda x:x.distance)

    matchPixelPositions = []
    for match in matches:
        stamp_i = match.queryIdx
        image_i = match.trainIdx
        (x1, y1) = kp2[ image_i ].pt
        matchPixelPositions.append( (int(x1), int(y1)) )

    return matchPixelPositions





stamp0  = cv.imread( "../resources/blenderStamps/numbers/0.png" )
stamp0  = cv.resize( stamp0, (100, 100) )

stamp1  = cv.imread( "../resources/blenderStamps/numbers/1.png" )
stamp1  = cv.resize( stamp1, (50, 50) )

stamp25 = cv.imread( "../resources/blenderStamps/numbers/25.png" )
stamp25  = cv.resize( stamp25, (100, 100) )


output = np.zeros( [ 800, 800, 3 ], np.uint8 )
output = addStampToImage( stamp0, output, (0,0) )
output = addStampToImage( stamp1, output, (300,0) )
output = addStampToImage( stamp25, output, (300,300) )

cv.imshow( "start", output )

matches0 = findStamp( stamp0, output )
for match in matches0:
    cv.rectangle( output, match, (match[0] + 10, match[1] + 10), (0,0,255), -1 )

matches1 = findStamp( stamp1, output )
for match in matches1:
    cv.rectangle( output, match, (match[0] + 10, match[1] + 10), (255, 0, 255), -1 )

matches25 = findStamp( stamp25, output )
for match in matches25:
    cv.rectangle( output, match, (match[0] + 10, match[1] + 10), (255,0,0), -1 )


cv.imshow( "image", output )

while 1:
    if cv.waitKey(33) == ord('q'):
        break
