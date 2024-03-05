import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import matplotlib as mpl

pixWidthTop  = 1034
pixHeightMin = 560
pixWidthBot  = 1280

imgX = 1280
imgY = 720

cap = cv.VideoCapture("/dev/video2")
if not cap.isOpened():
    print("Cannot open camera")
    exit()

cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

print("Width is " + str(cap.get(3)) + " height is " + str(cap.get(4)))
    
cap2 = cv.VideoCapture("/dev/video0")
if not cap2.isOpened():
    print("Cannot open camera 2")
    exit()
    
cap2.set(cv.CAP_PROP_FRAME_WIDTH, 640)
cap2.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

print("Width2 is " + str(cap2.get(3)) + " height2 is " + str(cap2.get(4)))
    
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    ret2, frame2 = cap2.read()
    
    frame_new=cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame2_new=cv.cvtColor(frame2, cv.COLOR_BGR2GRAY)
    
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    if not ret2:
        print("Can't receive frame2 (stream end?). Exiting ...")
        break
    
    stereo = cv.StereoBM.create(numDisparities=16, blockSize=15)
    disparity = stereo.compute(frame_new,frame2_new)

    # Display the resulting frame
    # cv.imshow('frame', disparity)
    cv.imshow('frame',disparity)
    
    if cv.waitKey(1) == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()