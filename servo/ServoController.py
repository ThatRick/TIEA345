class Servo:
    def __init__(self, pwm, min, max):
        self.min = min
        self.max = max
        self._pwm = pwm
        self._pos = 50.0
        self._started = False

    def setpos(self, perc): # pos = 0..100%
        span = self.max - self.min
        duty = self.min + span * (perc / 100.0)
        if not self._started:
            self._pwm.start(duty)
            self._started = True
        else:
            self._pwm.ChangeDutyCycle(duty)

    def stop(self):
        self._pwm.ChangeDutyCycle(0)
