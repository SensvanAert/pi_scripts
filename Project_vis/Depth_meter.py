import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.OUT)
GPIO.setup(8, GPIO.OUT)
GPIO.setup(18, GPIO.IN)
GPIO.setup(25, GPIO.IN)

aquariumDepth = 50
actualDepth = 0

try:
    while(True):
        GPIO.output(17, 1)
        time.sleep(0.00001)
        GPIO.output(17, 0)
        # GPIO.output(8, 0)

        while(GPIO.input(18) == 0):
            pass

        signalHigh = time.time()

        while(GPIO.input(18) == 1):
            pass

        signalLow = time.time()
        timePassed = signalLow - signalHigh
        distance = 17000 * timePassed
        actualDepth = aquariumDepth - distance
        print(str(actualDepth))
        time.sleep(0.5)

        if(actualDepth >= 40 or GPIO.input(25) == 1):
            GPIO.output(8, 0)
        else:
            GPIO.output(8, 1)


except KeyboardInterrupt:
    #cleanup
    GPIO.cleanup()
    print("clean closed")
