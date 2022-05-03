import RPi.GPIO as GPIO
import time
import threading
import cgitb ; cgitb.enable() 
import spidev 
import busio
import digitalio
import board
import requests
from adafruit_bus_device.spi_device import SPIDevice

GPIO.setmode(GPIO.BCM)
#Depth pins
GPIO.setup(18, GPIO.IN)
GPIO.setup(17, GPIO.OUT)
#Pump pins
GPIO.setup(25, GPIO.IN)
GPIO.setup(8, GPIO.OUT)
#Light pins
GPIO.setup(20, GPIO.IN)
GPIO.setup(21, GPIO.OUT)
#Feeder pins
GPIO.setup(27, GPIO.IN)
GPIO.setup(22, GPIO.IN)
GPIO.setup(9, GPIO.OUT)
GPIO.setup(1, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)

# Initialize SPI bus
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Initialize control pins for adc
cs0 = digitalio.DigitalInOut(board.CE0)  # chip select CE0 for adc
adc = SPIDevice(spi, cs0, baudrate= 1000000)

exit_event = threading.Event()
url = 'http://sensvanaert.hub.ubeac.io/iotesssensvanaert'
uid = 'iotesssensvanaert'
toggle = 0
pump = 0
actualDepth = 0

GPIO.output(8, 1)
GPIO.output(21, 1)
GPIO.output(9, 0)
GPIO.output(1, 0)
GPIO.output(5, 0)
GPIO.output(6, 0)

def light ():
    count = 0
    global toggle
    while True:
        timestamp = time.localtime()
        current_time =  time.strftime("%H:%M:%S", timestamp)

        if current_time == "20:00:00":
            GPIO.output(21, 0)
            toggle = 1

        if current_time == "00:00:00":
            GPIO.output(21, 1)
            toggle = 0

        if GPIO.input(20) == 0:
            if toggle == 0 and count == 0:
                GPIO.output(21, 0)
                toggle = 1
            elif count == 0:
                GPIO.output(21, 1)
                toggle = 0
            count = 1
            time.sleep(0.3)

        if GPIO.input(20) == 1:
            count = 0

        if exit_event.is_set():
            break

def depthAndPump():
    global pump
    aquariumDepth = 25
    global actualDepth
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
        actualDepth = round(aquariumDepth - distance, 2)
        print(str(actualDepth))

        if depthActive == 1 or buttonActive == 1:
            pump = 1
            time.sleep(0.2)
        else:
            pump = 0
            time.sleep(0.7)
        
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
            GPIO.output(9, 1)
            GPIO.output(1, 1)
            time.sleep(0.001)
            GPIO.output(9, 0)
            GPIO.output(5, 1)
            time.sleep(0.001)
            GPIO.output(1, 0)
            GPIO.output(6, 1)
            time.sleep(0.001)
            GPIO.output(5, 0)
            GPIO.output(9, 1)
            time.sleep(0.001)
            GPIO.output(6, 0)

        while GPIO.input(22) == 0:
            GPIO.output(6, 1)
            GPIO.output(5, 1)
            time.sleep(0.001)
            GPIO.output(6, 0)
            GPIO.output(1, 1)
            time.sleep(0.001)
            GPIO.output(5, 0)
            GPIO.output(9, 1)
            time.sleep(0.001)
            GPIO.output(1, 0)
            GPIO.output(6, 1)
            time.sleep(0.001)
            GPIO.output(9, 0)

        if exit_event.is_set():
            break

def sendData ():
    while True:
        data= {
		    "id": uid,
		    "sensors":[{
			    'id': 'light',
			    'data': toggle
		    },
            {
			    'id': 'pump',
			    'data': pump
			},
            {
			    'id': 'depth',
			    'data': actualDepth
			}
            ]
        }
        requests.post(url, verify=False,  json=data)

        time.sleep(1)
        if exit_event.is_set():
            break

# All Threads
lightThread = threading.Thread(target=light)
depthThread = threading.Thread(target=depthAndPump)
feederThread = threading.Thread(target=feeder)
sendDataThread = threading.Thread(target=sendData)

# Starting the threads
lightThread.start()
depthThread.start()
feederThread.start()
sendDataThread.start()

try:
    while(True):
        # t = time.localtime()
        # current_time = time.strftime("%H:%M:%S", t)
        # print(current_time)
        print("Still working")
        time.sleep(3.0)

except KeyboardInterrupt:
    exit_event.set()
    #cleanup
    GPIO.cleanup()
    print("clean closed")
