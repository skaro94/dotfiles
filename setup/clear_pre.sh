#!/bin/bash

DOT_PATH=$HOME"/.dotfiles"
PRE_FILE_LIST=$(find $DOT_PATH -name "*.pre")

for FILE_NAME in $PRE_FILE_LIST; do
    ORIGIN_NAME=${FILE_NAME:0:-4}
    rm -f $ORIGIN_NAME
done
