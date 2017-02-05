#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SCRIPT="$DIR/../python-src/funbots/funbotsMain.py"

amixer cset numid=3 1

python3 "$SCRIPT" 
