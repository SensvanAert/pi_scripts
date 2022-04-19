import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

GPIO.setup(8, GPIO.OUT)
GPIO.setup(25, GPIO.IN)
GPIO.output(8, 0)

try:
    while(True):
        if(GPIO.input(25) == 0):
            GPIO.output(8, 1)
            time.sleep(0.2)
        else:
            GPIO.output(8, 0)

except KeyboardInterrupt:
    #cleanup
    GPIO.cleanup()
    print("clean closed")