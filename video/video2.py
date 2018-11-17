import numpy as np
import cv2 as cv
import sys
sys.path.append("../stampRecognition/templateMatch/")
import contourMatching


stampMap = cv.imread("../resources/testStamps/5_5.jpg")
cap = cv.VideoCapture(2)
stamp = contourMatching.returnStamp( stampMap, 5, 5, 7)

'''
cv.imshow( "image2", stampMap)
while 1:
    if cv.waitKey(33) == ord('q'):
        break
'''

while(True):
    ret, frame = cap.read()
    output = (frame.copy()).astype( np.uint8 )

    w, h, c = output.shape[:3]

    #mask = cv.inRange( output, (0, 20, 20), (255, 100, 100) )

    #kernel = np.ones( (2, 2),np.uint8 )
    #output = cv.erode( output, kernel, iterations = 4 )

    output = contourMatching.findStamp( output, stamp )
    cv.imshow( "image", output )

    if cv.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv.destroyAllWindows()
