import numpy as np
import cv2
from math import atan2, degrees

FACE_PATH = "haarcascade_frontalface_default.xml"
EYE_PATH = "haarcascade_eye.xml"

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
                        yDiff = eye_box_center[1] - pupil_point[1]
                        angle = degrees(atan2(yDiff, xDiff))
                        if angle > 0 and angle < 25:
                            print("right")
                        elif angle >= 25 and angle <65:
                            print("top right")
                        elif angle >= 65 and angle <110:
                            print("up")
                        elif angle >= 110 and angle <120:
                            print("top left")
                        elif angle >= 120 and angle <200:
                            print("left")
                        elif angle >= 200 and angle <245:
                            print("bottom left")
                        elif angle >= 245 and angle <290:
                            print("down")
                        elif angle >= 290 and angle <335:
                            print("bottom right")
                        elif angle >=335:
                            print("right")


                        a = ""
                        b=""
                        if (xDiff > 10):
                            a = "left"
                        elif (xDiff < -10):
                            a = "right"
                        if (yDiff > 10):
                            b = "up"
                        elif (yDiff < -10):
                            b = "down"
                        print("" + a + "   " + b + "")
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