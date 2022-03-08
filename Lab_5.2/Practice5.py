import RPi.GPIO as GPIO
import time
# to use raspberry PI board GPIO numbers
GPIO.setmode (GPIO.BCM)
GPIO.setup (17, GPIO.IN) # GPIO 17 input
GPIO.setup (24, GPIO.OUT) # GPIO 24 output
GPIO.setup (23, GPIO.OUT) # GPIO 23 output
GPIO.setup (22, GPIO.OUT) # GPIO 22 output
GPIO.setup (27, GPIO.OUT) # GPIO 27 output


#Blinking function
def left(pin1,pin2,pin3,pin4):
    #setup GPIO output channel
    GPIO.setup(pin1, GPIO.OUT)
    GPIO.setup(pin2, GPIO.OUT)
    GPIO.setup(pin3, GPIO.OUT)
    GPIO.setup(pin4, GPIO.OUT)
    GPIO.output(pin1, 1)
    time.sleep(0.1)
    GPIO.output(pin1, 0)
    GPIO.output(pin2, 1)
    time.sleep(0.1)
    GPIO.output(pin2, 0)
    GPIO.output(pin3, 1)
    time.sleep(0.1)
    GPIO.output(pin3, 0)
    GPIO.output(pin4, 1)
    time.sleep(0.1)
    GPIO.output(pin4, 0)
    

def right(pin1,pin2,pin3,pin4):
    #setup GPIO output channel
    GPIO.setup(pin1, GPIO.OUT)
    GPIO.setup(pin2, GPIO.OUT)
    GPIO.setup(pin3, GPIO.OUT)
    GPIO.setup(pin4, GPIO.OUT)
    GPIO.output(pin4, 1)
    time.sleep(0.1)
    GPIO.output(pin4, 0)
    GPIO.output(pin3, 1)
    time.sleep(0.1)
    GPIO.output(pin3, 0)
    GPIO.output(pin2, 1)
    time.sleep(0.1)
    GPIO.output(pin2, 0)
    GPIO.output(pin1, 1)
    time.sleep(0.1)
    GPIO.output(pin1, 0)
    

#main program blink #GPIO24, #GPIO23, #GPIO22, #GPIO27 infinity
try:
    while(1):
        if (GPIO.input (17)==0): 
            print("To the left")
            left(24,23,22,27) #To the left
        else:
            print("To the right")
            right(24,23,22,27)
except KeyboardInterrupt:
    #cleanup
    GPIO.cleanup()
    print("clean closed")