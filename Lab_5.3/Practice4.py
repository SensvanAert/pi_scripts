import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

try:
    while(True):
        GPIO.setup(18, GPIO.OUT)
        GPIO.output(18, 0)
        time.sleep(0.1)

        GPIO.setup(18, GPIO.IN)
        start_time = time.time()
        while(GPIO.input(18) == 0):
            pass
        
        stop_time = time.time()
        interval = stop_time - start_time
        print(str(1000*interval))
        

except KeyboardInterrupt:
    #cleanup
    GPIO.cleanup()
    print("clean closed")