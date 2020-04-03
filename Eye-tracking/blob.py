from math import atan2, degrees
import math
import cv2
import numpy as np

FACE_PATH = "haarcascade_frontalface_default.xml"
EYE_PATH = "haarcascade_eye.xml"


class tileTracker:
    def __init__(self):
        self.history_size = 10
        self.minimum_repeats = 6

        self.history = [-1] * self.history_size
        self.last_location = -1

    def record(self, tile):
        for x in range(self.history_size - 1):
            self.history[x] = self.history[x + 1]
        self.history[self.history_size - 1] = tile
        self.check_for_change(tile)

    def check_for_change(self,tile):
        count = 0
        for x in range(self.history_size):
            if self.history[x] == tile:
                count += 1
        if(count >= self.minimum_repeats and tile != self.last_location):
            self.last_location = tile
            print(tile)

def InitHaarCascade():
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
    detector_params = cv2.SimpleBlobDetector_Params()
    detector_params.filterByArea = True
    detector_params.maxArea = 1500
    detector = cv2.SimpleBlobDetector_create(detector_params)

    return face_cascade, eye_cascade, detector

def detect_eyes(img, classifier):
    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    eyes = eye_cascade.detectMultiScale(gray_frame, 1.3, 5) # detect eyes
    width = np.size(img, 1) # get face frame width
    height = np.size(img, 0) # get face frame height
    left_eye = None
    right_eye = None
    for (x, y, w, h) in eyes:
        if y > height * 2 / 5:
            pass
        eyecenter = x + w / 2  # get the eye center
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        if eyecenter < width * 0.5:
            left_eye = img[y:y + h, x:x + w]
        else:
            right_eye = img[y:y + h, x:x + w]

    return left_eye, right_eye

def detect_faces(img, classifier):
    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    coords = face_cascade.detectMultiScale(gray_frame, 1.3, 5)
    if len(coords) > 1:
        biggest = (0, 0, 0, 0)
        for i in coords:
            if i[3] > biggest[3]:
                biggest = i
        biggest = np.array([i], np.int32)
    elif len(coords) == 1:
        biggest = coords
    else:
        return None
    for (x, y, w, h) in biggest:
        frame = img[y:y + h, x:x + w]
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return frame

def blob_process(img, threshold, detector):
    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img = cv2.threshold(gray_frame, threshold, 255, cv2.THRESH_BINARY)
    img = cv2.erode(img, None, iterations=2)
    img = cv2.dilate(img, None, iterations=4)
    img = cv2.medianBlur(img, 5)
    keypoints = detector.detect(img)

    return keypoints

def cut_eyebrows(img):
    height, width = img.shape[:2]
    eyebrow_h = int(height / 4)
    img = img[eyebrow_h:height, 0:width]  # cut eyebrows out (15 px)
    return img

def nothing(x):
    pass

def main():
    cap = cv2.VideoCapture(0)
    cv2.namedWindow('image')
    cv2.createTrackbar('threshold', 'image', 0, 255, nothing)

    tile_tracker = tileTracker()
    while True:
        _, frame = cap.read()
        face_frame = detect_faces(frame, face_cascade)
        if face_frame is not None:

            eyes = detect_eyes(face_frame, eye_cascade)
            for eye in eyes:
                if eye is not None:
                    threshold = cv2.getTrackbarPos('threshold', 'image')
                    eye = cut_eyebrows(eye)
                    keypoints = blob_process(eye, threshold, detector)
                    thresh = 0
                    while(not keypoints and thresh < 100):
                        keypoints = blob_process(eye, thresh, detector)
                        thresh += 5
                    eye = cv2.drawKeypoints(eye, keypoints, eye, (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
                    if(keypoints and len(keypoints)>0):
                        height, width = eye.shape[:2]
                        eye_box_center = [width/2, height/2]
                        pupil_point = keypoints[0].pt

                        xDiff = pupil_point[0] - eye_box_center[0]
                        yDiff = pupil_point[1] - eye_box_center[1]
                        distance = math.sqrt(xDiff * xDiff + yDiff * yDiff)

                        yDiff = -yDiff #account for the fact that the y axis moves downwards
                        angle = degrees(atan2(yDiff, xDiff))
                        result = -1
                        if (angle < 0): angle += 360;
                        if distance < 5:
                            #forward
                            result = 5
                        elif angle > 0 and angle < 25:
                            #left
                            result = 4
                        elif angle >= 25 and angle <65:
                            #top left
                            result = 1
                        elif angle >= 65 and angle <110:
                            #up
                            result = 2
                        elif angle >= 110 and angle <120:
                            #top right
                            result = 3
                        elif angle >= 120 and angle <200:
                            #right
                            result = 6
                        elif angle >= 200 and angle <245:
                            #bottom right
                            result = 9
                        elif angle >= 245 and angle <290:
                            #down
                            result = 8
                        elif angle >= 290 and angle <335:
                            #bottom left
                            result = 7
                        elif angle >=335 and angle < 360:
                            #left
                            result = 4
                        print(angle)
                        tile_tracker.record(result)
        cv2.imshow('image', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":

    face_cascade, eye_cascade, detector = InitHaarCascade()
    main()


'''
TODO
UNDERSTAND HOW TO ADJUST THE THRESHOLD
Maybe read up on how blob technique acutally works?
Need to dynamically set the threshold.... we're gonna need a calibrate function...

OBSERVATIONS
Tracking works a lot better at MODERATE LIGHTING
Make sure your eyes are not reflecting a lot of light
'''