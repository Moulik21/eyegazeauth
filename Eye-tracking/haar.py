import numpy as np
import numpy.ma as ma
import cv2

FACE_CASCADE = 'haarcascade_frontalface_default.xml'
EYE_CASCADE = 'haarcascade_eye.xml'

class haar_cascade:
    
    def __init__(self):
        #https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
        self._face_cascade = cv2.CascadeClassifier(FACE_CASCADE)
        #https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
        self._eye_cascade = cv2.CascadeClassifier(EYE_CASCADE)

    #Returns True if eye1 is the inner most box:
    #Inner most box is defined as the smallest box around a particular eye
    def innerBox(self, eye1, eye2):
        #eye_format = (topleft_point, bottomright_point)
        if(eye1[0][0] > eye2[1][0] or eye2[0][0] > eye1[1][0]):
            return False
        if (eye1[0][1] > eye2[1][1] or eye2[0][1] > eye1[1][1]):
            return False
        area1 = (eye1[1][0] - eye1[0][0]) * (eye1[1][1] - eye1[0][1])
        area2 = (eye2[1][0] - eye2[0][0]) * (eye2[1][1] - eye2[0][1])
        return area1 < area2

    def filterEyes(self, eyes):
        if (len(eyes) <= 2):
            return eyes

        result = []
        for eye in eyes:
            for eye2 in eyes:
                if (eye != eye2):
                    eye1_top_left = (eye[0], eye[1])
                    eye1_bottom_right = (eye[0] + eye[2], eye[1]+eye[2])
                    eye2_top_left = (eye2[0], eye2[1])
                    eye2_bottom_right = (eye2[0] + eye2[2], eye2[1]+eye2[2])
                    if(self.innerBox((eye1_top_left, eye1_bottom_right), (eye2_top_left, eye2_bottom_right))):
                        result.append(eye)

        return result

    def cut_eyebrows(self, eye):
        height, width = eye.shape[:2]

        '''
            From OpenCV : eyebrows always take ~25% of the eye 'frame' starting from the top        
        '''
        eyebrow_h = int(height / 4)
        eye = eye[eyebrow_h:height, 0:width]

        return eye

    def pupil_detection(self, eye, detector, threshold):
        '''
            did a series of erosions and dilations to reduce the “noise” we had.
            That trick is commonly used in different CV scenarios, but it works well
            in our situation. After that, we blurred the image so it’s smoother.
        '''
        gray_frame = cv2.cvtColor(eye, cv2.COLOR_BGR2GRAY)
        _, eye = cv2.threshold(gray_frame, threshold, 255, cv2.THRESH_BINARY)
        eye = cv2.erode(eye, None, iterations=2)  # 1
        eye = cv2.dilate(eye, None, iterations=4)  # 2
        eye = cv2.medianBlur(eye, 5)  # 3
        keypoints = detector.detect(eye)
        return keypoints

    def nothing(x):
        pass

    def Run(self):
        """Spawns a window and records using primary webcam
        """
        #https://stackoverflow.com/questions/34588464/python-how-to-capture-image-from-webcam-on-click-using-opencv
        cam = cv2.VideoCapture(0)

        cv2.namedWindow("img")
        cv2.createTrackbar('threshold', 'img', 0, 255, self.nothing)

        img_counter = 0

        detector_params = cv2.SimpleBlobDetector_Params()
        detector_params.filterByArea = True
        detector_params.maxArea = 1500
        detector = cv2.SimpleBlobDetector_create(detector_params)

        while True:
            ret, frame = cam.read()

            gray = cv2.cvtColor(cv2.GaussianBlur(frame,(5,5),0), 0)
            faces = self._face_cascade.detectMultiScale(gray, 1.3, 5)
            cx, cy, cw, ch = 0, 0, 0, 0

            # Draw rectange around eyes and face
            roi_gray = np.array([])
            for (x,y,w,h) in faces:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]

                eyes = self._eye_cascade.detectMultiScale(roi_gray)
                eyes_array = []
                for (ex,ey,ew,eh) in eyes:
                    eyes_array.append([ex,ey,ew,eh])
                filtered_eyes = self.filterEyes(eyes_array)
                for eye in filtered_eyes:
                    ex, ey, ew, eh = eye[0], eye[1], eye[2], eye[3]
                    cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
                    cx, cy, cw, ch = ex, ey, ew, eh
                    threshold = cv2.getTrackbarPos('threshold', 'img') #dynamically get threshold value
                    eye_frame = roi_color[ey : ey+eh, ex : ex+ew]
                    eye_frame = self.cut_eyebrows(eye_frame)
                    keypoints = self.pupil_detection(eye_frame, detector, threshold)

                    #draw pupil keypoints
                    cv2.drawKeypoints(eye_frame, keypoints, eye_frame, (0, 0, 255),
                                            cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

            
            cv2.imshow('img',frame)

            # Stop Recording
            if not ret:
                break
            k = cv2.waitKey(1)

            # Save the image or exit
            if k%256 == 27:
                # ESC pressed
                print("Escape hit, closing...")
                break
            elif k%256 == 32:
                # SPACE pressed
                img_name = "opencv_frame_{}.png".format(img_counter)
                cv2.imwrite(img_name, roi_gray[cy:cy+ch, cx:cx+cw])
                print("{} written!".format(img_name))
                img_counter += 1

        cam.release()

        cv2.destroyAllWindows()

class Gradient:
    """Computes gradient of images
    """
    def ComputeMagnitude(self, img, threshold=0.3):
        """Recommend applying the gaussian filter before processing.
        
        Arguments:
            img {Numpy Array} -- Gray Image
        
        Keyword Arguments:
            threshold {float} -- Used to remove unwanted magnitudes(default: {0.3})
        
        Returns:
            [Numpy Array, Numpy Array] -- Returns magnitude and direction
        """
        # Output dtype = cv.CV_64F. Then take its absolute and convert to cv.CV_8U
        sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0) # Find x and y gradients
        sobely = cv2.Sobel(img ,cv2.CV_64F, 0, 1)

        # Find magnitude and angle
        magnitude = np.sqrt(sobelx**2.0 + sobely**2.0)
        angle = np.arctan2(sobely, sobelx) * (180 / np.pi)

        # Compute mean and std dev for magnitude
        mean = np.mean(magnitude)
        std = np.std(magnitude)
        index = magnitude < (threshold * std + mean)
        magnitude[index] = 0.0

        # Normalize the matrix
        abs_mag = cv2.normalize(magnitude, 0, 255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_64F)
        return abs_mag, angle

    def FindPupil(self, magnitude, angle):
        pass

        

if __name__ == "__main__":
    hc = haar_cascade()
    hc.Run()
    

    # # ---------------------------------------
    # gr = Gradient()
    # # img = cv2.imread("C:\\Users\\crazy\\Documents\\490\\opencv_frame_0.png", 1)
    # # opencv_frame_0.png
    # img = cv2.imread("test_eye.png")
    # img = cv2.GaussianBlur(img,(5,5),0)
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # mag, ang = gr.ComputeMagnitude(gray)
    # print(mag.shape)
    # cv2.imshow("magnitude",mag)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    #
    # print(mag.shape)
