
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

def main() :

    while True :
        #assuming the script to call is long enough we can ignore bouncing
        if (GPIO.input(buttonPin)) and not processing:
            #this is the script that will be called (as root)
            processing = True
            print("Button pressed")
            processing = False

def setup() :
    global processing = False
    #adjust for where your switch is connected
    global buttonPin = 17
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(buttonPin,GPIO.IN)

    global camera = picamera.PiCamera()

def takePhoto(photoPath):
    camera.capture(photoPath)
