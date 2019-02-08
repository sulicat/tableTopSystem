import cv2 as cv
import time
import threading
import imutils

cap = cv.VideoCapture(0)
cap.set( cv.CAP_PROP_FRAME_WIDTH,  1920 )
cap.set( cv.CAP_PROP_FRAME_HEIGHT, 1080 )


image_counter = 0


while( True ):
    ret, frame = cap.read()

    show = imutils.resize(frame, width=1000)
    cv.imshow( "image", show )




    key = cv.waitKey(1)
    if key & 0xFF == ord('q'):
        break
    elif key & 0xFF == ord('n'):
        print("image")
        cv.imwrite("raspi_images/A_"+str(image_counter)+".jpg", frame)
        image_counter += 1





