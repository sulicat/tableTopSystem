# import the necessary packages
from __future__ import print_function
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import imutils
import cv2
import time
import sys
sys.path.append("../imageRecognition/")
import stampFuncs as Stamp
import stampFuncsOptimized as StampFast


vs = WebcamVideoStream(src=0)
vs.stream.set( cv2.CAP_PROP_FRAME_WIDTH, 1920 )
vs.stream.set( cv2.CAP_PROP_FRAME_HEIGHT, 1080 )
vs = vs.start()


start = time.time()
for i in range( 100 ):
    a = time.time()

    frame = vs.read()
    print( "\t" + str(time.time() - a) )
   # print( StampFast.stamps( frame ) )


print( "Read: " + str(time.time() - start))
