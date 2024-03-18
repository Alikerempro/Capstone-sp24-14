import numpy as np 
import cv2 as cv

########
### ADAPTED FROM: https://learnopencv.com/making-a-low-cost-stereo-camera-using-opencv/#individual-calibration-of-the-right-and-left-cameras-of-the-stereo-setup
########

def connectCamera(path, resX, resY):
    cap = cv.VideoCapture(path)
    if not cap.isOpened():
        return -1
    cap.set(cv.CAP_PROP_FRAME_WIDTH, resX)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, resY)
    return cap

# Set the path to the images captured by the left and right cameras
pathL = "./data/stereoL/"
pathR = "./data/stereoR/"

objectPoints = []
imagePointsL = []
imagePointsR = []


camLeft = connectCamera("/dev/v4l/by-id/usb-046d_HD_Pro_Webcam_C920_DE6EB69F-video-index0", 1280, 720)
camRight = connectCamera("/dev/v4l/by-id/usb-046d_HD_Pro_Webcam_C920_ACBF20EF-video-index0",1280, 720)

# Termination criteria for refining the detected corners
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
 
objp = np.zeros((9*6,3), np.float32)
objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)


for i in range(0,11):
    while True:
        
        cv.namedWindow('imgL',cv.WINDOW_NORMAL)
        cv.namedWindow('imgR',cv.WINDOW_NORMAL)
        ret, imgL = camLeft.read()
        ret, imgR = camRight.read()
        
        grayL = cv.cvtColor(imgL, cv.COLOR_BGR2GRAY)
        grayR = cv.cvtColor(imgR, cv.COLOR_BGR2GRAY)
        
        cv.imshow("imgL", imgL)
        cv.imshow("imgR", imgR)
            
        cv.resizeWindow("imgL", 600, 600)
        cv.resizeWindow("imgR", 600, 600)
        
        if cv.waitKey(3) != -1:
            cv.destroyAllWindows()
            print("Next picture!")
            
            outputL = imgL.copy()
            outputR = imgR.copy()
            
            retR, cornersR =  cv.findChessboardCorners(outputR,(9,6),None)
            retL, cornersL = cv.findChessboardCorners(outputL,(9,6),None)
            
            if retR and retL:
                objectPoints.append(objp)
                cv.cornerSubPix(grayL,cornersL,(11,11),(-1,-1),criteria)
                cv.cornerSubPix(grayR,cornersR,(11,11),(-1,-1),criteria)
                cv.drawChessboardCorners(outputL,(9,6),cornersL,retL)
                cv.drawChessboardCorners(outputR,(9,6),cornersR,retR)
            
                imagePointsL.append(cornersL)
                imagePointsR.append(cornersR)
                
            cv.imshow("left view", outputL)
            cv.imshow("right view", outputR)
            
            cv.resizeWindow("left view", 600, 600)
            cv.resizeWindow("right view", 600, 600)
            
            cv.waitKey(0)
            
            cv.destroyAllWindows()
            break

# Calibrating left camera
retL, mtxL, distL, rvecsL, tvecsL = cv.calibrateCamera(objectPoints,imagePointsL,grayL.shape[::-1],None,None)
hL,wL= grayL.shape[:2]
new_mtxL, roiL= cv.getOptimalNewCameraMatrix(mtxL,distL,(wL,hL),1,(wL,hL))
 
# Calibrating right camera
retR, mtxR, distR, rvecsR, tvecsR = cv.calibrateCamera(objectPoints,imagePointsR,grayR.shape[::-1],None,None)
hR,wR= grayR.shape[:2]
new_mtxR, roiR= cv.getOptimalNewCameraMatrix(mtxR,distR,(wR,hR),1,(wR,hR))

flags = 0
flags |= cv.CALIB_FIX_INTRINSIC
# Here we fix the intrinsic camara matrixes so that only Rot, Trns, Emat and Fmat are calculated.
# Hence intrinsic parameters are the same 
 
criteria_stereo= (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# This step is performed to transformation between the two cameras and calculate Essential and Fundamenatl matrix
retS, new_mtxL, distL, new_mtxR, distR, Rot, Trns, Emat, Fmat = cv.stereoCalibrate(objectPoints, imagePointsL, imagePointsR, new_mtxL, distL, new_mtxR, distR, grayL.shape[::-1], criteria_stereo, flags)

rectify_scale= 1
rect_l, rect_r, proj_mat_l, proj_mat_r, Q, roiL, roiR= cv.stereoRectify(new_mtxL, distL, new_mtxR, distR, grayL.shape[::-1], Rot, Trns, rectify_scale,(0,0))

Left_Stereo_Map= cv.initUndistortRectifyMap(new_mtxL, distL, rect_l, proj_mat_l,
                                             grayL.shape[::-1], cv.CV_16SC2)
Right_Stereo_Map= cv.initUndistortRectifyMap(new_mtxR, distR, rect_r, proj_mat_r,
                                              grayR.shape[::-1], cv.CV_16SC2)

print(new_mtxL)

cv_file = cv.FileStorage("stereo_calibration.xml", cv.FILE_STORAGE_WRITE)
cv_file.write("Left_Stereo_Map_x",Left_Stereo_Map[0])
cv_file.write("Left_Stereo_Map_y",Left_Stereo_Map[1])
cv_file.write("Right_Stereo_Map_x",Right_Stereo_Map[0])
cv_file.write("Right_Stereo_Map_y",Right_Stereo_Map[1])
cv_file.write("New_Mat_L", new_mtxL)
cv_file.release()

exit()