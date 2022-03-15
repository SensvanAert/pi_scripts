import RPi.GPIO as GPIO
import time
# to use raspberry PI board GPIO numbers
GPIO.setmode (GPIO.BCM)
GPIO.setup (17, GPIO.IN) # GPIO 17 input
GPIO.setup (23, GPIO.IN) # GPIO 23 input
GPIO.setup (24, GPIO.OUT) # GPIO 24 output
GPIO.setup (22, GPIO.OUT) # GPIO 22 output

#main program

try:
    while (True):
        GPIO.output(24, 1)
        GPIO.output(22, 1)
        if (GPIO.input(17) == 1):
            GPIO.output(24, 0)
        
        if (GPIO.input(23) == 1):
            GPIO.output(22, 0)

except KeyboardInterrupt:
    #cleanup
    GPIO.cleanup()
    print("clean closed")
