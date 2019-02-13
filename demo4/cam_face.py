import cv2
import time
from picamera import PiCamera
from picamera.array import PiRGBArray

CAMERA_RESOLUTION = (1280, 720)

camera = PiCamera()
camera.resolution = CAMERA_RESOLUTION
rawCapture = PiRGBArray(camera)

time.sleep(0.5)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

camera.capture(rawCapture, format="bgr")
img_color = rawCapture.array

img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)

# Tuloksena kasvojen sijainti muodossa (x,y,width,height)
faces = face_cascade.detectMultiScale(img_gray, 1.3, 5)

for (x,y,w,h) in faces:
    img = cv2.rectangle(img_color,(x,y),(x+w,y+h),(255,0,0),2)

cv2.imwrite('naama.jpg', img)