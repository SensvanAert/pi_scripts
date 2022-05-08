#!/usr/bin/env python3 
import time
import busio
import digitalio
import board
import adafruit_pcd8544
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

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

try:
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
    
    while 1:
        #  Clear the display.  Always call show after changing pixels to make the display update visible!
        display.fill(0)
        display.show()
 	
        # Draw a white filled box to clear the image.
        draw.rectangle((0, 0, display.width, display.height), outline=255, fill=255)
        
        # Write text
        Timestamp = time.localtime()
        current_time =  time.strftime("%H:%M:%S", Timestamp)

        if current_time < '18:00:00' and current_time > '06:00:00':
            feeding_time = '18:00:00'
        else:
            feeding_time = '6:00:00'

        toggle = 1      
        if toggle == 1:
            lampStatus = 'ON'
        else:
            lampStatus = 'OFF'
        
        # turnOff = '24:00:00' - current_time
        turnOff = 5

        draw.text((1,0), current_time, font=font)
        draw.text((1,8), 'Water depth: ' + str(20) + 'cm', font=font)
        draw.text((1,16), 'Next feeding: ' + feeding_time, font=font)
        draw.text((1,24), 'Lamp status: ' + lampStatus, font=font)
        draw.text((1,32), 'Turn off lamp in: ' + str(turnOff) + ' hours', font=font)
        display.image(image)
        display.show()
        time.sleep(1)

except KeyboardInterrupt:
    #cleanup
    print("clean closed")