import numpy as np
import cv2

FACE_CASCADE = 'haarcascade_frontalface_default.xml'
EYE_CASCADE = 'haarcascade_eye.xml'

# class haar_cascade():
    
#     def __init__(self):
#         #https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
#         self._face_cascade = cv2.CascadeClassifier(FACE_CASCADE)
#         #https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
#         self._eye_cascade = cv2.CascadeClassifier(EYE_CASCADE)

#     def detect_faces(img):
#         gray = cv2.cvtColor(img, 0)
#         return self._face_cascade.detectMultiScale(gray, 1.3, 5)

#     def detect_eyes(img):
#         gray = cv2.cvtColor(img, 0)
#         faces = self.detect_faces(img)
#         for x, y, w, h in faces:
#             roi_gray = gray[y:y+h, x:x+w]
#             roi_color = img[y:y+h, x:x+w]
            
#             eyes = self._eye_cascade.detectMultiScale(roi_gray)
#             for ex, ey, ew, eh in eyes:
#                 cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
#                 cx, cy, cw, ch = ex, ey, ew, eh


        
# class tracker():
#     pass

# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades

#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

#https://stackoverflow.com/questions/34588464/python-how-to-capture-image-from-webcam-on-click-using-opencv

cam = cv2.VideoCapture(0)

cv2.namedWindow("test")

img_counter = 0

while True:
    ret, frame = cam.read()

    gray = cv2.cvtColor(frame, 0)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    cx, cy, cw, ch = 0, 0, 0, 0

    # Draw rectange around eyes and face
    roi_gray = np.array([])
    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            cx, cy, cw, ch = ex, ey, ew, eh
    
    
    cv2.imshow('img',frame)

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