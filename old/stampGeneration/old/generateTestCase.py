import cv2 as cv
import numpy as np
from random import randint

# first we load in the image
# for now, we assume the image title is as follows:
#   bits_colCount.jpg

colCount = 5
bitCount = 5
rowCount = int(((2**bitCount) / colCount) + 1)
stampChoice = 5
testImageSize = (1000, 1000)


testCaseImage = np.zeros( [testImageSize[0], testImageSize[1], 3], np.uint8 )


print( "cols: " + str(colCount) )
print( "rows: " + str(rowCount) )
print( "bits: " + str(bitCount) )

def chooseRandomStamp( inMap ):
    stampChoice = randint(0, bitCount)
    map_h, map_w, map_channel = inMap.shape[:3]
    stamp_w = int(map_w / (colCount))
    stamp_h = int(map_h / (rowCount))

    x = stamp_w * int( (stampChoice%colCount) )
    y = stamp_h * int( (stampChoice/colCount) )
    x += int( stamp_w *0.1 )
    y += int( stamp_h *0.1 )
    return inMap[ y:y+stamp_h, x:x+stamp_w ]




def test( inMap, tempChoice ):
    stampChoice = tempChoice
    map_h, map_w, map_channel = inMap.shape[:3]
    stamp_w = int(map_w / (colCount))
    stamp_h = int(map_h / (rowCount))

    x = stamp_w * int( (stampChoice%colCount) )
    y = stamp_h * int( (stampChoice/colCount) )

    cv.line( inMap, (x, 0), (x, map_h), (255,255,0), 20 )
    cv.line( inMap, (0, y), (map_w, y), (255,255,0), 20 )

    inMap = cv.resize( inMap, (500, int(500 * map_h / map_w) ))
    return inMap



allStamps = cv.imread( str(bitCount) + "_" + str(colCount) + ".jpg", cv.IMREAD_COLOR )
stampChoice = stampChoice % (2**bitCount)

chosenStamp = chooseRandomStamp( allStamps )
#chosenStamp = test( allStamps, tempChoice )
#cv.imshow( "img", chosenStamp)

# add the chosen Stamp to a random place on the image
x_add = randint(0, testCaseImage.shape[0] - chosenStamp.shape[0] )
y_add = randint(0, testCaseImage.shape[1] - chosenStamp.shape[1] )





cv.imshow( "img", testCaseImage )
while 1:
    if cv.waitKey(0) == ord('q'):
        break

#    elif cv.waitKey(0) != ord('q'):
#        chosenStamp = chooseRandomStamp( allStamps )
#        cv.imshow( "img", chosenStamp)

