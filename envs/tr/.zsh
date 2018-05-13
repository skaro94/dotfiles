#!/bin/zsh

TR_ROOT="$HOME/Dropbox/tr"
TR_FILE="book"
export TR_ROOT=$(realpath $TR_ROOT)
export TR_ENV=$TR_ROOT"/envs"
export TR_UTIL=$TR_ENV"/utils"
export TR_SOURCE=$TR_ROOT"/source"
export TERM_FILE=$TR_ROOT"/terms.db"
export PDF_FILE=$TR_SOURCE"/$TR_FILE.pdf"
export HTML_FILE=$TR_SOURCE"/$TR_FILE.html"

export HTML_IMG_WIDTH=600

export PDF_PANE=1
export DICT_PANE=2
export TRANS_PANE=3
export TERM_PANE=4

alias termmem="python ${TR_UTIL}/terms.py"

for f in $TR_UTIL/functions/*; do
    source $f
done

ln -sf $TR_ENV/.vim/* ~/.vim/plugin/
