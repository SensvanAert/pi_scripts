import RPi.GPIO as GPIO
import time
# to use raspberry PI GPIO numbers
GPIO.setmode (GPIO.BCM) # GPIO18
# blinking function
def blink(pin, aantalBlinks, periode, dutyCycle):
    # setup GPIO output channel
    GPIO.setup(pin, GPIO.OUT)
    tijdhoog = periode * dutyCycle/100
    tijdlaag= periode - tijdhoog
    for teller in range (0, aantalBlinks):
        GPIO.output (pin, GPIO.HIGH)
        time.sleep (tijdhoog)
        GPIO.output (pin, GPIO.LOW)
        time.sleep (tijdlaag)
#main program blink GPIO18 (pin12) 200 times
blink(18, 200, 0.01, 15)

# cleanup
GPIO.cleanup ()
print ("program executed")