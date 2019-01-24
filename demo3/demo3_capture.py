import datetime
from picamera import PiCamera
import time

camera = PiCamera()
time.sleep(1)

file_name = u'/home/pi/dev/img/cron_{:%y-%m-%d_%H-%M}.jpg'.format(datetime.datetime.now())
print(file_name)

camera.capture(file_name)

camera.close()