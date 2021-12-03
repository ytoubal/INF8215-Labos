#!/usr/bin/env bash

# TODO: change to your PATH
source /home/yuhan/anaconda3/etc/profile.d/conda.sh

# check if requirements.txt exists?
exist=0
test -f ./requirements.txt
if [ $? == 0 ]
then
  # the file exists
  exist=1
  echo "requirements.txt exists! creating conda env..."
  conda create -y --name "tmp" python=3.8
  echo "activating..."
  conda activate "tmp"
  echo "installing..."
  pip install -r requirements.txt
fi

echo ""
echo "launching the agent!"
python main.py --train_file ./data/train.csv --test_file ./data/test_public.csv --prediction_file ./data/predictions.csv

# check if we need to close the conda env
if [ $exist == 1 ]
then
  echo "deactivating conda env..."
  conda deactivate
fi

