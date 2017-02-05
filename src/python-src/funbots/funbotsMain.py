
import time
import os
import base64

import picamera

from googleapiclient import discovery
from PIL import Image
from PIL import ImageDraw

import RPi.GPIO as GPIO


## main progarm for funbots.
## Current design:
##   1. click button to trigger the start of the processing...
##   2. take a picture
##   3. call Google Vision to analyze the picture.
##   4. then depend on the result, respond.
##   5. then the system could response to the button click again.


def setup() :
    
    #adjust for where your switch is connected
    global buttonPin
    buttonPin = 17
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(buttonPin,GPIO.IN)

    global camera
    camera = picamera.PiCamera()

def takePhoto(photoPath):
    camera.capture(photoPath)


def main() :
    print("main before true")
    counter = 0
    processing = False
    while True :
        ##counter = counter + 1
        ##if counter % 1000 == 0:
        ##     print("main inside true")
        #assuming the script to call is long enough we can ignore bouncing
        if (not GPIO.input(buttonPin)) and not processing:
            #this is the script that will be called (as root)
            processing = True
            print("Button pressed")
            
            ## sleep 1 second
            time.sleep(1)
            processing = False

print("before setup")
setup()
print("before main")
main()
