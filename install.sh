#!/bin/bash

source deactivate

bash setup/preprocess_pre.sh
bash setup/preprocess_mtype.sh
cp setup/install.py install.py
python2 module.py
rm -f install.py
bash setup/clear_pre.sh
bash setup/clear_mtype.sh

# monkey patch...
echo "Vim plug update"
vim +PlugUpdate +qall

echo "Exec zsh and clear outputs(y/n)?"
read line
if [ line = "y" ]; then
    clear
    exec zsh
fi
