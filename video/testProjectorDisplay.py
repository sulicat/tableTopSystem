import pygame
import numpy as np
import cv2 as cv
import sys
sys.path.append("../stampRecognition/templateMatch/")
import contourMatching


stampMap = cv.imread("../resources/testStamps/5_5.jpg")
cap = cv.VideoCapture(0)
stamp = contourMatching.returnStamp( stampMap, 5, 5, 7)



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
