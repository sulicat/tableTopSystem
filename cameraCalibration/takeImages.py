import cv2 as cv
import time
import threading

cap = cv.VideoCapture(2)

image_counter = 0


while( True ):
    ret, frame = cap.read()

    cv.imshow( "image", frame )


    key = cv.waitKey(1)
    if key & 0xFF == ord('q'):
        break
    elif key & 0xFF == ord('n'):
        cv.imwrite("images/"+str(image_counter)+".jpg", frame)
        image_counter += 1





