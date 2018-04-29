#!/bin/bash

# preprocess: fill up values in .pre files
VALUE_FILE=$HOME
VALUE_FILE+="/.dotfiles/values"

declare -a VALS
COUNT=0

while read LINE; do
    array=($LINE)
    EXPORT=${array[0]}
    if [ "$EXPORT" == "export" ]; then
        arr=$(echo "${array[1]}"| tr "=" "\n")
        arr=($arr)
        VAR_NAME=${arr[0]:1}
        VAR_VAL=${arr[1]:1}
        VAR_VAL=${VAR_VAL:0:-1}
        VALS[$COUNT]="$VAR_NAME:$VAR_VAL"
        let "COUNT += 1"
    fi
done < $VALUE_FILE

PRE_FILE_LIST=$(find . -name "*.pre")

for FILE_NAME in $PRE_FILE_LIST; do
    NEW_NAME=${FILE_NAME:0:-4}
    SED=""
    for VAL in ${VALS[*]}; do
        VAL=($(echo "${VAL}"| tr ":" "\n"))
        SED+="s/<<:${VAL[0]}>>/${VAL[1]}/g; "
    done
    SED=${SED:0:-2}
    sed "$SED" $FILE_NAME > $NEW_NAME
done

