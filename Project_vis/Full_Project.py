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
GPIO.setup(23, GPIO.IN)
GPIO.setup(24, GPIO.OUT)
#Feeder pins
GPIO.setup(27, GPIO.IN)
GPIO.setup(22, GPIO.IN)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(1, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)

exit_event = threading.Event()

GPIO.output(8, 1)
GPIO.output(24, 1)
GPIO.output(7, 0)
GPIO.output(1, 0)
GPIO.output(5, 0)
GPIO.output(6, 0)

def light ():
    toggle = 0
    while True:
        timestamp = time.localtime()
        current_time =  time.strftime("%H:%M:%S", timestamp)

        if current_time == "20:00:00":
            GPIO.output(24, 0)
            toggle = 1

        if current_time == "00:00:00":
            GPIO.output(24, 1)
            toggle = 0

        if GPIO.input(23) == 0:
            if toggle == 0:
                GPIO.output(24, 0)
                toggle = 1
            else:
                GPIO.output(24, 1)
                toggle = 0
            time.sleep(0.3)

        if exit_event.is_set():
            break

def depthAndPump():
    aquariumDepth = 20
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
        time.sleep(0.2)
        
        if (actualDepth < 14 and buttonActive == 0):
            depthActive = 1
            GPIO.output(8, 0)
        
        if (actualDepth > 17 and depthActive == 1):
            depthActive = 0
            GPIO.output(8, 1)
        
        if (GPIO.input(25) == 0 and depthActive == 0):
            buttonActive = 1
            GPIO.output(8, 0)
        
        if (GPIO.input(25) == 1 and buttonActive == 1):
            buttonActive = 0
            GPIO.output(8, 1)

        if exit_event.is_set():
            break

def feeder ():
    counter = 0
    enableFeeder = 0

    while True:
        Timestamp = time.localtime()
        current_time =  time.strftime("%H:%M:%S", Timestamp)

        if current_time == "18:00:00" or current_time == "06:00:00":
            enableFeeder = 1
            counter = 0



        while GPIO.input(27) == 0 or enableFeeder == 1:
            if enableFeeder == 1:
                counter +=1
            if counter == 125:
                enableFeeder = 0
            GPIO.output(7, 1)
            GPIO.output(1, 1)
            time.sleep(0.01)
            GPIO.output(7, 0)
            GPIO.output(5, 1)
            time.sleep(0.01)
            GPIO.output(1, 0)
            GPIO.output(6, 1)
            time.sleep(0.01)
            GPIO.output(5, 0)
            GPIO.output(7, 1)
            time.sleep(0.01)
            GPIO.output(6, 0)

        while GPIO.input(22) == 0:
            GPIO.output(6, 1)
            GPIO.output(5, 1)
            time.sleep(0.01)
            GPIO.output(6, 0)
            GPIO.output(1, 1)
            time.sleep(0.01)
            GPIO.output(5, 0)
            GPIO.output(7, 1)
            time.sleep(0.01)
            GPIO.output(1, 0)
            GPIO.output(6, 1)
            time.sleep(0.01)
            GPIO.output(7, 0)

        if exit_event.is_set():
            break


# All Threads
lightThread = threading.Thread(target=light)
depthThread = threading.Thread(target=depthAndPump)
feederThread = threading.Thread(target=feeder)

# Starting the threads
lightThread.start()
depthThread.start()
feederThread.start()

try:
    while(True):
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        print(current_time)
        print("Still working")
        time.sleep(1.0)

except KeyboardInterrupt:
    exit_event.set()
    #cleanup
    GPIO.cleanup()
    print("clean closed")
