#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

##SRCIMG="$DIR/../resources/face-input.jpg"
SRCIMG="$DIR/../resources/very-angry-face.jpg"
OUTIMG="/tmp/face-output.jpg"
SCRIPT="$DIR/../python-src/examples/googleVision.py"

## MAX 4 FACES.
python3 "$SCRIPT" "$SRCIMG" --out="$OUTIMG" --max-results=4
##
