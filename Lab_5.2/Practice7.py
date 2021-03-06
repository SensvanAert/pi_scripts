import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM) #GPIO24, #GPIO25, #GPIO8, #GPIO7

#Blinking function
def steps(pin1,pin2,pin3,pin4):
    #setup GPIO output channel
    GPIO.setup(pin1, GPIO.OUT)
    GPIO.setup(pin2, GPIO.OUT)
    GPIO.setup(pin3, GPIO.OUT)
    GPIO.setup(pin4, GPIO.OUT)
    GPIO.output(pin1, 1)
    time.sleep(1)
    GPIO.output(pin1, 0)
    GPIO.output(pin2, 1)
    time.sleep(1)
    GPIO.output(pin2, 0)
    GPIO.output(pin3, 1)
    time.sleep(1)
    GPIO.output(pin3, 0)
    GPIO.output(pin4, 1)
    time.sleep(1)
    GPIO.output(pin4, 0)

#main program stepper motor #GPIO24, #GPIO25, #GPIO8, #GPIO7 infinity
try:
    while(1):
        steps(24,25,8,7)
except KeyboardInterrupt:
    #cleanup
    GPIO.cleanup()
    print("clean closed")