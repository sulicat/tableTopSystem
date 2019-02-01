import cv2 as cv
import numpy as np
import math
import sys
import random
sys.path.append("../imageRecognition/")
import stampFuncs as Stamp
import imutils
from scipy.interpolate import splprep, splev
import random
import statistics

bit_colors = [ (255,0,0), (0,255,255), (0,255,0), (0,0,255), (255,255,0) ]
font = cv.FONT_HERSHEY_SIMPLEX
cap = cv.VideoCapture(0)

while( True ):

    ret, frame_original = cap.read()
    rows, cols, d = frame_original.shape
    M = cv.getRotationMatrix2D((cols/2,rows/2), 180, 1)
    # NOTE THIS IS CROPPING THE IMAGE --- FIX ME LAZY
    #frame_original = cv.warpAffine(frame_original, M, (cols,rows))

    frame = Stamp.preProcessImage( frame_original )
    contours, hierarchy = cv.findContours ( frame, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE )

    stamp_locations, new_contours = Stamp.findStampLocations( contours )
    new_contours.pop(0)

    rotation_contours = contours.copy()
    rotation_contours.pop(0)
    #cv.drawContours( frame_original, rotation_contours, -1, (255,0,0), 3 )


#    for (x,y,w,h) in stamp_locations:
#        cv.rectangle( frame_original, ( int(x),int(y) ), (int(x+w), int(y+h)), (0,0,255), 1, 200 )


#    for s in stamp_locations:
#        testBits, ID = Stamp.findID( new_contours,  s)
#        for ((x,y,w,h), bit) in testBits:
#            cv.rectangle( frame_original, ( int(x),int(y) ), (int(x+w), int(y+h)), bit_colors[bit], 1, 200 )
#            cv.putText( frame_original, str(bit), (int(x), int(y)), font, 0.5, (255,255,255), 1, cv.LINE_AA )

#        cv.putText( frame_original, str(ID), (int(s[0]), int(s[1])), font, 1, (255,0,255), 2, cv.LINE_AA )


    stamp_bounds_w_angle, new_cont = Stamp.fineStampLocationsWRotation( rotation_contours )

    for (rect, angle) in stamp_bounds_w_angle:
        bits, ID = Stamp.findIDwRotation( new_cont, rect, angle )

        box = cv.boxPoints(rect)
        pnts = np.array( box, np.int32 )
#        cv.polylines(frame_original, [pnts], True, (255,0,255), 1)

        for (poly, rect_bit, bit) in bits:
#            cv.polylines(frame_original, [poly], True, bit_colors[bit], 1)

            #test code
            for cnt in new_cont:
                x,y,w,h = cv.boundingRect(cnt)
                cnt_rect = ((x+w/2,y+h/2), (w,h), 0)
                cnt_rect1 = cv.boxPoints(cnt_rect)
                cnt_rect1 = np.int0(cnt_rect1)
                cv.drawContours(frame_original, [cnt_rect1], 0, (0,0,255), 1)

                # !!!!!!!
                # HERE CONVERT POLY TO Box2D ARRRAY
                # !!!!!!!

                rec1 = cv.boxPoints(rect_bit)
                rec1 = np.int0(rec1)
                cv.drawContours(frame_original, [rec1], 0, (0,0,0), 1)


                ret, reg = Stamp.findIntersection( cnt_rect, rect_bit )
                if ret != 0:
                    cv.polylines(frame_original, [reg], True, (0,255,0), 2)
                    cv.fillPoly(frame_original, [reg], bit_colors[bit] )

#    cv.drawContours( frame_original, new_cont, -1, (255,0,0), 1 )








                                                                                                    
    rec1 = ((100,100), (50,60), 30)
    rec2 = ((120,110), (50,70), 0)
    retval, region = cv.rotatedRectangleIntersection(rec1, rec2)

    rec1 = cv.boxPoints(rec1)
    rec1 = np.int0(rec1)
    cv.drawContours(frame_original, [rec1], 0, (0,0,255), 2)

    rec2 = cv.boxPoints(rec2)
    rec2 = np.int0(rec2)
    cv.drawContours(frame_original, [rec2], 0, (0,255,255), 2)


#    print(len(region))
#    print(region)

    region = [[item[0][0], item[0][1]] for item in region]
#    print(len(region))
#    print(region)

    region = np.array( region, np.int32 )
#    print(len(region))
#    print(region)


#    print("----------------------------------------------------------------------------------------------------")
    cv.polylines(frame_original, [region], True, (0,0,0), 4)
                                                                                                    



    cv.imshow( "test2", frame_original )

    if cv.waitKey(1) & 0xFF == ord('q'):
        break








        '''
        dx,dy = 400,400
        centre = dx//2,dy//2
        img = np.zeros((dy,dx),np.uint8)
        
        # construct a long thin triangle with the apex at the centre of the image
        polygon = np.array([(0,0),(100,10),(100,-10)],np.int32)
        polygon += np.int32(centre)

        # draw the filled-in polygon and then rotate the image
        cv.fillConvexPoly(img,polygon,(255))
        M = cv.getRotationMatrix2D(centre,80,1) # M.shape =  (2, 3)
        rotatedimage = cv.warpAffine(img,M,img.shape)

        # as an alternative, rotate the polygon first and then draw it

        # these are alternative ways of coding the working example
        # polygon.shape is 3,2

        # magic that makes sense if one understands numpy arrays
        poly1 = np.reshape(polygon,(3,1,2))
        # slightly more accurate code that doesn't assumy the polygon is a triangle
        poly2 = np.reshape(polygon,(polygon.shape[0],1,2))
        # turn each point into an array of points
        poly3 = np.array([[p] for p in polygon])
        # use an array of array of points 
        poly4 = np.array([polygon])
        # more magic 
        poly5 = np.reshape(polygon,(1,3,2))

        for poly in (poly1,poly2,poly3,poly4,poly5):
            newimg = np.zeros((dy,dx),np.uint8)
            rotatedpolygon = cv.transform(poly,M)
            cv.fillConvexPoly(newimg,rotatedpolygon,(127))
            cv.imshow( "test2", newimg )
        '''
