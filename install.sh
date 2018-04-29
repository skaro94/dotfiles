#!bin/bash

bash setup/preprocess.sh
cp setup/install.py install.py
python install.py
rm -f install.py
bash setup/clear_post.sh
