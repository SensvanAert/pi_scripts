# event input /home/pi
import RPi.GPIO as GPIO
import time
# to use raspberry PI board GPIO numbers
GPIO.setmode (GPIO.BCM)
GPIO.setup (17, GPIO.IN) # GPIO 17 input
GPIO.setup (24, GPIO.OUT) # GPIO 24 output


#Blinking function
def blink(pin):
    GPIO.output(pin, 1)
    time.sleep(0.5)
    GPIO.output(pin, 0)
    time.sleep(0.5)

# loop forever or ctrl^C
try:
    while True:
        if (GPIO.input (17)==0): #input low active
            print ("LED not flashing")
            time.sleep (0.3) # anti bouncing
        else:
            GPIO.output (24, 0)
            print ("led blinks")
            blink(24)
            time.sleep (0.3) # anti bouncing
except KeyboardInterrupt:
    #cleanup
    GPIO.cleanup()
    print("clean closed")