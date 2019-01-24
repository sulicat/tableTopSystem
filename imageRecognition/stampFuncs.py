import cv2 as cv
import numpy as np
import math
import sys
import random

# ----------------------------------------------------------------------------------------------------
def returnStamp( inMap, stamps_x, bits, stampNumber ):
    map_h, map_w, map_channel = inMap.shape[:3]
    stamp_bits = bits
    stampCount_x = stamps_x
    stampSize = int(map_w / stampCount_x)
    x = stampNumber % stamps_x
    y = int( (stampNumber / (stampCount_x)) )

    return inMap[ y*stampSize : (y+1)*stampSize, x*stampSize : (x+1)*stampSize ]


                                                                                                    
# ----------------------------------------------------------------------------------------------------
def preProcessImage( image ):

    output = image.copy()
    mask = cv.inRange( output, (0, 200, 0), (255, 255, 255) )
    kernel = np.ones( (4, 4), np.uint8 )
    mask = cv.erode( mask, kernel, iterations = 1)

    return mask



                                                                                                    

