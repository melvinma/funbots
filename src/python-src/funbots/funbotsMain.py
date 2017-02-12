
import time
import os
import signal
from os.path import expanduser
import base64
from enum import Enum
from subprocess import check_output
from subprocess import CalledProcessError

import picamera

from googleapiclient import discovery
from PIL import Image
from PIL import ImageDraw

import RPi.GPIO as GPIO
import simpleaudio as sa


def removeIfExisting(filePath):
    try:
    	os.remove(filePath)
    except OSError:
        pass

def takePhoto():
    removeIfExisting(photoPath)
    print("capturing image to %s" % (photoPath))
    camera = picamera.PiCamera()
    camera.capture(photoPath)
    camera.close()

def resizeImage():
    removeIfExisting(resizedPath)

    img = Image.open(photoPath)
    wpercent = (resizedImageWidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((resizedImageWidth, hsize), Image.ANTIALIAS)
    img.save(resizedPath)

def showImage(imgPath):
    try:
        pid = int(check_output(["pidof","-s", "display"]))
        if pid:
            os.kill(pid, signal.SIGTERM)    
    except CalledProcessError:
        pass
    img = Image.open(imgPath)
    img.show()


def get_vision_service():
    ## conf defined in the default variable GOOGLE_APPLICATION_CREDENTIAL
    return discovery.build('vision', 'v1')

def detect_face(face_file, max_results=4):
    """Uses the Vision API to detect faces in the given file.

    Args:
        face_file: A file-like object containing an image with faces.

    Returns:
        An array of dicts with information about the faces in the picture.
    """
    image_content = face_file.read()
    batch_request = [{
        'image': {
            'content': base64.b64encode(image_content).decode('utf-8')
            },
        'features': [{
            'type': 'FACE_DETECTION',
            'maxResults': max_results,
            }]
        }]

    service = get_vision_service()
    request = service.images().annotate(body={
        'requests': batch_request,
        })
    response = request.execute()

    if response['responses'][0]:
        return response['responses'][0]['faceAnnotations']
    else:
        return None

def highlight_faces(image, faces, output_filename):
    """Draws a polygon around the faces, then saves to output_filename.

    Args:
      image: a file containing the image with the faces.
      faces: a list of faces found in the file. This should be in the format
          returned by the Vision API.
      output_filename: the name of the image file to be created, where the
          faces have polygons drawn around them.
    """
    
    removeIfExisting(output_filename)

    im = Image.open(image)
    draw = ImageDraw.Draw(im)

    for face in faces:
        box = [(v.get('x', 0.0), v.get('y', 0.0))
               for v in face['fdBoundingPoly']['vertices']]
        draw.line(box + [box[0]], width=5, fill='#00ff00')

        print("angerLikelihood=" + face['angerLikelihood'])
        print("sorrowLikelihood=" + face['sorrowLikelihood'])


    im.save(output_filename)

class Likelihood (Enum) :
    """A representation of likelihood to give stable results across upgrades.

    See:
    https://cloud.google.com/vision/reference/rest/v1/images/annotate#likelihood
    """
    UNKNOWN = 0
    VERY_UNLIKELY = 1
    UNLIKELY = 2
    POSSIBLE = 3
    LIKELY = 4
    VERY_LIKELY = 5

    def convertString(strVal):
      ret = None
      for llh in Likelihood:
        if strVal == llh.name:
            ret = llh
            break
      return ret 

class Emotion:
    def __init__(self):
        self.joy_likelihood = Likelihood.UNKNOWN
        self.sorrow_likelihood = Likelihood.UNKNOWN
        self.surprise_likelihood = Likelihood.UNKNOWN
        self.anger_likelihood = Likelihood.UNKNOWN
        self.headwear_likelihood = Likelihood.UNKNOWN
    
    def dumpValues(self):
        print("joy_likelihood=%s, sorrow_likelihood=%s, surprise_likelihood=%s, anger_likelihood=%s headwear_likelihood=%s" 
                % (self.joy_likelihood.name, self.sorrow_likelihood.name, self.surprise_likelihood.name, self.anger_likelihood.name, self.headwear_likelihood.name ))

def resultImage(face):
    em = Emotion()
    em.anger_likelihood = Likelihood.convertString(face['angerLikelihood'])
    em.joy_likelihood = Likelihood.convertString(face['joyLikelihood'])
    em.sorrow_likelihood = Likelihood.convertString(face['sorrowLikelihood'])
    em.surprise_likelihood = Likelihood.convertString(face['surpriseLikelihood'])
    em.headwear_likelihood = Likelihood.convertString(face['headwearLikelihood'])
    return em


def reviewImage():
    with open(resizedPath, 'rb') as image:
        faces = detect_face(image, 4)
        if faces:
            print('Found {} face{}'.format(
                len(faces), '' if len(faces) == 1 else 's'))

            if len(faces) > 0 :
                print('Writing highlighted to file {}'.format(highlightedPath))
                # Reset the file pointer, so we can read the file again
                image.seek(0)
                highlight_faces(image, faces, highlightedPath)
       
                ## generate results
                return resultImage(faces[0])
            else :
                return None
        else:
            return None

def playSound(soundFilePath):
    print("Playing sound fullPath=" + soundFilePath)
    wave_obj = sa.WaveObject.from_wave_file(soundFilePath)
    play_obj = wave_obj.play()
    play_obj.wait_done()


def actOnEmotion(emotion):
    if emotion:
        if emotion.joy_likelihood.value > Likelihood.UNLIKELY.value :
            print("happy")
            playSound(soundPath + "light-sabre-battle.wav")
        elif emotion.anger_likelihood.value > Likelihood.UNLIKELY.value :
            print("anger")
            playSound(soundPath + "light-sabre-on.wav")
        elif emotion.sorrow_likelihood.value > Likelihood.UNLIKELY.value :
            print("sorrow")
            playSound(soundPath + "light-sabre-off.wav")
        elif emotion.surprise_likelihood.value > Likelihood.UNLIKELY.value :
            print("surprise")
            playSound(soundPath + "starwar-vader-breathing.wav")
        else:
            print("No Emotion??")
            playSound(soundPath + "starwar-vader-breathing.wav")


    else:
         playSound(soundPath + "chewy_roar.wav")


## main progarm for funbots.
## Current design:
##   1. click button to trigger the start of the processing...
##   2. take a picture
##   3. call Google Vision to analyze the picture.
##   4. then depend on the result, respond.
##   5. then the system could response to the button click again.

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
            
            takePhoto()
            resizeImage()
            emotion = reviewImage()
            if emotion:
                showImage(highlightedPath)

                emotion.dumpValues()
                actOnEmotion(emotion)
            else:
                showImage(resizedPath)
                actOnEmotion(emotion)
            ## sleep 1 second
            ## time.sleep(1)
            processing = False


print("start funbotsMain")    
#adjust for where your switch is connected
buttonPin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(buttonPin,GPIO.IN)

photoPath="/tmp/funbots-initial-image.jpg"
resizedPath="/tmp/funbots-resized-image.jpg"
highlightedPath="/tmp/funbots-highlighted-image.jpg"
resizedImageWidth = 600

homePath = expanduser("~")
credFile = os.path.join(homePath, 'funbots/baymax-googlekey.txt')
print("initiate google vision... the file is stored at %s" % (credFile))
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credFile

scriptPath = os.path.dirname(os.path.realpath(__file__))
soundPath = scriptPath + '/../../resources/sound-samples/'


print("before main")
main()
print("all done")
