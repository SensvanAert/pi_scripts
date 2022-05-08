from datetime import datetime, timedelta
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
import adafruit_pcd8544
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

GPIO.setmode(GPIO.BCM)
#Depth pins
GPIO.setup(18, GPIO.IN)
GPIO.setup(17, GPIO.OUT)    # trigger
#Pump pins
GPIO.setup(25, GPIO.IN)     # Pump on
GPIO.setup(14, GPIO.OUT)     # pump (25)
#Light pins
GPIO.setup(20, GPIO.IN)     # Light on/off
GPIO.setup(2, GPIO.IN)      # 15 min
GPIO.setup(21, GPIO.OUT)    # Light
#Feeder pins
GPIO.setup(27, GPIO.IN)     # StepperMotor left
GPIO.setup(22, GPIO.IN)     # StepperMotor right
GPIO.setup(9, GPIO.OUT)
GPIO.setup(1, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)

# Turn all outputs off
GPIO.output(14, 1)
GPIO.output(21, 1)
GPIO.output(9, 0)
GPIO.output(1, 0)
GPIO.output(5, 0)
GPIO.output(6, 0)

exit_event = threading.Event()
url = 'http://sensvanaert.hub.ubeac.io/iotesssensvanaert'
uid = 'iotesssensvanaert'
toggle = 0
pump = 0
actualDepth = 0
timer = 0
end_time = datetime.strptime('00:00:00', "%H:%M:%S")

def light ():
    pressed = 0
    global end_time
    global timer
    global toggle
    while True:
        timestamp = time.localtime()
        current_time =  time.strftime("%H:%M:%S", timestamp)

        if GPIO.input(2) == 0:
            if timer == 0:
                timer = 1
                end_time = datetime.strptime(current_time, "%H:%M:%S") + timedelta(minutes=1)
                print(end_time.strftime("%H:%M:%S"))
                GPIO.output(21, 0)
                toggle = 1
        
        if current_time == end_time.strftime("%H:%M:%S") and timer == 1:
            print("Turn the light off")
            timer = 0
            GPIO.output(21, 1)
            toggle = 0
            
        if current_time == "20:00:00":
            GPIO.output(21, 0)
            toggle = 1

        if current_time == "00:00:00":
            GPIO.output(21, 1)
            toggle = 0

        if GPIO.input(20) == 0:
            if toggle == 0 and pressed == 0:
                GPIO.output(21, 0)
                toggle = 1
            elif pressed == 0:
                GPIO.output(21, 1)
                toggle = 0
                timer = 0
            pressed = 1
            time.sleep(0.3)

        if GPIO.input(20) == 1:
            pressed = 0

        if exit_event.is_set():
            break

def depthAndPump():
    global pump
    global actualDepth
    aquariumDepth = 25
    depthActive = 0
    buttonActive = 0

    while True:
        GPIO.output(17, 1)      # give pulse for distance meter
        time.sleep(0.00001)
        GPIO.output(17, 0)

        while(GPIO.input(18) == 0): # do nothing if no signal is returned
            pass

        signalHigh = time.time()    # note time of received signal

        while(GPIO.input(18) == 1): # how long is the signal received for
            pass

        signalLow = time.time()                             # note time of how long is the signal received for
        timePassed = signalLow - signalHigh                 # time passed is time when received minus time of the end of the signal
        distance = 17000 * timePassed                       # formula to calculate the distance
        actualDepth = round(aquariumDepth - distance, 2)    # Formula to calculate how high the water level is
        print(str(actualDepth))

        if depthActive == 1 or buttonActive == 1:   # print every 0.2 seconds when pump activated else every 0.7 seconds
            pump = 1
            time.sleep(0.2)
        else:
            pump = 0
            time.sleep(0.7)
        
        if (actualDepth < 14 and buttonActive == 0):    # Turn on if depth below 14 cm and pump not turned on by button
            depthActive = 1
            GPIO.output(14, 0)
        
        if (actualDepth > 17 and depthActive == 1):     # Turn off if depth above 17 cm and pump activated by depth
            depthActive = 0
            GPIO.output(14, 1)
        
        if (GPIO.input(25) == 0 and depthActive == 0):  # Turn on if button pressed and not activated by depth
            buttonActive = 1
            GPIO.output(14, 0)
        
        if (GPIO.input(25) == 1 and buttonActive == 1): # Turn off button is not pressed and activated by button
            buttonActive = 0
            GPIO.output(14, 1)

        if exit_event.is_set():
            break

def feeder ():
    counter = 0
    enableFeeder = 0

    while True:
        Timestamp = time.localtime()
        current_time =  time.strftime("%H:%M:%S", Timestamp)

        if current_time == "18:00:00" or current_time == "06:00:00":    # Feed fishes on 6am and 6pm
            enableFeeder = 1
            counter = 0

        while GPIO.input(27) == 0 or enableFeeder == 1:     # Let feeder go forward
            if enableFeeder == 1:   # Feeder will turn on for 5 seconds
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

        while GPIO.input(22) == 0:  # Let feeder go Backwards
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

def LCD ():
    # Initialize SPI bus
    spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

    # Initialize display
    dc = digitalio.DigitalInOut(board.D23)  # data/command
    cs1 = digitalio.DigitalInOut(board.CE1)  # chip select CE1 for display
    reset = digitalio.DigitalInOut(board.D24)  # reset
    display = adafruit_pcd8544.PCD8544(spi, dc, cs1, reset, baudrate= 1000000)
    display.bias = 4
    display.contrast = 60
    display.invert = True

    #  Clear the display.  Always call show after changing pixels to make the display update visible!
    display.fill(0)
    display.show()

    # Load default font.
    font = ImageFont.load_default()
    #font=ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSansBold.ttf", 10)

    # Get drawing object to draw on image
    image = Image.new('1', (display.width, display.height)) 
    draw = ImageDraw.Draw(image)
 	
    # Draw a white filled box to clear the image.
    draw.rectangle((0, 0, display.width, display.height), outline=255, fill=255)

    while True:
        # Draw a white filled box to clear the image.
        draw.rectangle((0, 0, display.width, display.height), outline=255, fill=255)

        # Write text
        Timestamp = time.localtime()
        current_time =  time.strftime("%H:%M:%S", Timestamp)

        if current_time < '18:00:00' and current_time > '06:00:00':     # What time will be the next feeding
            feeding_time = '18:00:00'
        else:
            feeding_time = '6:00:00'
        
        if toggle == 1:            # if lamp is on display ON else display OFF
            lampStatus = 'ON'
        else:
            lampStatus = 'OFF'
        
        lightsOut = '00:00:00'
        if timer == 1:
            lightsOut = end_time.strftime("%H:%M:%S")

        draw.text((1,0), current_time, font=font)                           # current time
        draw.text((1,8), 'Depth: ' + str(actualDepth) + 'cm', font=font)    # depth of the water
        draw.text((1,16), 'NF: ' + feeding_time, font=font)                 # Next feeding time
        draw.text((1,24), 'Lamp: ' + lampStatus, font=font)                 # Status of the lamp
        draw.text((1,32), 'LO: ' + lightsOut, font=font)        # hours till the lamp will turn off
        display.image(image)
        display.show()
        time.sleep(1)

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
lcdThread = threading.Thread(target=LCD)
sendDataThread = threading.Thread(target=sendData)

# Starting the threads
lightThread.start()
depthThread.start()
feederThread.start()
lcdThread.start()
# sendDataThread.start()

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
