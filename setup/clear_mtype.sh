#!/bin/bash

FILE_LIST=$(find .. -name "*.temp")

for S in $FILE_LIST; do
    mv $S ${S:0:-5}
done
