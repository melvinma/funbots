#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SCRIPT="$DIR/../python-src/examples/playAudio.py"

python3 "$SCRIPT" -sn $1
