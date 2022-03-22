import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM) #GPIO17, #GPIO24, #GPIO25, #GPIO8, #GPIO7
GPIO.setup(17, GPIO.IN)
GPIO.setup(18, GPIO.IN)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(8, GPIO.OUT)
GPIO.setup(7, GPIO.OUT)

try:
    while(True):
        if(GPIO.input(17) == 0 or GPIO.input(18) == 0):
            print("Lights on")
            GPIO.output(24, 1)
            GPIO.output(25, 1)
            GPIO.output(8, 1)
            GPIO.output(7, 1)
            time.sleep(0.5)
        else:
            print("light off")
            GPIO.output(24, 0)
            GPIO.output(25, 0)
            GPIO.output(8, 0)
            GPIO.output(7, 0)
            time.sleep(0.5)

except KeyboardInterrupt:
    #cleanup
    GPIO.cleanup()
    print("clean closed")