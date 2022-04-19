import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
#setup GPIO input channel
GPIO.setup(27, GPIO.IN)
GPIO.setup(22, GPIO.IN)
#setup GPIO output channel
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(10, GPIO.OUT)
GPIO.setup(9, GPIO.OUT)

#main program stepper motor #GPIO23, #GPIO24, #GPIO10, #GPIO9 infinity
try:
    while(1):
        while (GPIO.input(27) == 0):
            GPIO.output(23, 1)
            GPIO.output(24, 1)
            time.sleep(0.01)
            GPIO.output(23, 0)
            GPIO.output(10, 1)
            time.sleep(0.01)
            GPIO.output(24, 0)
            GPIO.output(9, 1)
            time.sleep(0.01)
            GPIO.output(10, 0)
            GPIO.output(23, 1)
            time.sleep(0.01)
            GPIO.output(9, 0)

        while (GPIO.input(22) == 0):
            GPIO.output(9, 1)
            GPIO.output(10, 1)
            time.sleep(0.01)
            GPIO.output(9, 0)
            GPIO.output(24, 1)
            time.sleep(0.01)
            GPIO.output(10, 0)
            GPIO.output(23, 1)
            time.sleep(0.01)
            GPIO.output(24, 0)
            GPIO.output(9, 1)
            time.sleep(0.01)
            GPIO.output(23, 0)


except KeyboardInterrupt:
    #cleanup
    GPIO.cleanup()
    print("clean closed")