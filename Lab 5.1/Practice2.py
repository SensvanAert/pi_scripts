import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM) #GPIO24, #GPIO23, #GPIO22, #GPIO27

#Blinking function
def blink(pin1,pin2,pin3,pin4):
    #setup GPIO output channel
    GPIO.setup(pin1, GPIO.OUT)
    GPIO.output(pin1, 1)
    GPIO.setup(pin2, GPIO.OUT)
    GPIO.output(pin2, 1)
    GPIO.setup(pin3, GPIO.OUT)
    GPIO.output(pin3, 1)
    GPIO.setup(pin4, GPIO.OUT)
    GPIO.output(pin4, 1)
    time.sleep(0.1)
    GPIO.output(pin1, 0)
    GPIO.output(pin2, 0)
    GPIO.output(pin3, 0)
    GPIO.output(pin4, 0)
    time.sleep(0.1)

#main program blink #GPIO24, #GPIO23, #GPIO22, #GPIO27 infinity
try:
    while(1):
        blink(24,23,22,27)
except KeyboardInterrupt:
    #cleanup
    GPIO.cleanup()
    print("clean closed")