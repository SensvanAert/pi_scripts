import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM) #GPIO24

#Blinking function
def blink(pin):
    #setup GPIO output channel
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 1)
    time.sleep(0.5)
    GPIO.output(pin, 0)
    time.sleep(0.5)

#main program blink GPIO24 infinity
try:
    while(1):
        blink(24)
except KeyboardInterrupt:
    #cleanup
    GPIO.cleanup()
    print("clean closed")