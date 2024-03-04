import numpy as np
import cv2 as cv

pixWidthTop  = 1034
pixHeightMin = 560
pixWidthBot  = 1280

imgX = 1280
imgY = 720

cap = cv.VideoCapture("/dev/video2")
if not cap.isOpened():
    print("Cannot open camera")
    exit()

cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)
    
width  = cap.get(3)  # float `width`
height = cap.get(4)  # float `height`

print("Width is " + str(width) + " height is " + str(height))
    
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    
    # Our operations on the frame come here
    if not (pixHeightMin == -1):
        cv.line(frame, (imgX, imgY), (imgX, pixHeightMin),(0,0,255), 5)
        cv.line(frame, (imgX, pixHeightMin), ((int(imgX/2)+int(pixWidthTop/2)), 0),(0,0,255), 5)
        cv.line(frame, (0, imgY), (0, pixHeightMin),(0,0,255), 5)
        cv.line(frame, (0, pixHeightMin), ((int(imgX/2)-int(pixWidthTop/2)), 0),(0,0,255), 5)

    # Display the resulting frame
    cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()