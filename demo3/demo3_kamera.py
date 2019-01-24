from picamera import PiCamera
import RPi.GPIO as GPIO
import time
import sys

# Globals
# =============================

MOVEMENT_SENSOR = 20
RED_LED = 5
GREEN_LED = 6

CAMERA_RESOLUTION = (1280, 720)
CAMERA_RESIZE = (320, 240)

CYCLE_TIME = 0.1 # s
MIN_TIME_STEP = 0.001 # s

OUTPUT_FILE = '/home/pi/dev/img/capture{:04d}.jpg'

camera = PiCamera()
camera.resolution = CAMERA_RESOLUTION

img_counter = 0

# Setup
# ==============================
GPIO.setmode(GPIO.BCM)

GPIO.setup(MOVEMENT_SENSOR, GPIO.IN)
GPIO.setup(RED_LED, GPIO.OUT, initial=0)
GPIO.setup(GREEN_LED, GPIO.OUT, initial=0)

def takePicture():
    global img_counter
    camera.capture(OUTPUT_FILE.format(img_counter))
    img_counter += 1

# Events
# ==============================
def motionEvent(ch):
    movement = GPIO.input(MOVEMENT_SENSOR)
    GPIO.output(GREEN_LED, movement)
    if movement == 1:
        takePicture()



GPIO.add_event_detect(MOVEMENT_SENSOR, GPIO.BOTH, callback=motionEvent, bouncetime=100)


# Cyclic task
# ==============================
def cyclic(cycle):
    pass


last_t = time.time()
accu_t = 0
running = True

# MAIN LOOP
# ==============================
while running:
    try:
        now = time.time()
        accu_t += now - last_t
        last_t = now

        if accu_t > CYCLE_TIME:
            # run cyclic task
            cyclic(CYCLE_TIME)
            accu_t -= CYCLE_TIME
        else:
            remaining = CYCLE_TIME - accu_t
            idle_t = remaining - MIN_TIME_STEP
            if idle_t < MIN_TIME_STEP:
                idle_t = MIN_TIME_STEP
            time.sleep(idle_t)
            # print('Accu: {} idle {}'.format(accu_t, idle_t))

    except KeyboardInterrupt:
        print(u'\nCtrl-C detected.')
        running = False

# Clean up
# ==============================
print 'cleaning up...'
GPIO.cleanup()
camera.close()