import argparse
import os

import simpleaudio as sa

def soundOut (soundName) :
    files = {
        'roar':'chewy_roar.wav',
        'battle':'light-sabre-battle.wav',
        'sabreon':'light-sabre-on.wav',
        'sabroff':'light-sabre-off.wav',
        'breathing':'starwar-vader-breathing.wav',
    }

    path=os.path.dirname(os.path.realpath(__file__))
    fullPath= path + '/../../resources/sound-samples/' + files[soundName]
    print("fullPath=" + fullPath)
    wave_obj = sa.WaveObject.from_wave_file(fullPath)
    play_obj = wave_obj.play()
    play_obj.wait_done()

if __name__ == '__main__':

    ## get input from command line.
    ##   python3 playAudio.py -sn sabreon
    ## or   python3 playAudio.py
    parser = argparse.ArgumentParser(
        description='Voice out sounds given an input argument.')
    parser.add_argument(
        '-sn',
        '--soundName',
        help='the name of the sound.',
        default='battle',
        choices=['battle', 'sabreon', 'sabroff', 'breathing', 'roar'])
    args = parser.parse_args()

    ## call function soundOut
    soundOut(args.soundName)
