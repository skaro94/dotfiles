#!/bin/bash

# preprocess: merge server/user files with common

COMMON_FILE_LIST=$(find $(pwd)/ -name "common")
SERVER_FILE_LIST=$(find $(pwd)/ -name "server")
PERSONAL_FILE_LIST=$(find $(pwd)/ -name "personal")

function save_temp {
    for S in $1; do
        TEMP_S="${S}.temp"
        cp $S $TEMP_S
    done
}

function cat_common {
    for S in $1; do
        echo $S
        DIR=$( dirname $S )
        DIR+="/common"
        if [ -f $DIR ]; then
            cat $DIR >> $S
        fi
    done
}

save_temp $SERVER_FILE_LIST
save_temp $PERSONAL_FILE_LIST

cat_common $SERVER_FILE_LIST
cat_common $PERSONAL_FILE_LIST
