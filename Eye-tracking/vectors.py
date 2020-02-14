import cv2
import numpy as np

class pupil_dectector():

    def compute_gradient(self, image):
        # OpenCV tutorial
        # https://docs.opencv.org/3.4/d2/d2c/tutorial_sobel_derivatives.html

        ddepth = cv.CV_16S

        # Remove noise from image
        blur = cv2.GaussianBlur(image, (3,3), 0)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                
        sobel_x = cv2.Sobel(image, ddepth, 1, 0, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
        sobel_y = cv2.Sobel(image, ddepth, 0, 1, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)

        # Convert image depth back to CV_8S
        abs_grad_x = cv.convertScaleAbs(grad_x)
        abs_grad_y = cv.convertScaleAbs(grad_y)