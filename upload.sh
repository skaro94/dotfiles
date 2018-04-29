#!/bin/bash

# preprocess: fill up values in .pre files
bash preprocess.sh

# git push
git add .
git commit -m "$1"
git push origin master
