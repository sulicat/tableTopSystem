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

cap = cv.VideoCapture(2)

ACTIVE_AREA = [ [630, 160],
                [1310, 170],
                [560, 850],
                [1380, 840] ]

CAMERA_CALIB_MTX = np.array(
    [[1.99362428e+04, 0.00000000e+00, 9.07566367e+02],
     [0.00000000e+00, 7.92819569e+03, 5.07551013e+02],
     [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]]
, np.float)

CAMERA_CALIB_DIST = np.array(
    [[-1.23408977e+01,  1.48506849e+02,  1.96173243e-01,  2.73137122e-02,   2.45014575e+00]]
                              , np.float)


while( True ):

    ret, frame_original = cap.read()
    rows, cols, d = frame_original.shape
    M = cv.getRotationMatrix2D((cols/2,rows/2), 180, 1)
    # NOTE THIS IS CROPPING THE IMAGE --- FIX ME LAZY
    #frame_original = cv.warpAffine(frame_original, M, (cols,rows))


    h,  w = frame_original.shape[:2]
    newcameramtx, roi = cv.getOptimalNewCameraMatrix( CAMERA_CALIB_MTX, CAMERA_CALIB_DIST, (w,h), 1, (w,h))
    # undistort
    mapx, mapy = cv.initUndistortRectifyMap(CAMERA_CALIB_MTX, CAMERA_CALIB_DIST, None, newcameramtx, (w,h), 5)
    frame_calib = cv.remap(frame_original, mapx,mapy, cv.INTER_LINEAR)



    pts_from = np.float32( ACTIVE_AREA )


    to_width = 1000
    to_height = 1000

    pts_to = np.float32([ [0,0],
                          [cols,0],
                          [0,rows],
                          [cols, rows]
    ])


    #rect = order_points(ACTIVE_AREA)
    (tl, tr, bl, br) = ACTIVE_AREA

    # compute the width of the new image, which will be the
    # maximum distance between bottom-right and bottom-left
    # x-coordiates or the top-right and top-left x-coordinates
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    # compute the height of the new image, which will be the
    # maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))


    pts_to = np.array([
	[0, 0],
	[maxWidth - 1, 0],
        [0, maxHeight - 1],
	[maxWidth - 1, maxHeight - 1]], dtype = "float32")


    M = cv.getPerspectiveTransform(pts_from, pts_to)
    frame_skew = cv.warpPerspective( frame_calib, M, (maxWidth, maxHeight))
    #frame_skew = imutils.resize(frame_skew, width=1000, height=1000)



    for pnt in ACTIVE_AREA:
        cv.circle(frame_calib, (pnt[0], pnt[1]), 5, (255,0,255), -1)

    for pnt in ACTIVE_AREA:
        cv.circle(frame_skew, (pnt[0], pnt[1]), 5, (255,255, 0), -1)


    #cv.imshow( "ior fix", frame_calib )
    cv.imshow( "test", frame_skew )

    if cv.waitKey(1) & 0xFF == ord('q'):
        break
