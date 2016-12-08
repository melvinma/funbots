from gtts import gTTS
import sys

print(sys.version)

blabla = ("You have been a good boy Have a lollipop")
tts = gTTS(text=blabla, lang='en-au')
tts.save("/tmp/test.mp3")
