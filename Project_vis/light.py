import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

GPIO.setup(1, GPIO.OUT)
GPIO.setup(7, GPIO.IN)

GPIO.output(1, 0)
toggle = 0

try:
    while(True):
        if(GPIO.input(7) == 0):
            if(toggle == 0):
                GPIO.output(1, 0)
                toggle = 1
            else:
                GPIO.output(1, 1)
                toggle = 0
            time.sleep(0.3)

except KeyboardInterrupt:
    #cleanup
    GPIO.cleanup()
    print("clean closed")