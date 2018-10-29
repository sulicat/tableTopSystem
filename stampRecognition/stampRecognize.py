import cv2 as cv
import numpy as np
import math
import sys
import random

random.seed(4)
orb = cv.ORB_create()


def returnStamp( inMap, stamps_x, bits, stampNumber ):
    map_h, map_w, map_channel = inMap.shape[:3]
    stamp_bits = bits
    stampCount_x = stamps_x
    stampSize = int(map_w / stampCount_x)
    x = stampNumber % stamps_x
    y = int((stampNumber / (stampCount_x)))

    return inMap[ y*stampSize : (y+1)*stampSize, x*stampSize : (x+1)*stampSize ]


def generateRandomStampImage( stampSize, stamp, image ):
    retval  = image;
    retSize = image.shape[:3]
    x = random.randint( 0, retSize[0] - stampSize[0] )
    y = random.randint( 0, retSize[1] - stampSize[1] )
    stamp = cv.resize( stamp, stampSize )
    retval[ y:y+stampSize[1], x:x+stampSize[0] ] = stamp

    return retval, (x,y)


#def findStamp( stamp, image ):
#    threshold = 0.5
#    stamp = cv.cvtColor( stamp, cv.COLOR_BGR2GRAY )
#    retval = image
#    image = cv.cvtColor( image, cv.COLOR_BGR2GRAY )
#    w, h = stamp.shape[::-1]

#    res = cv.matchTemplate(image, stamp, cv.TM_CCOEFF_NORMED)
#    loc = np.where( res >= threshold )

#    for pt in zip(*loc[::-1]):
#        cv.rectangle(retval, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

#    return retval


def findStamp( stamp, image ):
    kp1, des1 = orb.detectAndCompute( stamp,None )
    kp2, des2 = orb.detectAndCompute( image,None )
    # BFMatcher with default params
    bf = cv.BFMatcher()
    matches = bf.match( des1, des2 )
    matches = sorted(matches, key = lambda x:x.distance)
    #return cv.drawMatches(stamp, kp1, image, kp2, matches, None, flags=2)
    matchPixelPositions = []
    for match in matches:
        stamp_i = match.queryIdx
        image_i = match.trainIdx

        (x1, y1) = kp2[ image_i ].pt
        matchPixelPositions.append((int(x1), int(y1)))

    return matchPixelPositions



stampMap = cv.imread("../resources/testStamps/5_5.jpg")

#return the stamp #2
stamp2 = returnStamp( stampMap, 5, 5, 2 )
#return the stamp #2
stamp10 = returnStamp( stampMap, 5, 5, 10 )


#start with a blank image
startImage = np.zeros( [ 800, 800, 3 ], np.uint8 );
#randomly overlay 1 stamp on it
output, pos2 = generateRandomStampImage( (50, 50), stamp2, startImage )
output, pos2 = generateRandomStampImage( (100, 100), stamp2, startImage )
output, pos2 = generateRandomStampImage( (150, 150), stamp2, startImage )
output, pos2 = generateRandomStampImage( (200, 200), stamp2, startImage )


#matches = findStamp( stamp2, output )
#for match in matches:
#    print(match)

matches = findStamp( stamp2, output )

for match in matches:
    cv.rectangle(output, match, (match[0] + 10, match[1] + 10), (0,0,255) )


cv.imshow( "image", output )
while 1:
    if cv.waitKey(33) == ord('q'):
        break



'''
for i in range( 0, 32 ):
    output = returnStamp( stampMap, 5, 5, i )
    cv.imshow( "image", output )
    while 1:
        if cv.waitKey(33) == ord('q'):
            break
'''
