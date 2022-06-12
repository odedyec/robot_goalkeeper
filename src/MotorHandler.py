import RPi.GPIO as GPIO
import time
from math import pi

MIN_PWM = 2.5
MAX_PWM = 10.



class MotorHandler:
    def __init__(self):
        self._servoPIN = 17
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._servoPIN, GPIO.OUT)

        self._pwm_h = GPIO.PWM(self._servoPIN, 50) # GPIO 17 for PWM with 50Hz
        self._pwm_h.start((MAX_PWM + MIN_PWM) / 2.)

    def set_pwm(self, pwm):
        self._pwm_h.ChangeDutyCycle(pwm)

    def set_angle(self, angle):
        pwm = angle * (MAX_PWM - MIN_PWM) / pi + (MAX_PWM+MIN_PWM) / 2.
        self.set_pwm(pwm)

    def __del__(self):
        self._pwm_h.stop()
        #GPIO.cleanup()


if __name__ == '__main__':
    try:
        mot = MotorHandler()
        angle = 0
        prog = 0.1
        while True:
            mot.set_angle(angle)
            print(angle)
            angle += prog
            if angle > pi / 2:
                prog = -0.1
            if angle < -pi / 2:
                prog = 0.1
            time.sleep(0.1)

    except KeyboardInterrupt:
        GPIO.cleanup()
