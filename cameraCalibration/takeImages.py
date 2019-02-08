import cv2 as cv
import time
import threading

cap = cv.VideoCapture(0)
cap.set( cv.CAP_PROP_FRAME_WIDTH, 1080 )
cap.set( cv.CAP_PROP_FRAME_HEIGHT, 720 )


image_counter = 0


while( True ):
    ret, frame = cap.read()

    cv.imshow( "image", frame )


    key = cv.waitKey(1)
    if key & 0xFF == ord('q'):
        break
    elif key & 0xFF == ord('n'):
        print("image")
        cv.imwrite("raspi_images/"+str(image_counter)+".jpg", frame)
        image_counter += 1





