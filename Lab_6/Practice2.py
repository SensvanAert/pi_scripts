#!/usr/bin/env python3 
import RPi.GPIO as GPIO
import time
import cgitb ; cgitb.enable() 
import spidev 
import time
import busio
import digitalio
import board
from adafruit_bus_device.spi_device import SPIDevice
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
# Initialize SPI bus
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Initialize control pins for adc
cs0 = digitalio.DigitalInOut(board.CE0)  # chip select
adc = SPIDevice(spi, cs0, baudrate= 1000000)
 
# read SPI data 8 possible adc's (0 thru 7) 
def readadc(adcnum): 
    if ((adcnum > 7) or (adcnum < 0)): 
        return -1 
    with adc:
        r = bytearray(3)
        spi.write_readinto([1,(8+adcnum)<<4,0], r)
        time.sleep(0.000005)
        adcout = ((r[1]&3) << 8) + r[2] 
        return adcout 
 
try:
    while (1):
        tmp0 = readadc(0) # read channel 0 
        tmp1 = readadc(1) # read channel 1
        if tmp0 > tmp1:
            if tmp0 - tmp1 >= 10:
                GPIO.output(23, 1)
                GPIO.output(24, 0)
                print("LED_A on")
        elif tmp1 - tmp0 >= 10:
            GPIO.output(23, 0)
            GPIO.output(24, 1)
            print("LED_B on")
        time.sleep(0.2)

except KeyboardInterrupt:
    GPIO.cleanup()
    print("program executed")