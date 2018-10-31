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
stamp_number = int(sys.argv[1])






def createRandomWalkStamp( size, idNum ):
    output  = np.zeros( [ size, size, 3 ], np.uint8 )
    return output





output = createRandomWalkStamp( stamp_size, stamp_number )

cv.imshow( "image", output )
while 1:
    if cv.waitKey(33) == ord('q'):
        break
