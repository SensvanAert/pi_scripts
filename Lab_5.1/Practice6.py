import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM) #GPIO24, #GPIO23, #GPIO22, #GPIO27

#Blinking function
def blink(pin1):
    #setup GPIO output channel
    GPIO.setup(pin1, GPIO.OUT)
    GPIO.output(pin1, 1)
    time.sleep(0.1)
    GPIO.output(pin1, 0)
    time.sleep(0.1)
    GPIO.output(pin1, 1)
    time.sleep(0.1)
    GPIO.output(pin1, 0)
    time.sleep(0.1)
    GPIO.output(pin1, 1)
    time.sleep(0.1)
    GPIO.output(pin1, 0)
    time.sleep(0.1)

    GPIO.output(pin1, 1)
    time.sleep(0.3)
    GPIO.output(pin1, 0)
    time.sleep(0.3)
    GPIO.output(pin1, 1)
    time.sleep(0.3)
    GPIO.output(pin1, 0)
    time.sleep(0.3)
    GPIO.output(pin1, 1)
    time.sleep(0.3)
    GPIO.output(pin1, 0)
    time.sleep(0.3)

    GPIO.output(pin1, 0)
    time.sleep(0.1)
    GPIO.output(pin1, 1)
    time.sleep(0.1)
    GPIO.output(pin1, 0)
    time.sleep(0.1)
    GPIO.output(pin1, 1)
    time.sleep(0.1)
    GPIO.output(pin1, 0)
    time.sleep(0.1)



    

#main program blink #GPIO24, #GPIO23, #GPIO22, #GPIO27 infinity
try:
    while(1):
        blink(18)
except KeyboardInterrupt:
    #cleanup
    GPIO.cleanup()
    print("clean closed")