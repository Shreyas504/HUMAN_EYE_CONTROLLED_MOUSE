#############################################################  LIBRARIES USED  ##########################################################################

import sys  # used in python run time env
import cv2  # real-time optimized Computer Vision library, tools
from PyQt5.QtCore import pyqtSlot  # Binding click event
from PyQt5.QtGui import QImage, QPixmap  # Image representation using pixel data
from PyQt5.QtWidgets import QDialog, QApplication  # QDialog used to take user responses and maintains GUI's flow
from PyQt5.uic import loadUi  # to load .ui file
import dlib  # modern toolkit library used in ML,IP,NA

from tkinterGUISplashScreen import endLoop
from utils import *  # utils contains the operation part of the project(ratios calculations..etc)
import numpy as np  # used for multidimensional arrays for faster calculation
import pyautogui  # used to control mouse and keyboard
from imutils import face_utils  # used for basic image processing functions like resizing..

import imutils


##############################################################  PROGRAM STARTS  #################################################################################

# class shreyas is UI class

class shreyas(QDialog):
    # default method of class (constructor)
    def __init__(self):
        super(shreyas, self).__init__()
        loadUi(r'C:\Users\shrey\Documents\FinalProjectFiles\UIFiles\main.ui', self)  # loading UI design
        self.SHOW.clicked.connect(self.onClicked)  # when start button is clicked
        self.TEXT.setText("Kindly Press 'START' to get started...")
        self.STOP.clicked.connect(self.endOP)  # when Stop button in is clicked

    # method when user click start button
    # start
    @pyqtSlot()
    def onClicked(self):
        shapepredictor = r"C:\Users\shrey\Documents\FinalProjectFiles\models\shape_predictor_68_face_landmarks.dat"  # contains facial landmarks of face
        detector = dlib.get_frontal_face_detector()  # detects the face and its landmarks
        predictor = dlib.shape_predictor(shapepredictor)  # based upon the values it predicts the next step
        (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]  # start and end points of left eye [37-42]
        (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]  # start and end points of right eye [43-48]
        (nStart, nEnd) = face_utils.FACIAL_LANDMARKS_IDXS["nose"]  # start and end points of left eye [28-36]
        (mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]  # start and end points of left eye [49-68]
        YELLOW_COLOR = (0, 255, 255)
        WINK_COUNTER = 0  # to properly maintain left click and right click
        eye_counter = 0  # for cursor movement
        MOUTH_COUNTER = 0  # for scrolling
        count = 0  # count no of cycles
        skip_frames = 2  # after every 2 frames face will be detected
        INPUT_MODE = False  # condition checker for mouse movements
        SCROLL_MODE = False  # condition checker for scrolling
        self.TEXT.setText("Video Started!!!")
        cap = cv2.VideoCapture(0)  # start webcam

        while (cap.isOpened()):
            ret, frame = cap.read()  # take video into frames and return value
            frame = cv2.flip(frame, 1)  # flip it
            frame = imutils.resize(frame, width=640, height=480)  # resizing of frame
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # conversion of color for better detection
            if (count % skip_frames == 0):  # to make system fast
                faces = detector(gray, 0)
            if ret == True:  # main operations starts from here
                print("here")
                if len(faces) > 0:
                    rect = faces[0]  # face values

                else:
                    print("no face detected")

                    continue
                count += 1
                landmarks = predictor(gray, rect)  # it determine the facial landmarks for the face region
                landmarks = face_utils.shape_to_np(
                    landmarks)  # convert the landmark (x, y)-coordinates to a NumPy array
                mouth = landmarks[mStart:mEnd]
                leftEye = landmarks[lStart:lEnd]
                rightEye = landmarks[rStart:rEnd]
                nose = landmarks[nStart:nEnd]
                temp = leftEye  # since screen is flipped
                leftEye = rightEye
                rightEye = temp
                nose_point = (nose[3, 0], nose[3, 1])
                print("here2")
                # ratios are calculated
                mar = mouth_aspect_ratio(mouth)
                leftEAR = eye_aspect_ratio(leftEye)
                rightEAR = eye_aspect_ratio(rightEye)
                ear = (leftEAR + rightEAR) / 2.0
                diff_ear = np.abs(leftEAR - rightEAR)
                # draw the shape
                leftEyeHull = cv2.convexHull(leftEye)
                rightEyeHull = cv2.convexHull(rightEye)
                mouthHull = cv2.convexHull(mouth)
                cv2.drawContours(frame, [mouthHull], -1, YELLOW_COLOR, 1)
                cv2.drawContours(frame, [leftEyeHull], -1, YELLOW_COLOR, 1)
                cv2.drawContours(frame, [rightEyeHull], -1, YELLOW_COLOR, 1)
                # left click and right click

                if diff_ear > 0.04:

                    if leftEAR < rightEAR:
                        if leftEAR < 0.19:
                            WINK_COUNTER += 1

                            if WINK_COUNTER > 2:
                                pyautogui.click(button='left')
                                self.TEXT.setText("LEFT CLICK")
                                WINK_COUNTER = 0

                    elif leftEAR > rightEAR:
                        if rightEAR < 0.19:
                            WINK_COUNTER += 1

                            if WINK_COUNTER > 2:
                                pyautogui.click(button='right')
                                self.TEXT.setText("RIGHT CLICK")
                                WINK_COUNTER = 0
                    else:
                        WINK_COUNTER = 0
                # cursor movement
                else:
                    if ear <= 0.19:
                        eye_counter += 1
                        if eye_counter > 1:
                            INPUT_MODE = not INPUT_MODE
                            eye_counter = 0
                            ANCHOR_POINT = nose_point
                    else:
                        eye_counter = 0
                # scrolling using mouth
                if mar > 0.6:
                    MOUTH_COUNTER += 1

                    if MOUTH_COUNTER > 2:
                        SCROLL_MODE = not SCROLL_MODE
                        MOUTH_COUNTER = 0
                else:
                    MOUTH_COUNTER = 0

                if INPUT_MODE:
                    self.TEXT.setText("Reading Input!")
                    x, y = ANCHOR_POINT
                    nx, ny = nose_point
                    w, h = 60, 35
                    multiple = 1
                    cv2.rectangle(frame, (x - w, y - h), (x + w, y + h), (0, 255, 0), 2)
                    cv2.line(frame, ANCHOR_POINT, nose_point, (255, 0, 0), 2)
                    dir = direction(nose_point, ANCHOR_POINT, w, h)

                    drag = 40
                    if dir == 'right':
                        pyautogui.moveRel(drag, 0)
                        self.TEXT.setText("RIGHT movement")
                    elif dir == 'left':
                        pyautogui.moveRel(-drag, 0)
                        self.TEXT.setText("LEFT movement")
                    elif dir == 'up':
                        if SCROLL_MODE:
                            pyautogui.scroll(40)
                        else:
                            pyautogui.moveRel(0, -drag)
                            self.TEXT.setText("UP movement")
                    elif dir == 'down':
                        if SCROLL_MODE:
                            pyautogui.scroll(-40)
                        else:
                            pyautogui.moveRel(0, drag)
                            self.TEXT.setText("DOWN movement")
                if SCROLL_MODE:
                    self.TEXT.setText("SCROLLING")
            self.displayImage(frame, 1)
            ch = cv2.waitKey(1)
            # to close the window


            if not ret:
                print("no camera detected")
                self.TEXT.setText("No FACE Detected...")
        if(cap.isOpened() == False):
            self.TEXT.setText("No camera detected")
        # cap.release()
        # cv2.destroyAllWindows()
        cap.release()
        cv2.destroyAllWindows()
        if ch == 27 or ch == ord('q') or ch == ord('Q'):
            cap.release()
            cv2.destroyAllWindows()
            endLoop()

    # method end
    # STOP button
    def endOP(self):
        self.close()
        
        cv2.destroyAllWindows()
        endLoop()
   

    # to display video on GUI
    def displayImage(self, img, window=1):
        qformat = QImage.Format_Indexed8
        if len(img.shape) == 3:
            if img.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        img = QImage(img, img.shape[1], img.shape[0], qformat)
        img = img.rgbSwapped()
        if window == 1:
            self.imgLabel.setPixmap(QPixmap.fromImage(img))
            self.imgLabel.setScaledContents(True)


#####################################################  EXECUTION OF PROGRAM STARTS FROM HERE  ###############################################################################

app = QApplication(sys.argv)
window = shreyas()
window.show()
try:
    sys.exit(app.exec())
except:
    cv2.destroyAllWindows()
    print('exiting')
