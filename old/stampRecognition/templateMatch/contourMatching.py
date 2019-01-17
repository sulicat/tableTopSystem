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

    cutoff = 1
    for cnt in image_contours:
        ret = cv.matchShapes( cnt, stamp_contours[0], 1, 0.0 )
        if ret < cutoff:
            x,y,w,h = cv.boundingRect( cnt )
            cv.rectangle( image, ( int(x),int(y) ), (int(x+w), int(y+h)), fill, 3, 200 )
            #print(ret)


    return image



'''
def findStamp( image, stamp, fill=(0,0,255) ):
    output = image.copy()
#    output = preProcessImage( output )

#    image_gray = cv.cvtColor( output, cv.COLOR_BGR2GRAY )

    image_gray = image.copy()
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

    output = []

    cutoff = 1
    for cnt in image_contours:
        ret = cv.matchShapes( cnt, stamp_contours[0], 1, 0.0 )
        if ret < cutoff:
            x,y,w,h = cv.boundingRect( cnt )
            cv.rectangle( image, ( int(x),int(y) ), (int(x+w), int(y+h)), fill, 3, 200 )
            #print(ret)
            output.append( (x,y,w,h) )

        ret = cv.matchShapes( cnt, stamp_contours[1], 1, 0.0 )
        if ret < cutoff:
            x,y,w,h = cv.boundingRect( cnt )
            cv.rectangle( image, ( int(x),int(y) ), (int(x+w), int(y+h)), fill, 3, 200 )
            #print(ret)
            output.append( (x,y,w,h) )

    return output
'''

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



stampMap = cv.imread("../../resources/testStamps/5_5.jpg")

stamp0 = returnStamp( stampMap, 5, 5, 0 )
stamp1 = returnStamp( stampMap, 5, 5, 1 )
stamp2 = returnStamp( stampMap, 5, 5, 2 )
stamp10 = returnStamp( stampMap, 5, 5, 10 )

###############################################3

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

###############################################3


'''
#temp = cv.imread("../../resources/randomImages/metallica.png")
temp  = np.zeros( [ 800, 800, 3 ], np.uint8 )
temp = cv.resize( temp, (800, 800))

output = addToTestImage( temp, stamp2, (0,0), (200, 200) )
output = addToTestImage( output, stamp2, (0,200), (200, 200), 30 )
output = addToTestImage( output, stamp2, (0,400), (200, 200), 60 )
output = addToTestImage( output, stamp2, (0,600), (200, 200), 90 )


output = addToTestImage( output, stamp1, (200,0), (200, 200), 0 )
output = addToTestImage( output, stamp1, (200,200), (200, 200), 30 )
output = addToTestImage( output, stamp1, (200,400), (200, 200), 60 )
output = addToTestImage( output, stamp1, (200,600), (200, 200), 90 )


output = addToTestImage( output, stamp10, (400,0), (200, 200), 0 )
output = addToTestImage( output, stamp10, (400,200), (200, 200), 30 )
output = addToTestImage( output, stamp10, (400,400), (200, 200), 60 )
output = addToTestImage( output, stamp10, (400,600), (200, 200), 90 )


show = findStamp( output, stamp2, fill=(255, 0, 0) )
show = cv.resize( show, (500, 500) )
cv.imshow( "image0", show )

show = findStamp( output, stamp1, fill=(255, 255, 0) )
show = cv.resize( show, (500, 500) )
cv.imshow( "image1", show )

show = findStamp( output, stamp10, fill=(255, 0, 255) )
show = cv.resize( show, (500, 500) )
cv.imshow( "image2", show )

'''
while 1:
    if cv.waitKey(33) == ord('q'):
        break



cv.imwrite( "out.jpg", show)

