import RPi.GPIO as GPIO
import time
# to use raspberry PI board GPIO numbers
GPIO.setmode (GPIO.BCM)
GPIO.setup (17, GPIO.IN) # GPIO 17 input
GPIO.setup (24, GPIO.OUT) # GPIO 24 output

#Blinking function
def blink(pin1):
    #setup GPIO output channel
    GPIO.setup(pin1, GPIO.OUT)
    GPIO.output(pin1, 1)
    time.sleep(0.1)
    GPIO.output(pin1, 0)
    time.sleep(0.05)
    GPIO.output(pin1, 1)
    time.sleep(0.05)
    GPIO.output(pin1, 0)
    time.sleep(0.1)
    GPIO.output(pin1, 1)
    time.sleep(0.1)
    GPIO.output(pin1, 0)
    time.sleep(0.1)

    GPIO.output(pin1, 1)
    time.sleep(0.3)
    GPIO.output(pin1, 0)
    time.sleep(0.3)
    GPIO.output(pin1, 1)
    time.sleep(0.3)
    GPIO.output(pin1, 0)
    time.sleep(0.3)
    GPIO.output(pin1, 1)
    time.sleep(0.3)
    GPIO.output(pin1, 0)
    time.sleep(0.3)

    GPIO.output(pin1, 0)
    time.sleep(0.1)
    GPIO.output(pin1, 1)
    time.sleep(0.1)
    GPIO.output(pin1, 0)
    time.sleep(0.1)
    GPIO.output(pin1, 1)
    time.sleep(0.1)
    GPIO.output(pin1, 0)
    time.sleep(0.1)



    

#main program blink #GPIO24, #GPIO23, #GPIO22, #GPIO27 infinity
try:
    while True:
        if (GPIO.input (17)==0):
            print ("led is not flashing")
            GPIO.output(24, 0)
            time.sleep(0.3) #anti-bounce
        else:
            print("led blinks")
            blink(24)
            time.sleep(0.3) #anti-bounce
except KeyboardInterrupt:
    #cleanup
    GPIO.cleanup()
    print("clean closed")