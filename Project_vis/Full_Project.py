import RPi.GPIO as GPIO
import time
import threading

GPIO.setmode(GPIO.BCM)
#Depth pins
GPIO.setup(18, GPIO.IN)
GPIO.setup(17, GPIO.OUT)
#Pump pins
GPIO.setup(25, GPIO.IN)
GPIO.setup(8, GPIO.OUT)
#Light pins
GPIO.setup(7, GPIO.IN)
GPIO.setup(1, GPIO.OUT)
#Feeder pins
GPIO.setup(27, GPIO.IN)
GPIO.setup(22, GPIO.IN)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(10, GPIO.OUT)
GPIO.setup(9, GPIO.OUT)

exit_event = threading.Event()

GPIO.output(8, 0)
GPIO.output(1, 0)
GPIO.output(24, 0)
GPIO.output(10, 0)
GPIO.output(9, 0)

def light ():
    toggle = 0
    while True:
        if(GPIO.input(7) == 0):
            if(toggle == 0):
                GPIO.output(1, 1)
                toggle = 1
            else:
                GPIO.output(1, 0)
                toggle = 0
            time.sleep(0.3)

        if exit_event.is_set():
            break

def depthAndPump():
    aquariumDepth = 50
    actualDepth = 0
    depthActive = 0
    buttonActive = 0

    while True:
        GPIO.output(17, 1)
        time.sleep(0.00001)
        GPIO.output(17, 0)

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

        # if(actualDepth < 40 or GPIO.input(25) == 0):
        #     GPIO.output(8, 1)
        # elif(actualDepth > 45 and GPIO.input(25) == 1):
        #     GPIO.output(8, 0)
        
        if (actualDepth < 40 and buttonActive == 0):
            depthActive = 1
            GPIO.output(8, 1)
        
        if (actualDepth > 45 and depthActive == 1):
            depthActive = 0
            GPIO.output(8, 0)
        
        if (GPIO.input(25) == 0 and depthActive == 0):
            buttonActive = 1
            GPIO.output(8, 1)
        
        if (GPIO.input(25) == 1 and buttonActive == 1):
            buttonActive = 0
            GPIO.output(8, 0)

        if exit_event.is_set():
            break

def feeder ():
    while True:
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

        if exit_event.is_set():
            break


# All Threads
lightThread = threading.Thread(target=light)
depthThread = threading.Thread(target=depthAndPump)
feederThread = threading.Thread(target=feeder)

# Starting the threads
lightThread.start()
depthThread.start()

try:
    while(True):
        print("Still working")
        time.sleep(5.0)

except KeyboardInterrupt:
    exit_event.set()
    #cleanup
    GPIO.cleanup()
    print("clean closed")
