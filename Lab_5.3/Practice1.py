import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM) #GPIO17
GPIO.setup(17, GPIO.IN)

try:
    while(True):
        if(GPIO.input(17) == 0):
            print("dark")
            time.sleep(0.5)
        else:
            print("light")
            time.sleep(0.5)

except KeyboardInterrupt:
    #cleanup
    GPIO.cleanup()
    print("clean closed")