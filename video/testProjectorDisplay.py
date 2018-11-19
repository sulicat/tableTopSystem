import pygame
import numpy as np
import cv2 as cv
import sys
sys.path.append("../stampRecognition/")
import recognize
import imutils


stampMap = cv.imread("../resources/testStamps/5_5.jpg")
cap = cv.VideoCapture(2)
stamp = recognize.returnStamp( stampMap, 5, 5, 3)



while(True):
    ret, frame = cap.read()
    frame = imutils.resize(frame, width=3000)

    output = (frame.copy()).astype( np.uint8 )
    w, h, c = output.shape[:3]

    #kernel = np.ones( (3, 3), np.uint8 )
    #mask = cv.erode( output, kernel, iterations = 8 )
    mask = cv.inRange( output, (0, 200, 0), (255, 255, 255) )

    #output = contourMatching.findStamp( mask, stamp )



    matches, ctIm, ctStamp = recognize.findStamp( output, stamp )
    temp_out = output.copy()
    temp_stamp = stamp.copy()
    cv.drawContours( temp_out, ctIm, -1, (255,0,0), 3 )
    cv.drawContours( temp_stamp, ctStamp, -1, (255,0,0), 3 )


    for (x,y,w,h) in matches:
            cv.rectangle( temp_out, ( int(x),int(y) ), (int(x+w), int(y+h)), (0,0,255), 3, 200 )

    temp_out = imutils.resize(temp_out, width=800)
    cv.imshow( "image", temp_out )
    cv.imshow( "stamp", temp_stamp )
    #cv.imshow( "image2", matches )

    if cv.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv.destroyAllWindows()



'''
pygame.init()
screen = pygame.display.set_mode((1800, 1200))
done = False
while not done:

        screen.fill((255,255,255))


        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True


        pygame.display.flip()
'''
