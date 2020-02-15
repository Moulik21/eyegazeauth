import cv2
import numpy as np

class pupil_dectector():

    def compute_gradient(self, image):
        # OpenCV tutorial
        # https://docs.opencv.org/3.4/d2/d2c/tutorial_sobel_derivatives.html

        ddepth = cv2.CV_16S

        # Remove noise from image
        blur = cv2.GaussianBlur(image, (3,3), 0)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                
        grad_x = cv2.Sobel(image, ddepth, 1, 0, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
        grad_y = cv2.Sobel(image, ddepth, 0, 1, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)

        # Convert image depth back to CV_8S
        abs_grad_x = cv2.convertScaleAbs(grad_x)
        abs_grad_y = cv2.convertScaleAbs(grad_y)

        magnitude = ((abs_grad_x * abs_grad_x) + (abs_grad_y * abs_grad_y)) ** 0.5
        direction = np.arctan2(abs_grad_y, abs_grad_x)

        return magnitude, direction

if __name__ == '__main__':
    image = cv2.imread('C:\\Users\\crazy\\Documents\\490\\eyegazeauth\\Eye-tracking\\test_eye.png')


    cv2.imshow('test',image)


    # pd = pupil_dectector()
    # magnitude, direction = pd.compute_gradient(image)
    # cv2.imshow(magnitude)
    # cv2.waitkey(0)
    # cv2.destroyAllWindows()
