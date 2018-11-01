import cv2 as cv
import numpy as np
import math
import sys
import random

stamp_size = 100
stamp_number = 0

if( len(sys.argv) != 3 ):
    print("Not correct args..... prog [size] [id]")
    sys.exit(1)

stamp_size = int(sys.argv[1])
stamp_number = int(sys.argv[2])
random.seed( stamp_number )


def imageRandomize( image, fill ):
    w, h, c = image.shape[:3]

    for i in range (0, 200):
        pos = ( random.randint(0, w), random.randint(0, h) )
        cv.circle( image, pos, random.randint(0, 20), fill, -1, 200 )

    for i in range (0, 200):
        posStart = ( random.randint(0, w - 20), random.randint(0, h - 20) )
        posEnd   = ( posStart[0] + random.randint(0, 30), posStart[1] + random.randint(0, 30) )
        cv.rectangle( image, posStart, posEnd, fill, -1, 200 )

    for i in range (0, 200):
        posStart = ( random.randint(0, w - 20), random.randint(0, h - 20) )
        posEnd   = ( posStart[0] + random.randint(-30, 30), posStart[1] + random.randint(-30, 30) )
        arr_pnts = []
        arr_pnts.append( (int(posStart[0]-10), posStart[1]) )
        arr_pnts.append( (int(posStart[0]+10), posStart[1]) )
        arr_pnts.append( posEnd )

        cv.fillConvexPoly( image, np.array( arr_pnts ), fill )

    return image

def imageGradient( image, fill ):
    w, h, c = image.shape[:3]
    heightScale = 0.05
    widthScale = 0.05

    for i in range (0, 250):
        pos = ( random.randint(0, w), random.randint(0, h) )
        cv.circle( image, pos, random.randint(0, 20), fill, -1, 200 )

    for i in range (0, 250):
        posStart = ( random.randint(0, w - 20), random.randint(0, h - 20) )
        posEnd   = ( posStart[0] + random.randint(0, 30), posStart[1] + random.randint(0, 30) )
        cv.rectangle( image, posStart, posEnd, fill, -1, 200 )

    for i in range (0, 250):
        posStart = ( random.randint(0, w), random.randint(0, h) )
        posEnd   = ( posStart[0] + random.randint(-1*w*widthScale, w*widthScale), posStart[1] + random.randint(-1*h*heightScale, h*heightScale) )
        arr_pnts = []
        arr_pnts.append( (int(posStart[0]-int(w*widthScale)), posStart[1]) )
        arr_pnts.append( (int(posStart[0]+int(w*widthScale)), posStart[1]) )
        arr_pnts.append( posEnd )

        cv.fillConvexPoly( image, np.array( arr_pnts ), fill )

    return image


def imageDeleteExtra( image, fill ):
    w, h, c = image.shape[:3]
    r = min( int(w/2), int(h/2) )
    pos = (int(w/2), int(h/2))
    mask = np.zeros( [ w, h, 3 ], np.uint8 )
    cv.circle( mask, pos, r, (255, 255, 255), -1, 200 )
    image = cv.bitwise_and(image, mask )

    r_arr = ( int(r*0.9), int(r*0.9) )
    cv.ellipse( image, pos, r_arr, 0, 30, 150, fill, int(r*0.2) )
    cv.ellipse( image, pos, r_arr, 0, 210, 330, fill, int(r*0.2) )

    mask = np.zeros( [ w, h, 3 ], np.uint8 )
    arr_pnts = []
    arr_pnts.append( pos )
    arr_pnts.append( (0, int(h/4)) )
    arr_pnts.append( (0, int(3*h/4)) )
    cv.fillConvexPoly( mask, np.array( arr_pnts ), (255, 255, 255) )

    arr_pnts = []
    arr_pnts.append( pos )
    arr_pnts.append( (w, int(h/4)) )
    arr_pnts.append( (w, int(3*h/4)) )
    cv.fillConvexPoly( mask, np.array( arr_pnts ), (255, 255, 255) )

    image = cv.bitwise_and( image, cv.bitwise_not(mask) )
    return image


def floodFillSelect( image, start ):
    w, h, c = image.shape[:3]
    mask = np.zeros( (w + 2, h + 2), np.uint8 )
    cv.floodFill(image, mask,  start, (255, 255, 255) )
    cv.floodFill(image, mask,  (start[0], h - start[1]), (255, 255, 255) )
    image = cv.inRange( image, (200, 200, 200), (255, 255, 255) )
    return image


def createRandomWalkStamp( size, idNum ):
    fill = (0, 255, 0)
    output = np.zeros( [ size, size, 3 ], np.uint8 )
#    output = imageRandomize( output, fill )
    output = imageGradient( output, fill )
    output = imageDeleteExtra( output, fill )
    output = floodFillSelect( output, (int(size/2), size - 3) )

    return output





output = createRandomWalkStamp( stamp_size, stamp_number )

cv.imshow( "image", output )
while 1:
    if cv.waitKey(33) == ord('q'):
        break

cv.imwrite( "random_" + str(stamp_number) + "_" + str(stamp_size) +".jpg", output)
