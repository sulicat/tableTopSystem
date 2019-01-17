import pygame
import numpy as np
import cv2 as cv
import sys
sys.path.append("../stampRecognition/")
import recognize
import imutils


stampMap = cv.imread("../resources/testStamps/5_5.jpg")
cap = cv.VideoCapture(2)
stamp1 = recognize.returnStamp( stampMap, 5, 5, 1)
stmap1 = imutils.resize(stamp1, width=50)
stamp2 = recognize.returnStamp( stampMap, 5, 5, 2)
stamp15 = recognize.returnStamp( stampMap, 5, 5, 15)



while(True):
    ret, frame = cap.read()
    frame = imutils.resize(frame, width=3000)

    output = (frame.copy()).astype( np.uint8 )
    w, h, c = output.shape[:3]

    kernel = np.ones( (5, 5), np.uint8 )
    mask = cv.inRange( output, (0, 200, 0), (255, 255, 255) )
    tempMask = mask.copy()
    mask = cv.erode( mask, kernel, iterations = 2)
#    mask2 = cv.inRange( output, (180, 180, 180), (255, 255, 255) )
#    mask2 = 255 - mask2
#    mask = cv.bitwise_and(mask,mask2)
    #mask = mask2


    matches1, ctIm1, ctStamp1 = recognize.findStamp( mask, stamp1 )
    matches2, ctIm2, ctStamp2 = recognize.findStamp( mask, stamp2 )
    matches15, ctIm15, ctStamp15 = recognize.findStamp( mask, stamp15 )
    temp_out = output.copy()
    cv.drawContours( temp_out, ctIm1, -1, (255,0,0), 3 )



    for (x,y,w,h) in matches1:
            cv.rectangle( temp_out, ( int(x),int(y) ), (int(x+w), int(y+h)), (0,0,255), 5, 200 )

    '''
    for (x,y,w,h) in matches2:
            cv.rectangle( temp_out, ( int(x),int(y) ), (int(x+w), int(y+h)), (0,255,255), 3, 200 )

    for (x,y,w,h) in matches15:
            cv.rectangle( temp_out, ( int(x),int(y) ), (int(x+w), int(y+h)), (255,0,255), 3, 200 )
    '''

    #temp_out = imutils.resize(temp_out, width=800)
    #frame = imutils.resize(frame, width=800)
    #mask = imutils.resize(mask, width=800)
    #tempMask = imutils.resize(tempMask, width=800)


    #cv.imshow( "frame", frame )
    #cv.imshow( "mask", mask )
    #cv.imshow( "mask1", tempMask )
    #cv.imshow( "mask2", temp_out )

    cv.imshow( "image", stamp2 )
    tempStamp = stamp2.copy()
    cv.drawContours( tempStamp, ctStamp2, -1, (255,0,0), 3 )
    cv.imshow( "image1", tempStamp )


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
