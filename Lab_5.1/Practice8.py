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

#main program blink GPIO18 (pin12) fade from 25 to 100%
#Fade from 25 to  50% in 4 steps
blink(18, 50, 0.01, 25)
blink(18, 50, 0.01, 30)
blink(18, 50, 0.01, 35)
blink(18, 50, 0.01, 40)
blink(18, 50, 0.01, 45)
#Fade from 50 to  75% in 4 steps
blink(18, 50, 0.01, 50)
blink(18, 50, 0.01, 55)
blink(18, 50, 0.01, 60)
blink(18, 50, 0.01, 65)
blink(18, 50, 0.01, 70)
#Fade from 75 to  100% in 4 steps
blink(18, 50, 0.01, 75)
blink(18, 50, 0.01, 80)
blink(18, 50, 0.01, 85)
blink(18, 50, 0.01, 90)
blink(18, 50, 0.01, 95)
blink(18, 50, 0.01, 100)


# cleanup
GPIO.cleanup ()
print ("program executed")