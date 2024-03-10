import numpy as np
import cv2 as cv
import pickle 
from matplotlib import pyplot as plt

def connectCamera(path, resX, resY):
    cap = cv.VideoCapture(path)
    if not cap.isOpened():
        return -1
    cap.set(cv.CAP_PROP_FRAME_WIDTH, resX)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, resY)
    return cap
    
def readFrame(cap):
    ret, frame = cap.read()
    if not ret:
        return -1
    return frame

###########
##### START
###########

### VALUES

lambdaVal = 8000
sigmaVal = 2.0
visMult = 1

windowSize = 7
minDisp = 16
nDispFactor = 14
numDisp = 16*nDispFactor-minDisp 

baseline = 97 #Distance between cameras in mm

### CODE

cv_file = cv.FileStorage("stereo_calibration.xml", cv.FILE_STORAGE_READ)

LeftStereo = [cv_file.getNode("Left_Stereo_Map_x").mat(), cv_file.getNode("Left_Stereo_Map_y").mat()]
RightStereo = [cv_file.getNode("Right_Stereo_Map_x").mat(), cv_file.getNode("Right_Stereo_Map_y").mat()]
NewMatL = cv_file.getNode("New_Mat_L").mat()
focalLength = (NewMatL[0][0] + NewMatL[1][1])/2

cv_file.release()

leftCam = connectCamera("/dev/video4", 1280, 720)
rightCam = connectCamera("/dev/video2",1280, 720)


stereo = cv.StereoSGBM.create(minDisparity=minDisp,
                              numDisparities = numDisp, 
                              blockSize = windowSize,
                              P1 = 8*3*windowSize**2,
                              P2=32*3*windowSize**2,
                              disp12MaxDiff=1,
                              uniquenessRatio=15,
                              speckleWindowSize=0,
                              speckleRange=2,
                              preFilterCap=63,
                              mode=cv.STEREO_SGBM_MODE_SGBM_3WAY)
stereoR = cv.ximgproc.createRightMatcher(stereo)

wlsFilter = cv.ximgproc.createDisparityWLSFilter(stereo)
wlsFilter.setLambda(lambdaVal)
wlsFilter.setSigmaColor(sigmaVal)


while True:

    imgLc = readFrame(leftCam)
    imgRc = readFrame(rightCam)

    cv.normalize(imgLc, imgLc, 0, 255, cv.NORM_MINMAX)
    cv.normalize(imgRc, imgRc, 0, 255, cv.NORM_MINMAX)

    #imgL = cv.resize(imgL, (0,0), fx=0.5, fy=0.5, 
    #               interpolation = cv.INTER_LINEAR_EXACT)
    #imgR = cv.resize(imgR, (0,0), fx=0.5, fy=0.5, 
    #               interpolation = cv.INTER_LINEAR_EXACT)

    imgLc= cv.remap(imgLc,LeftStereo[0],LeftStereo[1], cv.INTER_LANCZOS4, cv.BORDER_CONSTANT, 0)
    imgRc= cv.remap(imgRc,RightStereo[0],RightStereo[1], cv.INTER_LANCZOS4, cv.BORDER_CONSTANT, 0)

    imgL = cv.cvtColor(imgLc, cv.COLOR_BGR2GRAY)
    imgR = cv.cvtColor(imgRc, cv.COLOR_BGR2GRAY)

    disparityL = stereo.compute(imgL, imgR)#.astype(np.float32) / 16.0
    disparityR = stereoR.compute(imgR, imgL)#.astype(np.float32) / 16.0

    filteredDisp = disparityL.copy()
    wlsFilter.filter(disparityL, imgL, filteredDisp, disparityR)

    #confMap = wlsFilter.getConfidenceMap()
    #solvedL = cv.ximgproc.fastBilateralSolverFilter(imgLc, disparityL, confMap/255)
    #solvedFL = cv.ximgproc.fastBilateralSolverFilter(imgLc, filteredDisp, confMap/255)

    filteredDispVis = cv.ximgproc.getDisparityVis(filteredDisp, visMult)

    distanceMap = (focalLength*baseline + 0.)/filteredDisp

    depthMin = 100.0 # Threshold for SAFE distance (in cm)
    
    # Mask to segment regions with depth less than threshold
    mask = cv.inRange(distanceMap,10,depthMin)

    outputCanvas = imgLc.copy()

    # Check if a significantly large obstacle is present and filter out smaller noisy regions
    if np.sum(mask)/255.0 > 0.01*mask.shape[0]*mask.shape[1]:
        # Contour detection 
        contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        cnts = sorted(contours, key=cv.contourArea, reverse=True)
        
        for contour in cnts:
            # Check if detected contour is significantly large (to avoid multiple tiny regions)
            if cv.contourArea(contour) > 0.01*mask.shape[0]*mask.shape[1]:
                x,y,w,h = cv.boundingRect(cnts[0])
    
                # finding average depth of region represented by the largest contour 
                mask2 = np.zeros_like(mask)
                cv.drawContours(mask2, cnts, 0, (255), -1)
            
                # Calculating the average depth of the object closer than the safe distance
                depth_mean, _ = cv.meanStdDev(distanceMap, mask=mask2)
                
                # Display warning text
                cv.putText(outputCanvas, "WARNING !", (x+5,y-40), 1, 2, (0,0,255), 2, 2)
                cv.putText(outputCanvas, "Object at", (x+5,y), 1, 2, (100,10,25), 2, 2)
                cv.putText(outputCanvas, "%.2f cm"%depth_mean, (x+5,y+40), 1, 2, (100,10,25), 2, 2)
                cv.drawContours(outputCanvas, [contour], -1, (36, 255, 12), thickness=5)
    else:
        cv.putText(outputCanvas, "SAFE!", (100,100),1,3,(0,255,0),2,3)
    
    cv.imshow('frame',outputCanvas)
    if cv.waitKey(1) > -1:
        cv.destroyAllWindows()
        break